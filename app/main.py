import asyncio
import json
from typing import Union

import websockets
import wmi
from loguru import logger
from pydantic import ValidationError

from app.config import settings
from app.schemas.events.base import (
    EventErrorResponse,
    EventInRequest,
    EventInResponse,
    PayloadInResponse,
)
from app.schemas.status import Status, StatusType
from app.services.events_handlers import handle_event
from app.services.wmi_api.operating_system import get_computer_details


class Lifespan:
    is_running: bool = True


@logger.catch
async def server_connection_with_retry(
    lifespan: Lifespan, server_endpoint: str, computer_wmi: wmi.WMI
) -> None:
    while lifespan.is_running:
        try:
            await start_connection(lifespan, server_endpoint, computer_wmi)
        except (websockets.exceptions.ConnectionClosedError, OSError, RuntimeError):
            logger.debug(
                f"will try reconnection after {settings.reconnect_delay} seconds"
            )
            await asyncio.sleep(settings.reconnect_delay)


async def process_registration(
    websocket: websockets.WebSocketClientProtocol, computer_wmi: wmi.WMI
) -> bool:
    logger.info("starting registration...")
    computer = get_computer_details(computer_wmi).json()
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
    logger.info(f"starting connection to server {server_endpoint}")
    websocket = await websockets.connect(server_endpoint)
    try:
        if not await process_registration(websocket, computer_wmi):
            exit(1)  # noqa: WPS421
    except Exception as unknown_error:
        # fixme
        #  while windows start service cant get data from wmi for unknown reason
        #  raising error for reconnecting later when wmi work
        logger.error(f"unknown error during registration {unknown_error}")
        raise RuntimeError

    while lifespan.is_running:
        event_req = json.loads(await websocket.recv())
        logger.debug(f"event request: {event_req}")
        try:
            request = EventInRequest(**event_req)
        except ValidationError as request_error:
            logger.info(f"bad request: {request_error.json()}")
            continue  # todo error response when backend change events format

        try:
            event_payload: Union[PayloadInResponse, EventErrorResponse] = handle_event(
                event_type=request.event.type,
                payload=request.payload,
                computer=computer_wmi,
            )
        except KeyError:
            event_payload = EventErrorResponse(error="event is not supported")
        response = EventInResponse(event=request.event, payload=event_payload).json()
        logger.bind(payload=response).debug(f"event response: {response}")
        await websocket.send(response)
    await websocket.close()
