import asyncio
import subprocess  # noqa: S404
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Any, List
from uuid import getnode as get_mac

import wmi
from loguru import logger

from mirumon.schemas.computer.details import ComputerSystemModel, OperatingSystemModel
from mirumon.schemas.computer.users import LogonType, UserModel
from mirumon.schemas.events.computer.details import ComputerDetails, ComputerInList
from mirumon.schemas.events.computer.execute import ExecuteCommand, ExecuteResult
from mirumon.schemas.events.computer.shutdown import Shutdown


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


def get_computer_details(computer: wmi.WMI, *_: Any) -> ComputerDetails:
    computer_system = computer.Win32_ComputerSystem()[0]
    model = ComputerSystemModel.from_orm(computer_system)
    user = get_current_user(computer)
    os = get_operating_systems(computer)
    return ComputerDetails(
        mac_address=get_computer_mac_address(),
        name=model.name,
        domain=model.domain,
        workgroup=model.workgroup,
        last_user=user,
        os=os,
    )


def get_computer_in_list(computer: wmi.WMI, *_: Any) -> ComputerInList:
    computer_system = computer.Win32_ComputerSystem()[0]
    pc = ComputerSystemModel.from_orm(computer_system)
    user = get_current_user(computer)
    return ComputerInList(
        mac_address=get_computer_mac_address(),
        name=pc.name,
        domain=pc.domain,
        workgroup=pc.workgroup,
        last_user=user,
        part_of_domain=pc.part_of_domain,
    )


def shutdown(computer: wmi.WMI, *_: Any) -> Shutdown:
    os = computer.Win32_OperatingSystem(Primary=1)[0]
    logger.info("shutdown...")
    os.Shutdown()
    logger.info("process shutdown")
    return Shutdown(status="ok")


def command_execute(_: wmi.WMI, payload: dict) -> ExecuteResult:
    execute = ExecuteCommand(**payload)
    command = f"{execute.command} {execute.args_str}"

    executor = ThreadPoolExecutor(max_workers=1)
    asyncio.get_event_loop().run_in_executor(executor, subprocess.call, command)
    return ExecuteResult(status="ok")
