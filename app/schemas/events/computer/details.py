from typing import List

from pydantic import BaseModel

from app.schemas.computer.details import OperatingSystemModel
from app.schemas.computer.users import UserModel


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
    current_user: UserModel
    os: List[OperatingSystemModel]
