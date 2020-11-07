from enum import Enum
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel

from mirumon.schemas.devices.hardware import (
    HardwareModel,
    MotherBoardModel,
    NetworkAdapterModel,
    PhysicalDiskModel,
    ProcessorModel,
    VideoControllerModel,
)
from mirumon.schemas.devices.software import InstalledProgramModel
from mirumon.schemas.events.details import ComputerDetails, ComputerInList
from mirumon.schemas.events.execute import ExecuteCommand, ExecuteResult
from mirumon.schemas.events.shutdown import Shutdown


class EventType(str, Enum):  # noqa: WPS600
    devices_list: str = "list"
    details: str = "detail"

    hardware: str = "hardware"
    hardware_motherboard: str = "hardware:motherboard"
    hardware_cpu: str = "hardware:cpu"
    hardware_gpu: str = "hardware:gpu"
    hardware_network: str = "hardware:network"
    hardware_disks: str = "hardware:disks"

    installed_programs: str = "software"

    shutdown: str = "shutdown"

    execute: str = "execute"

    def __str__(self) -> str:
        return self.value


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
    id: UUID
    method: EventType
    params: Optional[dict]


class EventInResponse(BaseModel):
    status: str = "ok"
    id: UUID
    method: EventType
    result: Optional[PayloadInResponse]
    error: Optional[dict]
