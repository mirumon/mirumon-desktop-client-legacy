from enum import Enum
from typing import List, Union
from uuid import UUID

from pydantic import BaseModel

from app.schemas.computer.hardware import (
    HardwareModel,
    MotherBoardModel,
    NetworkAdapterModel,
    PhysicalDiskModel,
    ProcessorModel,
    VideoControllerModel,
)
from app.schemas.computer.software import InstalledProgramModel
from app.schemas.events.computer.details import ComputerDetails, ComputerInList
from app.schemas.events.computer.shutdown import Shutdown

EventPayload = Union[
    ComputerInList,
    ComputerDetails,
    List[InstalledProgramModel],
    MotherBoardModel,
    List[NetworkAdapterModel],
    List[PhysicalDiskModel],
    List[ProcessorModel],
    List[VideoControllerModel],
    HardwareModel,
    Shutdown,
]


class EventType(str, Enum):  # noqa: WPS600
    registration: str = "registration"

    computers_list: str = "computers-list"
    details: str = "details"

    hardware: str = "hardware"
    hardware_motherboard: str = "hardware:motherboard"
    hardware_cpu: str = "hardware:cpu"
    hardware_gpu: str = "hardware:gpu"
    hardware_network: str = "hardware:network"
    hardware_disks: str = "hardware:disks"

    installed_programs: str = "installed-programs"

    shutdown: str = "shutdown"

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
    error: str
