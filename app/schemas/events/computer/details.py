from typing import List

from pydantic import BaseModel

from app.schemas.computer.details import OperatingSystemModel
from app.schemas.computer.users import User


class ComputerInList(BaseModel):
    mac_address: str
    name: str
    username: str
    workgroup: str
    domain: str
    part_of_domain: bool


class ComputerDetails(BaseModel):
    mac_address: str
    name: str
    domain: str
    workgroup: str
    current_user: User
    os: List[OperatingSystemModel]
