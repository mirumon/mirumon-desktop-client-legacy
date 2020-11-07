import pathlib
import subprocess

import typer

from mirumon.cli.groups.core import DEFAULT_ATTEMPTS, DEFAULT_DELAY
from mirumon.cli.helpers import create_logs_dir, current_dir

current_path = pathlib.Path().absolute()

NSSM_PATH = current_path / "thirdparty" / "nssm.exe"
SERVICE_NAME = "mirumon"

group = typer.Typer()


@group.command()
def start() -> None:
    subprocess.call([NSSM_PATH, "start", SERVICE_NAME])


@group.command()
def install(
    server: str,
    device_token: str,
    reconnect_delay: int = DEFAULT_DELAY,
    reconnect_attempts: int = DEFAULT_ATTEMPTS,
    allow_shutdown: bool = False,
    debug: bool = False,
) -> None:
    logs_dir = create_logs_dir()
    executable_path = current_dir() / f"{SERVICE_NAME}.exe"

    stdout_path = logs_dir / "stdout.log"
    stderr_path = logs_dir / "stderr.log"

    nssm_commands = nssm_service_setup_commands(
        # nssm config
        executable_path=executable_path,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        # client config
        server=server,
        device_token=device_token,
        reconnect_delay=reconnect_delay,
        reconnect_attempts=reconnect_attempts,
        allow_shutdown=allow_shutdown,
        debug=debug,
    )

    for command in nssm_commands:
        subprocess.call(command)


@group.command()
def remove() -> None:
    subprocess.call([NSSM_PATH, "remove", SERVICE_NAME, "confirm"])


@group.command()
def stop() -> None:
    subprocess.call([NSSM_PATH, "stop", SERVICE_NAME])


@group.command()
def restart() -> None:
    subprocess.call([NSSM_PATH, "restart", SERVICE_NAME])


def nssm_service_setup_commands(
    *,
    executable_path: pathlib.Path,
    stdout_path: pathlib.Path,
    stderr_path: pathlib.Path,
    server: str,
    device_token: str,
    reconnect_delay: int,
    reconnect_attempts: int,
    allow_shutdown: bool,
    debug: bool,
) -> list:
    return [
        [NSSM_PATH, "install", SERVICE_NAME, executable_path],
        [NSSM_PATH, "set", SERVICE_NAME, "Application", executable_path],
        [
            NSSM_PATH,
            "set",
            SERVICE_NAME,
            "AppParameters",
            "run",
            str(server),
            str(device_token),
            "--reconnect-delay",
            str(reconnect_delay),
            "--reconnect-attempts",
            str(reconnect_attempts),
            "--allow-shutdown" if allow_shutdown else "--no-allow-shutdown",
            "--debug" if debug else "--no-debug",
        ],
        [NSSM_PATH, "set", SERVICE_NAME, "AppStdout", stdout_path],
        [NSSM_PATH, "set", SERVICE_NAME, "AppStderr", stderr_path],
        [NSSM_PATH, "set", SERVICE_NAME, "AppExit", "Default", "Restart"],
        [NSSM_PATH, "set", SERVICE_NAME, "AppRestartDelay", "0"],
        [NSSM_PATH, "set", SERVICE_NAME, "DependOnService", "MpsSvc"],
        [NSSM_PATH, "set", SERVICE_NAME, "DependOnService", "winmgmt"],
    ]
