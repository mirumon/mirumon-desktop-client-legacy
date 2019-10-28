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

import servicemanager
import win32api
import win32event
import win32service
import win32serviceutil
import wmi

from app.config import settings
from app.main import server_connection_with_retry


class AppServerSvc(win32serviceutil.ServiceFramework):
    # you can NET START/STOP the service by the following name
    _svc_name_ = "MirumonService"
    # this text shows up as the service name in the Service
    # Control Manager (SCM)
    _svc_display_name_ = "Mirumon Service"
    # this text shows up as the description in the SCM
    _svc_description_ = "Monitoring service by mirumon team"

    # _exe_name_ = "MirumonService.exe"  # ??? #_exe_path_

    is_running: bool

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # create an event to listen for stop requests on
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        servicemanager.LogInfoMsg("service started")

        asyncio.run(
            server_connection_with_retry(
                service=self, server_endpoint=settings.server_websocket_url,
                computer_wmi=wmi.WMI()
            )
        )
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def SvcStop(self):
        # tell the SCM we're shutting down
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # fire the stop event
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False


if __name__ == '__main__':
    win32api.SetConsoleCtrlHandler(lambda _: True, True)
    win32serviceutil.HandleCommandLine(AppServerSvc)
