from mirumon.schemas.devices.base import BaseModelWMI


class InstalledProgramModel(BaseModelWMI):
    name: str
    vendor: str
    version: str
