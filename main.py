# pip install --upgrade wmi
# pip install --upgrade pypiwin32

import wmi

from schemas.schemas import (
    GroupModel,
    OperatingSystemModel,
    ComputerSystemModel,
    MotherBoardModel,
    ProcessorModel,
    VideoControllerModel,
    NetworkAdapterModel,
    DiskModel,
    StartupCommandModel,
    ShareModel,
    PrinterModel,
    InstalledProgramModel,
    EnvironmentModel,
    UserAccountModel,
)

computer = wmi.WMI()

for user in computer.Win32_UserAccount():
    groups = []
    for group in user.associators("Win32_GroupUser"):
        groups.append(GroupModel.from_orm(group))
    u = UserAccountModel.from_orm(user)
    u.groups = groups
    print(u)

for os in computer.Win32_OperatingSystem():
    print(OperatingSystemModel.from_orm(os))

for computer_system in computer.Win32_ComputerSystem():
    print(ComputerSystemModel.from_orm(computer_system))

for mother in computer.Win32_BaseBoard():
    print(MotherBoardModel.from_orm(mother))

for cpu in computer.Win32_Processor():
    print(ProcessorModel.from_orm(cpu))

for gpu in computer.Win32_VideoController():
    print(VideoControllerModel.from_orm(gpu))

for interface in computer.Win32_NetworkAdapterConfiguration(IPEnabled=1):
    print(NetworkAdapterModel.from_orm(interface))

for physical_disk in computer.Win32_DiskDrive():
    print(DiskModel.from_orm(physical_disk))

for share in computer.Win32_Share():
    print(ShareModel.from_orm(share))

for startup in computer.Win32_StartupCommand():
    print(StartupCommandModel.from_orm(startup))

for environment in computer.Win32_Environment():
    print(EnvironmentModel.from_orm(environment))

for printer in computer.Win32_Printer():
    print(PrinterModel.from_orm(printer))

try:
    for program in computer.Win32_InstalledWin32Program():
        print(InstalledProgramModel.from_orm(program))
except wmi.x_access_denied:
    print("Run script as admin to see installed programs!")
