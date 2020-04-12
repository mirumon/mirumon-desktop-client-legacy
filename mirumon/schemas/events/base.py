from enum import Enum
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel

from mirumon.schemas.computer.hardware import (
    HardwareModel,
    MotherBoardModel,
    NetworkAdapterModel,
    PhysicalDiskModel,
    ProcessorModel,
    VideoControllerModel,
)
from mirumon.schemas.computer.software import InstalledProgramModel
from mirumon.schemas.events.computer.details import ComputerDetails, ComputerInList
from mirumon.schemas.events.computer.execute import ExecuteCommand, ExecuteResult
from mirumon.schemas.events.computer.shutdown import Shutdown


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

    execute: str = "execute"

    def __str__(self) -> str:
        return self.value


PayloadInRequest = Optional[Union[ExecuteCommand]]

PayloadInResponse = Union[
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
    ExecuteCommand,
    ExecuteResult,
]


class Event(BaseModel):
    type: EventType
    id: UUID


class EventInRequest(BaseModel):
    event: Event
    payload: PayloadInRequest


class EventInResponse(BaseModel):
    event: Event
    payload: PayloadInResponse


class EventErrorResponse(BaseModel):
    error: str
