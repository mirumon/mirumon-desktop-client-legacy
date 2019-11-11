from enum import IntEnum

from app.schemas.computer.base import BaseModelWMI


class LogonType(IntEnum):
    interactive = 2


class UserModel(BaseModelWMI):
    name: str
    domain: str
    fullname: str
