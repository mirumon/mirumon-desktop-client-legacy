from enum import Enum

from pydantic import BaseModel


class StatusType(str, Enum):  # noqa: WPS600
    registration_success: str = "registration-success"
    registration_failed: str = "registration-failed"
    auth_success: str = "auth-success"
    auth_failed: str = "auth-failed"

    def __str__(self):
        return self.value


class Status(BaseModel):
    status: StatusType
