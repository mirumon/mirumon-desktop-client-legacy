from typing import Optional

import typer

from mirumon.cli.helpers import create_logs_dir
from mirumon.client.main import run_service
from mirumon.config import Config

group = typer.Typer()

DEFAULT_DELAY = 10
DEFAULT_ATTEMPTS = 10


@group.command()
def run(
    server: str,
    device_token: str,
    reconnect_delay: int = DEFAULT_DELAY,
    reconnect_attempts: int = DEFAULT_ATTEMPTS,
    allow_shutdown: bool = False,
    debug: bool = False,
) -> None:
    create_logs_dir()
    config = Config(
        server=server,
        device_token=device_token,
        reconnect_delay=reconnect_delay,
        reconnect_attempts=reconnect_attempts,
        allow_shutdown=allow_shutdown,
        debug=debug,
    )
    run_service(config)
