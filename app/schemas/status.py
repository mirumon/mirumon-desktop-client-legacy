from enum import Enum

from pydantic import BaseModel


class StatusType(str, Enum):
    registration_success: str = "registration-success"
    registration_failed: str = "registration-failed"
    auth_success: str = "auth-success"
    auth_failed: str = "auth-failed"


class Status(BaseModel):
    status: StatusType
