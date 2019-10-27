from app.schemas.computer.base import BaseComponent


class ComputerSystemModel(BaseComponent):
    name: str
    username: str
    workgroup: str
    domain: str
    part_of_domain: bool


class OperatingSystemModel(BaseComponent):
    caption: str
    version: str
    build_number: str
    os_architecture: str
    serial_number: str
    product_type: str
    number_of_users: int
    install_date: str
