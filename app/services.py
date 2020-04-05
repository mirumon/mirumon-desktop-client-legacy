from typing import Callable, Dict, List
from uuid import getnode as get_mac

import wmi
from loguru import logger

from app.schemas.computer.details import ComputerSystemModel, OperatingSystemModel
from app.schemas.computer.hardware import (
    HardwareModel,
    MotherBoardModel,
    NetworkAdapterModel,
    PhysicalDiskModel,
    ProcessorModel,
    VideoControllerModel,
)
from app.schemas.computer.software import InstalledProgramModel
from app.schemas.computer.users import LogonType, UserModel
from app.schemas.events.base import EventPayload, EventType
from app.schemas.events.computer.details import ComputerDetails, ComputerInList


def get_computer_mac_address() -> str:
    """Convert uuid.getnode() result to mac address by some magic"""
    mac = get_mac()
    magic_number = 12
    hex_mac = iter(hex(mac)[2:].zfill(magic_number))
    return ":".join(num + next(hex_mac) for num in hex_mac)


def get_current_user(computer: wmi.WMI) -> UserModel:
    for session in computer.Win32_LogonSession():
        if session.LogonType != LogonType.interactive:
            continue
        user = session.references("Win32_LoggedOnUser")[0]
        return UserModel.from_orm(user.Antecedent)
    raise RuntimeError("No interactive logon sessions")


def get_operating_systems(computer: wmi.WMI) -> List[OperatingSystemModel]:
    return [
        OperatingSystemModel.from_orm(os) for os in computer.Win32_OperatingSystem()
    ]


def handle_event(*, event_type: EventType, computer: wmi.WMI) -> EventPayload:
    func = event_handlers[event_type]
    return func(computer)


def get_computer_details(computer: wmi.WMI) -> ComputerDetails:
    computer_system = computer.Win32_ComputerSystem()[0]
    model = ComputerSystemModel.from_orm(computer_system)
    user = get_current_user(computer)
    os = get_operating_systems(computer)
    return ComputerDetails(
        mac_address=get_computer_mac_address(),
        name=model.name,
        domain=model.domain,
        workgroup=model.workgroup,
        current_user=user,
        os=os,
    )


def get_computer_in_list(computer: wmi.WMI) -> ComputerInList:
    computer_system = computer.Win32_ComputerSystem()[0]
    pc = ComputerSystemModel.from_orm(computer_system)
    user = get_current_user(computer)
    return ComputerInList(
        mac_address=get_computer_mac_address(),
        name=pc.name,
        domain=pc.domain,
        workgroup=pc.workgroup,
        username=user.name,
        part_of_domain=pc.part_of_domain,
    )


def get_installed_programs(computer: wmi.WMI) -> List[InstalledProgramModel]:
    try:
        return [
            InstalledProgramModel.from_orm(program)
            for program in computer.Win32_InstalledWin32Program()
        ]
    except wmi.x_access_denied:
        logger.error("Run as admin to see installed programs!")
        raise KeyError


def get_motherboard(computer: wmi.WMI) -> MotherBoardModel:
    mother = computer.Win32_BaseBoard()[0]
    return MotherBoardModel.from_orm(mother)


def get_cpu(computer: wmi.WMI) -> List[ProcessorModel]:
    return [ProcessorModel.from_orm(cpu) for cpu in computer.Win32_Processor()]


def get_gpu(computer: wmi.WMI) -> List[VideoControllerModel]:
    return [
        VideoControllerModel.from_orm(gpu) for gpu in computer.Win32_VideoController()
    ]


def get_network_adapters(computer: wmi.WMI) -> List[NetworkAdapterModel]:
    return [
        NetworkAdapterModel.from_orm(interface)
        for interface in computer.Win32_NetworkAdapterConfiguration(IPEnabled=1)
    ]


def get_physical_disks(computer: wmi.WMI) -> List[PhysicalDiskModel]:
    return [
        PhysicalDiskModel.from_orm(physical_disk)
        for physical_disk in computer.Win32_DiskDrive()
    ]


def get_hardware(computer: wmi.WMI) -> HardwareModel:
    return HardwareModel(
        motherboard=get_motherboard(computer),
        cpu=get_cpu(computer),
        gpu=get_gpu(computer),
        network=get_network_adapters(computer),
        disks=get_physical_disks(computer),
    )


event_handlers: Dict[EventType, Callable[[wmi.WMI], EventPayload]] = {
    EventType.details: get_computer_details,
    EventType.computers_list: get_computer_in_list,
    EventType.installed_programs: get_installed_programs,
    EventType.hardware_cpu: get_cpu,
    EventType.hardware_motherboard: get_motherboard,
    EventType.hardware_gpu: get_gpu,
    EventType.hardware_disks: get_physical_disks,
    EventType.hardware_network: get_network_adapters,
    EventType.hardware: get_hardware,
}
