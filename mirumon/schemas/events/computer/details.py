from typing import List, Optional

from pydantic import BaseModel

from mirumon.schemas.computer.details import OperatingSystemModel
from mirumon.schemas.computer.users import UserModel


class ComputerInList(BaseModel):
    mac_address: str
    name: str
    domain: Optional[str]
    workgroup: Optional[str]
    last_user: UserModel
    part_of_domain: bool


class ComputerDetails(BaseModel):
    mac_address: str
    name: str
    domain: Optional[str]
    workgroup: Optional[str]
    last_user: UserModel
    os: List[OperatingSystemModel]
