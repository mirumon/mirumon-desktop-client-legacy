import servicemanager
import win32event


class Lifespan:
    def __init__(self, service):
        self.service = service

    @property
    def is_running(self):
        result = win32event.WaitForSingleObject(self.service.hWaitStop, 5)
        is_running = result != win32event.WAIT_OBJECT_0
        return not is_running
