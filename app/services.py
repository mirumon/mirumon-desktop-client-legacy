from typing import Any, List
from uuid import getnode as get_mac

import wmi
from loguru import logger

from app.schemas.computer.overview import ComputerSystemModel
from app.schemas.computer.software import InstalledProgramModel
from app.schemas.computer.users import LogonType, User
from app.schemas.events.base import EventType
from app.schemas.events.computer.details import ComputerDetails, ComputerInList


def get_computer_mac_address() -> str:
    """Convert uuid.getnode() result to mac address by some magic"""
    mac = get_mac()
    magic_number = 12
    hex_mac = iter(hex(mac)[2:].zfill(magic_number))
    return ":".join(num + next(hex_mac) for num in hex_mac)


def get_current_user(computer: wmi.WMI) -> User:
    for s in computer.Win32_LogonSession():
        if s.LogonType != LogonType.interactive:
            continue
        try:
            for user in s.references("Win32_LoggedOnUser"):
                return User.from_orm(user.Antecedent)
        except wmi.x_wmi:
            continue


def handle_event(event_type: EventType, mac_address: str, computer: wmi.WMI) -> Any:
    return event_handlers[event_type](mac_address=mac_address, computer=computer)


def get_computer_details(mac_address: str, computer: wmi.WMI) -> ComputerDetails:
    computer_system = computer.Win32_ComputerSystem()[0]
    model = ComputerSystemModel.from_orm(computer_system)
    user = get_current_user(computer)
    return ComputerDetails(
        mac_address=mac_address,
        name=model.name,
        domain=model.domain,
        workgroup=model.workgroup,
        current_user=user,
    )


def get_computer_in_list(mac_address: str, computer: wmi.WMI) -> ComputerInList:
    computer_system = computer.Win32_ComputerSystem()[0]
    pc = ComputerSystemModel.from_orm(computer_system)
    user = get_current_user(computer)
    return ComputerInList(
        mac_address=mac_address,
        name=pc.name,
        domain=pc.domain,
        workgroup=pc.workgroup,
        username=user.name,
        part_of_domain=pc.part_of_domain,
    )


def get_installed_programs(computer: wmi.WMI, **_) -> List[InstalledProgramModel]:
    try:
        return [
            InstalledProgramModel.from_orm(program)
            for program in computer.Win32_InstalledWin32Program()
        ]
    except wmi.x_access_denied:
        logger.error("Run as admin to see installed programs!")
        raise KeyError


event_handlers = {
    EventType.details: get_computer_details,
    EventType.computers_list: get_computer_in_list,
    EventType.installed_programs: get_installed_programs,
}
