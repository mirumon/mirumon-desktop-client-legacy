from typing import Dict
from typing import Optional, List

from pydantic import BaseModel
from pydantic import Schema

from schemas.computer.base import BaseComponent


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
    part_of_domain: bool = Schema(..., alias="PartOfDomain")
    domain: str
    number_of_processors: int = Schema(..., alias="NumberOfProcessors")
    number_of_enabled_core: Optional[int] = Schema(None, alias="NumberOfEnabledCore")
    number_of_logical_processors: int = Schema(..., alias="NumberOfLogicalProcessors")


class ComputerInList(BaseModel):
    name: str
    username: str
    domain: str


class ComputerDetails(BaseModel):  # todo create models
    name: str
    domain: str
    workgroup: str
    users: List = []
    current_user: Dict
    logon_users: List = []
    os: List = []
    enviroment: List = []
