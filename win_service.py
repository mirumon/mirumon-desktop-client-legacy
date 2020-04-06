"""
Script for starting mirumon client like windows service

Commands:
python "venv\Scripts\pywin32_postinstall.py" -install
python.exe .\win_service.py --startup=auto install
python.exe .\win_service.py start
NET START MirumonService

http://thepythoncorner.com/dev/how-to-create-a-windows-service-in-python/


nuitka compile:
python -m nuitka --standalone --windows-dependency-tool=pefile --experimental=use_pefile_recurse --experimental=use_pefile_fullrecurse --follow-imports  --mingw64 --show-progress  --python-arch=x86_64 --include-module=win32timezone win_service.py

"""

import os, sys, site

project_name = "mirumon-desktop-client"  # Change this for your own project !!!!!!!!!!!!!!
venv_folder_name = "venv"  # Change this for your own venv path !!!!!!!!!!!!!!

if sys.executable.lower().endswith("pythonservice.exe"):  # https://issue.life/questions/34696815

    # Get root path for the project
    service_directory = os.path.abspath(os.path.dirname(__file__))
    project_directory = service_directory[:service_directory.find(project_name)+len(project_name)]

    # Get venv path for the project
    def file_path(x): return os.path.join(project_directory, x)
    venv_base = file_path(venv_folder_name)
    venv_scripts = os.path.join(venv_base, "Scripts")
    venv_packages = os.path.join(venv_base, 'Lib', 'site-packages')

    # Change current working directory from PythonService.exe location to something better.
    os.chdir(project_directory)
    sys.path.append(".")
    prev_sys_path = list(sys.path)

    # Manually activate a virtual environment inside an already initialized interpreter.
    os.environ['PATH'] = venv_scripts + os.pathsep + os.environ['PATH']

    site.addsitedir(venv_packages)
    sys.real_prefix = sys.prefix
    sys.prefix = venv_base

    # Move some sys path in front of others
    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)
    sys.path[:0] = new_sys_path


import asyncio
import logging

import servicemanager
import win32event
import win32service
from loguru import logger
import win32serviceutil
import wmi
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
