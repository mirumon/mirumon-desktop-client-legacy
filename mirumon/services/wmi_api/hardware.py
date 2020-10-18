from typing import Any, List

import wmi

from mirumon.schemas.computer.hardware import (
    HardwareModel,
    MotherBoardModel,
    NetworkAdapterModel,
    PhysicalDiskModel,
    ProcessorModel,
    VideoControllerModel,
)


def get_motherboard(computer: wmi.WMI, *_: Any) -> MotherBoardModel:
    mother = computer.Win32_BaseBoard()[0]
    return MotherBoardModel.from_orm(mother)


def get_cpu(computer: wmi.WMI, *_: Any) -> List[ProcessorModel]:
    return [ProcessorModel.from_orm(cpu) for cpu in computer.Win32_Processor()]


def get_gpu(computer: wmi.WMI, *_: Any) -> List[VideoControllerModel]:
    return [
        VideoControllerModel.from_orm(gpu) for gpu in computer.Win32_VideoController()
    ]


def get_network_adapters(computer: wmi.WMI, *_: Any) -> List[NetworkAdapterModel]:
    return [
        NetworkAdapterModel.from_orm(interface)
        for interface in computer.Win32_NetworkAdapterConfiguration(IPEnabled=1)
    ]


def get_physical_disks(computer: wmi.WMI, *_: Any) -> List[PhysicalDiskModel]:
    return [
        PhysicalDiskModel.from_orm(physical_disk)
        for physical_disk in computer.Win32_DiskDrive()
    ]


def get_hardware(computer: wmi.WMI, *_: Any) -> HardwareModel:
    return HardwareModel(
        motherboard=get_motherboard(computer),
        cpu=get_cpu(computer),
        gpu=get_gpu(computer),
        network=get_network_adapters(computer),
        disks=get_physical_disks(computer),
    )
