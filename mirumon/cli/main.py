import os
import pathlib
import typer
import subprocess
import platform

from mirumon.client.main import run_service

cli = typer.Typer()

if platform.system() == "Windows":
    from mirumon.cli.groups import windows

    cli.add_typer(windows.group)



@cli.command(hidden=True)
def run(
    token: str, server: str, reconnect_delay: int = 10, reconnect_attempts: int = 10
) -> None:
    create_logs_dir()

    message = "\n".join(
        [
            "Start service with current config",
            f"token: {token}",
            f"server: {server}",
            f"reconnect delay: {reconnect_delay}",
            f"reconnect attempts: {reconnect_attempts}",
        ]
    )
    typer.echo(message)
    # run_service()
