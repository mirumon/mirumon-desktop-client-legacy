from typing import List

from schemas.base import BaseComponent
from schemas.components import (
    OperatingSystemModel,
    ComputerSystemModel,
    MotherBoardModel,
    ProcessorModel,
    VideoControllerModel,
    NetworkAdapterModel,
    PhysicalDiskModel,
    SharedModel,
    StartupCommandModel,
    EnvironmentModel,
    InstalledProgramModel,
    PrinterModel,
    UserAccountModel,
)


class ComputerModel(BaseComponent):
    operating_systems: List[OperatingSystemModel] = []

    computer_systems: List[ComputerSystemModel] = []
    mother_boards: List[MotherBoardModel] = []
    cpu: List[ProcessorModel] = []
    gpu: List[VideoControllerModel] = []
    network_adapters: List[NetworkAdapterModel] = []

    users: List[UserAccountModel] = []

    disks: List[PhysicalDiskModel] = []
    shared: List[SharedModel] = []

    startup_commands: List[StartupCommandModel] = []
    environment: List[EnvironmentModel] = []
    programs: List[InstalledProgramModel] = []

    printers: List[PrinterModel] = []

    services: List = []

    processes: List = []
