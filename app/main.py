import json
import os
from pathlib import Path
from typing import Union, Any

import typer
import websockets
import wmi
from loguru import logger
from pydantic import ValidationError

from app import config
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


@logger.catch
async def server_connection_with_retry(
        server_endpoint: str, computer_wmi: wmi.WMI
) -> None:
    try:
        while True:
            try:
                await start_connection(server_endpoint, computer_wmi)
            except (websockets.exceptions.ConnectionClosedError, OSError, RuntimeError):
                logger.debug(
                    f"will try reconnection after {settings.reconnect_delay} seconds"
                )
                await asyncio.sleep(settings.reconnect_delay)
    except asyncio.CancelledError:
        logger.debug("catch CancelledError during shutdown")


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
        server_endpoint: str, computer_wmi: wmi.WMI
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


import asyncio
import signal


class GracefulExit(SystemExit):
    code = 1


def raise_graceful_exit(*args: Any):
    loop.stop()
    logger.info("shutdown service...")
    raise GracefulExit()

loop = asyncio.get_event_loop()


def run_service():
    signal.signal(signal.SIGINT, raise_graceful_exit)
    signal.signal(signal.SIGTERM, raise_graceful_exit)

    try:
        asyncio.run(server_connection_with_retry(
            config.settings.server_websocket_url,
            wmi.WMI(privileges=["Shutdown", "RemoteShutdown"])
        ))
    finally:
        loop.close()

app = typer.Typer()
nssm = "nssm"
service_name = "mirumon"


@app.command()
def run(token: str, server: str, reconnect_delay: int = 10, reconnect_attempts: int = 10):
    pwd = os.getcwd()
    logs_dir = os.path.join(pwd, "logs")
    Path(logs_dir).mkdir(exist_ok=True)
    message = "\n".join([
        "Start service with current config",
        f"token: {token}",
        f"server: {server}",
        f"reconnect delay: {reconnect_delay}",
        f"reconnect attempts: {reconnect_attempts}",
    ]
    )
    typer.echo(message)
    run_service()



@app.command()
def start():
    os.system(f"nssm start {service_name}")


@app.command()
def install(token: str, server: str, reconnect_delay: int = 10, reconnect_attempts: int = 10):
    message = "\n".join([
        "`install`",
        f"token: {token}",
        f"server: {server}",
        f"reconnect delay: {reconnect_delay}",
        f"reconnect attempts: {reconnect_attempts}",
    ]
    )
    typer.echo(message)

    pwd = os.getcwd()
    executable_path = os.path.join(pwd, f"{service_name}.exe")
    logs_dir = os.path.join(pwd, "logs")
    Path(logs_dir).mkdir(exist_ok=True)

    stdout_path = os.path.join(logs_dir, "stdout.log")
    stderr_path = os.path.join(logs_dir, "stderr.log")

    os.system(f"nssm install {service_name} {executable_path}")
    os.system(f"nssm set {service_name} Application {executable_path}")
    os.system(f"nssm set {service_name} AppParameters run {token} {server} --reconnect-delay {reconnect_delay} --reconnect-attempts {reconnect_attempts}")
    os.system(f"nssm set {service_name} AppStdout {stdout_path}")
    os.system(f"nssm set {service_name} AppStderr {stderr_path}")
    os.system(f"nssm set {service_name} AppExit Default Restart")
    os.system(f"nssm set {service_name} AppRestartDelay 0")

    os.system(f"nssm set {service_name} DependOnService MpsSvc")
    os.system(f"nssm set {service_name} DependOnService winmgmt")


@app.command()
def remove():
    os.system(f"nssm remove {service_name} confirm")


@app.command()
def stop():
    os.system(f"nssm stop {service_name}")


@app.command()
def restart():
    os.system(f"nssm restart {service_name}")


if __name__ == "__main__":
    app()
