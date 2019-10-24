from app.schemas.computer.base import BaseComponent


class InstalledProgramModel(BaseComponent):
    name: str
    vendor: str
    version: str
