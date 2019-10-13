import asyncio
import json
import logging

import websockets
import wmi

from schemas.computer.overview import ComputerDetails, ComputerSystemModel
from schemas.computer.users import UserAccountModel
from schemas.events import EventType, EventInRequest, EventInResponse
from schemas.registration import ComputerInRegistration, Status, StatusEnum
from utils import get_pk_field_for_computer

logging.basicConfig(level=logging.DEBUG)

COMPUTER = wmi.WMI()

# def get_hardware(computer):
#     models = [
#         MotherBoardModel, ProcessorModel, VideoControllerModel, NetworkAdapterModel,
#         PhysicalDiskModel]
#     wmi_objects = [computer.Win32_BaseBoard, computer.Win32_Processor,
#                    computer.Win32_VideoController,
#                    computer.Win32_NetworkAdapterConfiguration,  # (IPEnabled=1),
#                    computer.Win32_DiskDrive]
#
#     d = {}
#     keys = list(HardwareModel.schema()["properties"].keys())
#     print(models)
#     print(wmi_objects)
#     print(keys)
#     for model, interface, key in (models, wmi_objects, keys):
#         d[key] = model.from_orm(interface())
#
#     return HardwareModel(**d)

EVENTS_HANDLERS = {
    EventType.system: lambda: [
        ComputerSystemModel.from_orm(obj).dict()
        for obj in COMPUTER.Win32_ComputerSystem()
    ],
    EventType.users: lambda: [
        UserAccountModel.from_orm(user).dict() for user in COMPUTER.Win32_UserAccount()
    ],
    EventType.processes: lambda: [
        {"name": pr.name, "id": pr.ProcessId} for pr in COMPUTER.Win32_Process()
    ],
}


async def start_connection(server_endpoint, computer: wmi.WMI):
    websocket = await websockets.connect(server_endpoint)
    pc_id = get_pk_field_for_computer(computer)

    computer = ComputerDetails(name="nick-desktop", domain="mirumon",
                               workgroup="mirumon",
                               current_user={"username": "nick"}, )
    payload = ComputerInRegistration(mac_address=pc_id, name="name", details=computer)
    logging.debug(payload.json())
    await websocket.send(payload.json())

    auth_response = json.loads(await websocket.recv())
    logging.debug(auth_response)
    status = Status(**auth_response)
    logging.info(status.status)
    if status.status == StatusEnum.registration_failed:
        exit(1)

    while True:
        recv = await websocket.recv()
        logging.debug(recv)
        payload = json.loads(recv)
        request = EventInRequest(**payload)

        computer_info = EVENTS_HANDLERS[request.event.type]()
        logging.debug(computer_info)

        response = EventInResponse(event=request.event, payload=computer_info)
        await websocket.send(json.dumps(response.dict()))


WEBSOCKET_URL = "localhost:8000/clients/ws"
WEBSOCKET_URL = "api.mirumon.dev/clients/ws"
asyncio.get_event_loop().run_until_complete(
    start_connection(server_endpoint=f"ws://{WEBSOCKET_URL}", computer=wmi.WMI())
)
asyncio.get_event_loop().run_forever()
