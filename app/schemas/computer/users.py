from enum import IntEnum

from app.schemas.computer.base import BaseComponent


class LogonType(IntEnum):
    interactive = 2


class User(BaseComponent):
    name: str
    domain: str
    fullname: str
