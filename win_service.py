"""
Script for starting mirumon client like windows service

Commands:
python "P:\Python3\Scripts\pywin32_postinstall.py" -install
python.exe .\win_service.py --startup=auto install
python.exe .\win_service.py start
NET START MirumonService

Links:
https://www.chrisumbel.com/article/windows_services_in_python
https://www.thepythoncorner.com/2018/08/how-to-create-a-windows-service-in-python/

"""
import asyncio
import concurrent
import json
from typing import Union

import servicemanager
import websockets
import win32api
import win32event
import win32service
import win32serviceutil
import wmi
from loguru import logger

from app.config import settings
from app.main import process_registration
from app.schemas.events.base import (
    EventErrorResponse,
    EventInRequest,
    EventInResponse,
    EventPayload,
)
from app.services import get_computer_mac_address, handle_event


class AppServerSvc(win32serviceutil.ServiceFramework):
    # you can NET START/STOP the service by the following name
    _svc_name_ = "MirumonService"
    # this text shows up as the service name in the Service
    # Control Manager (SCM)
    _svc_display_name_ = "Mirumon Service"
    # this text shows up as the description in the SCM
    _svc_description_ = "Monitoring service by mirumon team"

    # _exe_name_ = "MirumonService.exe"  # ??? #_exe_path_

    _websocket = None

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # create an event to listen for stop requests on
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self._stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        servicemanager.LogInfoMsg("service started")

        asyncio.run(connect(self))

        while True:
            result = win32event.WaitForSingleObject(self._stop_event, 5)

            if result == win32event.WAIT_OBJECT_0:
                # stop requested

                servicemanager.LogInfoMsg('is stopping')
                break

            else:
                servicemanager.LogInfoMsg('is running')
                loop = asyncio.new_event_loop()
                executor = concurrent.futures.ThreadPoolExecutor(5)
                loop.set_default_executor(executor)
                loop.run_until_complete(process(self))

    def _stop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self._stop_event)

    def SvcStop(self):
        self._stop()

    def SvcOtherEx(self, control, event_type, data):
        # See the MSDN documentation for "HandlerEx callback" for a list
        # of control codes that a service can respond to.
        #
        # We respond to `SERVICE_CONTROL_PRESHUTDOWN` instead of
        # `SERVICE_CONTROL_SHUTDOWN` since it seems that we can't log
        # info messages when handling the latter.

        if control == win32service.SERVICE_CONTROL_PRESHUTDOWN:
            servicemanager.LogInfoMsg('received a pre-shutdown notification')
            self._stop()
        else:
            servicemanager.LogInfoMsg(
                'received an event: code={}, type={}, data={}'.format(
                    control, event_type, data))


async def connect(service: AppServerSvc):
    AppServerSvc._websocket = await websockets.connect(settings.server_websocket_url)
    service._mac_address = get_computer_mac_address()
    service._computer_wmi = wmi.WMI()
    if not await process_registration(service._mac_address, AppServerSvc._websocket,
                                      service._computer_wmi):
        exit(401)  # noqa: WPS421


async def process(service: AppServerSvc):
    request = EventInRequest(**json.loads(await service._websocket.recv()))
    try:
        event_payload: Union[
            EventPayload, EventErrorResponse] = handle_event(
            event_type=request.event.type,
            mac_address=service._mac_address,
            computer=service._computer_wmi,
        )
    except KeyError:
        event_payload = EventErrorResponse(error="event is not supported")
    response = EventInResponse(event=request.event,
                               payload=event_payload).json()
    logger.bind(payload=response).debug("event response")
    await service._websocket.send(response)


if __name__ == '__main__':
    win32api.SetConsoleCtrlHandler(lambda _: True, True)
    win32serviceutil.HandleCommandLine(AppServerSvc)
