from enum import Enum

from pydantic import BaseModel

from schemas.computer.overview import ComputerDetails


class ComputerInRegistration(BaseModel):
    mac_address: str
    name: str
    details: ComputerDetails


class StatusEnum(Enum):
    registration_success: str = "registration_success"
    registration_failed: str = "registration_failed"
    auth_success: str = "auth_success"
    auth_failed: str = "auth_failed"


class Status(BaseModel):
    status: StatusEnum