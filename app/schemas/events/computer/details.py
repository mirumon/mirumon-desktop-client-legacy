from typing import Dict, List

from pydantic import BaseModel


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
    current_user: Dict
    os: List = []
