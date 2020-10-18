from mirumon.schemas.computer.base import BaseModelWMI


class InstalledProgramModel(BaseModelWMI):
    name: str
    vendor: str
    version: str
