from typing import Any
from uuid import getnode as get_mac

import wmi
from app.schemas.computer import ComputerSystemModel
from app.schemas.events import ComputerDetails, ComputerInList, EventType


def get_computer_mac_address() -> str:
    """Convert uuid.getnode() result to mac address by some magic"""
    mac = get_mac()
    h = iter(hex(mac)[2:].zfill(12))
    return ":".join(i + next(h) for i in h)


def get_current_user(computer: wmi.WMI) -> Any:
    return (
        computer.Win32_LogonSession()[0].references("Win32_LoggedOnUser")[0].Antecedent
    )


def handle_event(event_type: EventType, mac_address: str, computer: wmi.WMI):
    handler = EVENTS_HANDLERS[event_type]
    return handler(mac_address, computer)


def get_computer_details(mac_address: str, computer: wmi.WMI) -> ComputerDetails:
    computer_system = computer.Win32_ComputerSystem()[0]
    model = ComputerSystemModel.from_orm(computer_system)
    user = get_current_user(computer)
    return ComputerDetails(
        mac_address=mac_address,
        name=model.name,
        domain=model.domain,
        workgroup=model.workgroup,
        current_user={"name": user.name},
    )


def get_computer_in_list(mac_address: str, computer: wmi.WMI) -> ComputerInList:
    computer_system = computer.Win32_ComputerSystem()[0]
    model = ComputerSystemModel.from_orm(computer_system)
    user = get_current_user(computer)
    return ComputerInList(
        mac_address=mac_address,
        name=model.name,
        domain=model.domain,
        workgroup=model.workgroup,
        username=user.name,
        part_of_domain=model.part_of_domain,
    )


EVENTS_HANDLERS = {
    EventType.details: get_computer_details,
    EventType.computers_list: get_computer_in_list,
}
