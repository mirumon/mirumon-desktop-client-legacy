from typing import Optional
from pydantic import Field
from mirumon.schemas.computer.base import BaseModelWMI


class ComputerSystemModel(BaseModelWMI):
    name: str
    username: str
    workgroup: Optional[str] = None
    domain: str
    part_of_domain: bool


class OperatingSystemModel(BaseModelWMI):
    name: str = Field(..., alias="caption")
    version: str
    build_number: str
    os_architecture: str
    serial_number: str
    product_type: str
    number_of_users: int
    install_date: str
