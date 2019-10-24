from pydantic import Schema

from app.schemas.computer.base import BaseComponent


class ComputerSystemModel(BaseComponent):
    name: str
    username: str
    workgroup: str
    domain: str
    part_of_domain: bool = Schema(..., alias="PartOfDomain")
