import os
import pathlib
import typer
import subprocess


NSSM_PATH = "nssm"
SERVICE_NAME = "mirumon"

group = typer.Typer()

from mirumon.cli.helpers import create_logs_dir, current_dir


def nssm_service_setup_commands(
    executable_path: pathlib.Path,
    token: str,
    server: str,
    reconnect_delay: int,
    reconnect_attempts: int,
    stdout_path: pathlib.Path,
    stderr_path: pathlib.Path,
) -> list:
    return [
        [NSSM_PATH, "install", SERVICE_NAME, executable_path],
        [NSSM_PATH, "set", SERVICE_NAME, "Application", executable_path],
        [
            NSSM_PATH,
            "set",
            SERVICE_NAME,
            "AppParamters",
            "run",
            token,
            server,
            "--reconnect-delay",
            reconnect_delay,
            "--reconnect_attempts",
            reconnect_attempts,
        ],
        [NSSM_PATH, "set", SERVICE_NAME, "AppStdout", stdout_path],
        [NSSM_PATH, "set", SERVICE_NAME, "AppStderr", stderr_path],
        [NSSM_PATH, "set", SERVICE_NAME, "AppExit", "Default", "Restart"],
        [NSSM_PATH, "set", SERVICE_NAME, "AppRestartDelay", 0],
        [NSSM_PATH, "set", SERVICE_NAME, "DependOnService", "MpsSvc"],
        [NSSM_PATH, "set", SERVICE_NAME, "DependOnService", "winmgmt"],
    ]


@group.command()
def start() -> None:
    subprocess.call([NSSM_PATH, "start", SERVICE_NAME])


@group.command()
def install(
    token: str, server: str, reconnect_delay: int = 10, reconnect_attempts: int = 10
) -> None:
    message = "\n".join(
        [
            "`install`",
            f"token: {token}",
            f"server: {server}",
            f"reconnect delay: {reconnect_delay}",
            f"reconnect attempts: {reconnect_attempts}",
        ]
    )
    typer.echo(message)
    logs_dir = create_logs_dir()

    executable_path = current_dir() / f"{SERVICE_NAME}.exe"

    stdout_path = logs_dir / "stdout.log"
    stderr_path = logs_dir / "stderr.log"

    nssm_commands = nssm_service_setup_commands(
        executable_path,
        token,
        server,
        reconnect_delay,
        reconnect_attempts,
        stdout_path,
        stderr_path,
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
