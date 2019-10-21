from typing import List, Optional

from pydantic import Schema

from app.schemas.computer.base import BaseComponent


class MotherBoardModel(BaseComponent):
    name: str
    caption: str
    status: str
    product: str
    serial_number: str = Schema(..., alias="serialNumber")


class ProcessorModel(BaseComponent):
    status: str
    name: str
    caption: str
    current_clock_speed: str = Schema(..., alias="CurrentClockSpeed")
    thread_count: Optional[int] = Schema(None, alias="CurrentCThreadCountlockSpeed")
    virtualization_firmware_enabled: bool = Schema(
        ..., alias="VirtualizationFirmwareEnabled"
    )
    load_percentage: int = Schema(..., alias="LoadPercentage")
    number_of_cores: int = Schema(..., alias="NumberOfCores")
    number_of_enabled_core: int = Schema(..., alias="NumberOfEnabledCore")
    number_of_logical_processors: int = Schema(..., alias="NumberOfLogicalProcessors")


class VideoControllerModel(BaseComponent):
    status: str
    name: str
    caption: str
    driver_version: str = Schema(..., alias="DriverVersion")
    driver_date: str = Schema(..., alias="DriverDate")
    video_mode_description: str = Schema(..., alias="VideoModeDescription")
    current_vertical_resolution: str = Schema(..., alias="CurrentVerticalResolution")


class NetworkAdapterModel(BaseComponent):
    description: str
    mac_address: str = Schema(..., alias="MACAddress")
    ip_addresses: List[str] = Schema(..., alias="IPAddress")


class PhysicalDiskModel(BaseComponent):
    status: str
    caption: str
    SerialNumber: Optional[str]
    Size: float
    Model: Optional[str]
    Description: str
    Partitions: int


class HardwareModel(BaseComponent):
    mother: List[MotherBoardModel]
    cpu: List[ProcessorModel]
    gpu: List[VideoControllerModel]
    network: List[NetworkAdapterModel]
    disks: List[PhysicalDiskModel]


class SharedModel(BaseComponent):
    name: str
    path: str = Schema(..., alias="Path")
