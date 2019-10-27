from enum import IntEnum

from pydantic import Field

from app.schemas.computer.base import BaseComponent


class LogonType(IntEnum):
    interactive = 2


class User(BaseComponent):
    name: str = Field(..., alias="Name")
    domain: str = Field(..., alias="Domain")
    fullname: str = Field(..., alias="FullName")
