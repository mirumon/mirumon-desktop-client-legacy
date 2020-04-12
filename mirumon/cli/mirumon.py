import platform

import typer

from mirumon.cli.groups import core

cli = typer.Typer()

cli.registered_commands = core.group.registered_commands

if platform.system() == "Windows":
    from mirumon.cli.groups import windows

    cli.registered_commands.extend(windows.group.registered_commands)

if __name__ == "__main__":
    cli()
