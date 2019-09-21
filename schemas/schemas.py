from schemas.base import BaseComponent
from pydantic import Schema
from typing import Optional, List


class OperatingSystemModel(BaseComponent):
    status: str
    caption: str
    version: str
    build_number: str = Schema(..., alias="BuildNumber")
    architecture: str = Schema(..., alias="OSArchitecture")
    serial_number: str = Schema(..., alias="SerialNumber")
    mui_languages: List[str] = Schema(..., alias="MUILanguages")
    product_type: str = Schema(..., alias="ProductType")
    number_of_users: int = Schema(..., alias="NumberOfUsers")

    total_visible_memory_size: float = Schema(..., alias="TotalVisibleMemorySize")
    total_virtual_memory_size: float = Schema(..., alias="TotalVirtualMemorySize")

    free_physical_memory: float = Schema(..., alias="FreePhysicalMemory")
    free_virtual_memory: float = Schema(..., alias="FreeVirtualMemory")


class ComputerSystemModel(BaseComponent):
    caption: str
    name: str
    username: str
    workgroup: str
    domain: str
    part_of_domain: bool = Schema(..., alias="PartOfDomain")
    number_of_processors: int = Schema(..., alias="NumberOfProcessors")
    number_of_enabled_core: Optional[int] = Schema(None, alias="NumberOfEnabledCore")
    number_of_logical_processors: int = Schema(..., alias="NumberOfLogicalProcessors")


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


class DiskModel(BaseComponent):
    status: str
    caption: str
    SerialNumber: Optional[str]
    Size: float
    Model: Optional[str]
    Description: str
    Partitions: int


class ShareModel(BaseComponent):
    name: str
    path: str = Schema(..., alias="Path")


class StartupCommandModel(BaseComponent):
    caption: str
    description: str
    user: str
    command: str
    location: str


class EnvironmentModel(BaseComponent):
    name: str
    username: str
    variable_value: str = Schema(..., alias="VariableValue")
    system_variable: bool = Schema(..., alias="SystemVariable")


class InstalledProgramModel(BaseComponent):
    name: str
    vendor: str
    version: str


class PrinterModel(BaseComponent):
    caption: str
    hidden: bool
    shared: bool
    published: bool
    printer_status: str = Schema(..., alias="PrinterStatus")
    driver_name: str = Schema(..., alias="DriverName")


class GroupModel(BaseComponent):
    status: str
    caption: str
    description: str
    domain: str
    name: str
    local_account: bool = Schema(..., alias="LocalAccount")

    def __str__(self):
        return self.name


class UserAccountModel(BaseComponent):
    status: str
    name: str
    fullname: str
    domain: str
    disabled: bool
    local_account: bool = Schema(..., alias="LocalAccount")
    lockout: bool
    groups: List[GroupModel] = []
    password_changeable: str = Schema(..., alias="PasswordChangeable")
    password_expires: str = Schema(..., alias="PasswordExpires")
    password_required: str = Schema(..., alias="PasswordRequired")
