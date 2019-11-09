import asyncio
import json
from typing import Union

import websockets
import wmi
from loguru import logger

from app.config import settings
from app.schemas.events.base import (
    EventErrorResponse,
    EventInRequest,
    EventInResponse,
    EventPayload,
)
from app.schemas.status import Status, StatusType
from app.services import get_computer_details, get_computer_mac_address, handle_event


class Lifespan:
    is_running: bool = True


@logger.catch
async def server_connection_with_retry(
    lifespan: Lifespan, server_endpoint: str, computer_wmi: wmi.WMI
) -> None:
    while lifespan.is_running:
        try:
            await start_connection(lifespan, server_endpoint, computer_wmi)
        except (websockets.exceptions.ConnectionClosedError, OSError):
            await asyncio.sleep(settings.reconnect_delay)
            logger.debug(f"reconnection after {settings.reconnect_delay} seconds")


async def process_registration(
    mac_address: str,
    websocket: websockets.WebSocketClientProtocol,
    computer_wmi: wmi.WMI,
) -> bool:
    computer = get_computer_details(computer_wmi, mac_address).json()
    logger.bind(payload=computer).debug("process registration")
    await websocket.send(computer)
    auth_response = json.loads(await websocket.recv())
    logger.debug(auth_response)
    status = Status(**auth_response)
    logger.info(f"registration status: {status.status}")
    return status.status == StatusType.registration_success


async def start_connection(
    lifespan: Lifespan, server_endpoint: str, computer_wmi: wmi.WMI
) -> None:  # noqa: WPS210
    websocket = await websockets.connect(server_endpoint)
    mac_address = get_computer_mac_address()
    if not await process_registration(mac_address, websocket, computer_wmi):
        exit(1)  # noqa: WPS421

    while lifespan.is_running:
        request = EventInRequest(**json.loads(await websocket.recv()))
        try:
            event_payload: Union[EventPayload, EventErrorResponse] = handle_event(
                event_type=request.event.type,
                mac_address=mac_address,
                computer=computer_wmi,
            )
        except KeyError:
            event_payload = EventErrorResponse(error="event is not supported")
        response = EventInResponse(event=request.event, payload=event_payload).json()
        logger.bind(payload=response).debug("event response")
        await websocket.send(response)
