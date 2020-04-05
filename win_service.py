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
import logging

import servicemanager
import win32event
import win32service
import win32serviceutil
import wmi
from loguru import logger

from app import config
from app.main import Lifespan, server_connection_with_retry


class ServiceHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        servicemanager.LogInfoMsg(record.getMessage())


logger.add(ServiceHandler())


async def start(service):
    service.loop.create_task(
        server_connection_with_retry(
            service.lifespan,
            config.settings.server_websocket_url,
            wmi.WMI(privileges=["Shutdown", "RemoteShutdown"])
        )
    )
    await service.event.wait()


class AppServerSvc(win32serviceutil.ServiceFramework):
    # you can NET START/STOP the service by the following name
    _svc_name_ = "MirumonService"
    # this text shows up as the service name in the Service
    # Control Manager (SCM)
    _svc_display_name_ = "Mirumon Service"
    # this text shows up as the description in the SCM
    _svc_description_ = "Monitoring service by mirumon team"

    event: asyncio.Event
    lifespan: Lifespan

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # create an event to listen for stop requests on
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

        self.lifespan = Lifespan()
        self.loop = asyncio.get_event_loop()

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)

        self.event = asyncio.Event()
        self.loop.run_until_complete(start(self))
        servicemanager.LogInfoMsg("service stopped")

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.lifespan.is_running = False
        self.event.set()

    def SvcOtherEx(self, control, event_type, data):
        # See the MSDN documentation for "HandlerEx callback" for a list
        # of control codes that a service can respond to.
        #
        # We respond to `SERVICE_CONTROL_PRESHUTDOWN` instead of
        # `SERVICE_CONTROL_SHUTDOWN` since it seems that we can't log
        # info messages when handling the latter.

        if control == win32service.SERVICE_CONTROL_PRESHUTDOWN:
            servicemanager.LogInfoMsg('received a pre-shutdown notification')
            self.SvcStop()
        else:
            servicemanager.LogInfoMsg(
                'received an event: code={}, type={}, data={}'.format(
                    control, event_type, data))


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
