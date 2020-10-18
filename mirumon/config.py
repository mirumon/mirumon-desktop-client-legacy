import asyncio
import logging
import signal
from typing import Any

import wmi
from loguru import logger
from pydantic import AnyUrl, BaseModel


class Config(BaseModel):
    server: AnyUrl
    device_token: str
    reconnect_delay: int = 10
    reconnect_attempts: int = 7
    allow_shutdown: bool = False
    debug: bool = False


class GracefulExit(SystemExit):
    code = 1  # noqa: C101


def init_logger(config: Config) -> None:
    level = logging.DEBUG if config.debug else logging.INFO
    logging.basicConfig(level=level)


def init_wmi(config: Config) -> wmi.WMI:
    privileges = ["Shutdown", "RemoteShutdown"] if config.allow_shutdown else []
    return wmi.WMI(privileges=privileges)


def raise_graceful_exit(*_: Any, **__: Any) -> None:
    loop = asyncio.get_event_loop()
    loop.stop()
    logger.info("shutdown service...")
    raise GracefulExit()


def init_signals() -> None:
    signal.signal(signal.SIGINT, raise_graceful_exit)
    signal.signal(signal.SIGTERM, raise_graceful_exit)
