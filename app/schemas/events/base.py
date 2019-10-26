from enum import Enum
from typing import Dict, List, Union
from uuid import UUID

from pydantic import BaseModel

EventPayload = Union[List, Dict]


class EventType(str, Enum):  # noqa: WPS600
    registration: str = "registration"
    auth = "auth"

    computers_list: str = "computers-list"
    details: str = "details"

    users: str = "users"

    system: str = "system"
    hardware: str = "hardware"
    storage: str = "storage"
    network: str = "network"

    devices: str = "devices"

    installed_programs: str = "installed-programs"
    startup_programs: str = "startup-programs"
    services: str = "services"
    processes: str = "processes"

    def __str__(self) -> str:
        return self.value


class Event(BaseModel):
    type: EventType
    id: UUID


class EventInRequest(BaseModel):
    event: Event


class EventInResponse(BaseModel):
    event: Event
    payload: EventPayload


class EventErrorResponse(BaseModel):
    error: Union[str, Dict, List]
