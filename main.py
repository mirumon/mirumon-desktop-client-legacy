# pip install --upgrade wmi
# pip install --upgrade pypiwin32

import wmi

from schemas.components import (
    GroupModel,
    OperatingSystemModel,
    ComputerSystemModel,
    MotherBoardModel,
    ProcessorModel,
    VideoControllerModel,
    NetworkAdapterModel,
    PhysicalDiskModel,
    StartupCommandModel,
    SharedModel,
    PrinterModel,
    InstalledProgramModel,
    EnvironmentModel,
    UserAccountModel,
)
from schemas.computer import ComputerModel

computer = wmi.WMI()

computer_response = ComputerModel()

for user in computer.Win32_UserAccount():
    groups = []
    for group in user.associators("Win32_GroupUser"):
        groups.append(GroupModel.from_orm(group))
    u = UserAccountModel.from_orm(user)
    u.groups = groups
    computer_response.users.append(u)

for os in computer.Win32_OperatingSystem():
    computer_response.operating_systems.append(OperatingSystemModel.from_orm(os))

for computer_system in computer.Win32_ComputerSystem():
    computer_response.computer_systems.append(
        ComputerSystemModel.from_orm(computer_system)
    )

for mother in computer.Win32_BaseBoard():
    computer_response.mother_boards.append(MotherBoardModel.from_orm(mother))

for cpu in computer.Win32_Processor():
    computer_response.cpu.append(ProcessorModel.from_orm(cpu))

for gpu in computer.Win32_VideoController():
    computer_response.gpu.append(VideoControllerModel.from_orm(gpu))

for interface in computer.Win32_NetworkAdapterConfiguration(IPEnabled=1):
    computer_response.network_adapters.append(NetworkAdapterModel.from_orm(interface))

for physical_disk in computer.Win32_DiskDrive():
    computer_response.disks.append(PhysicalDiskModel.from_orm(physical_disk))

for share in computer.Win32_Share():
    computer_response.shared.append(SharedModel.from_orm(share))

for startup in computer.Win32_StartupCommand():
    computer_response.startup_commands.append(StartupCommandModel.from_orm(startup))

for environment in computer.Win32_Environment():
    computer_response.environment.append(EnvironmentModel.from_orm(environment))

for printer in computer.Win32_Printer():
    computer_response.printers.append(PrinterModel.from_orm(printer))

try:
    for program in computer.Win32_InstalledWin32Program():
        computer_response.programs.append(InstalledProgramModel.from_orm(program))
except wmi.x_access_denied:
    print("Run script as admin to see installed programs!")

with open("tmp.py", "w", encoding="utf-8") as file:
    file.write(str(computer_response.dict()))
