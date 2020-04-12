from typing import List, Optional

from pydantic import BaseModel

from mirumon.schemas.computer.details import OperatingSystemModel
from mirumon.schemas.computer.users import UserModel


class ComputerInList(BaseModel):
    mac_address: str
    name: str
    username: str
    workgroup: Optional[str]
    domain: str
    part_of_domain: bool


class ComputerDetails(BaseModel):
    mac_address: str
    name: str
    domain: str
    workgroup: Optional[str]
    current_user: UserModel
    os: List[OperatingSystemModel]
