from typing import Any, List

import wmi
from loguru import logger

from app.schemas.computer.software import InstalledProgramModel


def get_installed_programs(computer: wmi.WMI, *_: Any) -> List[InstalledProgramModel]:
    try:
        return [
            InstalledProgramModel.from_orm(program)
            for program in computer.Win32_InstalledWin32Program()
        ]
    except wmi.x_access_denied:
        logger.error("Run as admin to see installed programs!")
        raise KeyError
