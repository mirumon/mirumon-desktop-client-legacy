from typing import Optional, List

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
    name: str
    username: str
    workgroup: str
    domain: str
    part_of_domain: bool = Schema(..., alias="PartOfDomain")
