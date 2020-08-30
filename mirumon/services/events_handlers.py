from typing import Any, Callable, Dict

import wmi

from mirumon.schemas.events.base import EventType, PayloadInResponse
from mirumon.services.wmi_api.hardware import (
    get_cpu,
    get_gpu,
    get_hardware,
    get_motherboard,
    get_network_adapters,
    get_physical_disks,
)
from mirumon.services.wmi_api.operating_system import (
    command_execute,
    get_computer_details,
    get_computer_in_list,
    shutdown,
)
from mirumon.services.wmi_api.software import get_installed_programs


def handle_event(
    *, event_type: EventType, payload: dict, computer: wmi.WMI
) -> PayloadInResponse:
    func = event_handlers[event_type]
    return func(computer, payload)


event_handlers: Dict[EventType, Callable[[wmi.WMI, Any], PayloadInResponse]] = {
    EventType.details: get_computer_details,
    EventType.computers_list: get_computer_in_list,
    EventType.installed_programs: get_installed_programs,
    EventType.hardware_cpu: get_cpu,
    EventType.hardware_motherboard: get_motherboard,
    EventType.hardware_gpu: get_gpu,
    EventType.hardware_disks: get_physical_disks,
    EventType.hardware_network: get_network_adapters,
    EventType.hardware: get_hardware,
    EventType.shutdown: shutdown,
    EventType.execute: command_execute,
}
