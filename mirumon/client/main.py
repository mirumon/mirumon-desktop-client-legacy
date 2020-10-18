import asyncio
import json

import websockets
import wmi
from loguru import logger
from pydantic import ValidationError

from mirumon.config import Config, init_wmi
from mirumon.schemas.events.base import (
    EventInRequest,
    EventInResponse,
    PayloadInResponse,
)
from mirumon.services.events_handlers import handle_event


@logger.catch
async def server_connection_with_retry(config: Config) -> None:
    try:
        device_wmi = init_wmi(config)
        while True:
            try:
                await start_connection(config.server, config.device_token, device_wmi)
            except (websockets.exceptions.ConnectionClosedError, OSError, RuntimeError):
                logger.debug(
                    f"will try reconnection after {config.reconnect_delay} seconds"
                )
                await asyncio.sleep(config.reconnect_delay)
    except asyncio.CancelledError:
        logger.debug("catch CancelledError during shutdown")
        exit(1)


async def start_connection(
    server_endpoint: str, device_token: str, computer_wmi: wmi.WMI
) -> None:  # noqa: WPS210
    logger.info(f"starting connection to server {server_endpoint}")
    websocket = await websockets.connect(
        server_endpoint, extra_headers={"Authorization": device_token}
    )

    while True:
        p = await websocket.recv()
        event_req = json.loads(p)
        logger.debug(f"event request: {event_req}")
        try:
            request = EventInRequest(**event_req)
        except ValidationError as request_error:
            logger.info(f"bad request: {request_error.json()}")
            continue  # todo error response when backend change events format

        try:
            event_payload: PayloadInResponse = handle_event(
                event_type=request.method, payload=request.params, computer=computer_wmi
            )
        except KeyError:
            event_payload = EventInResponse(
                id=request.id,
                method=request.method,
                error={"detail": "event is not supported"},
            )
        response = EventInResponse(
            id=request.id, method=request.method, result=event_payload
        ).json()
        logger.debug(f"event response: {response}")
        await websocket.send(response)
    await websocket.close()


def run_service(config: Config) -> None:
    loop = asyncio.get_event_loop()
    try:
        task = server_connection_with_retry(config)
        asyncio.run(task)
    finally:
        loop.close()


if __name__ == "__main__":
    import sys

    _, server, device_token, *_ = sys.argv
    server = "wss://api.mirumon.dev/devices/service"
    device_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkZXZpY2UiOnsiaWQiOiIxODBkYTIwMi0xZjQ4LTQ2MTctYmE2Yi04ZThjN2Y3MThjZDkifSwiZXhwIjoxNjMzOTAwNDQ1LCJzdWIiOiJhY2Nlc3MifQ.vO-2kUD9wnZU9g06mf531vYbpSWutqqv86aQNMa8f20"
    config = Config(server=server, device_token=device_token, debug=True)
    run_service(config)
