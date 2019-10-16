import asyncio
import json
import logging

import websockets
import wmi

import config
from schemas.events.base import EventInResponse, EventInRequest, EventErrorResponse
from schemas.status import StatusType, Status
from services import get_computer_mac_address, handle_event, get_computer_details


async def start_connection(server_endpoint, computer_wmi: wmi.WMI):
    websocket = await websockets.connect(server_endpoint)

    mac_address = get_computer_mac_address()
    computer = get_computer_details(mac_address, computer_wmi)
    logging.debug(computer)
    await websocket.send(computer.json())

    auth_response = json.loads(await websocket.recv())
    logging.debug(auth_response)
    status = Status(**auth_response)
    logging.info(status.status)
    if status.status == StatusType.registration_failed:
        exit(1)

    while True:
        recv = await websocket.recv()
        logging.debug(recv)
        payload = json.loads(recv)
        request = EventInRequest(**payload)
        try:
            event_payload = handle_event(request.event.type, mac_address, computer_wmi)
        except KeyError:
            await websocket.send(
                EventErrorResponse(error="event is not supported").json()
            )
            continue
        logging.debug(event_payload)
        response = EventInResponse(event=request.event, payload=event_payload)
        await websocket.send(response.json())


asyncio.get_event_loop().run_until_complete(
    start_connection(
        server_endpoint=config.SERVER_WEBSOCKET_URL, computer_wmi=wmi.WMI()
    )
)
asyncio.get_event_loop().run_forever()
