import os
import pathlib
import typer
import subprocess
import platform

from mirumon.cli.groups import core


cli = typer.Typer()

cli.add_typer(core)

if platform.system() == "Windows":
    from mirumon.cli.groups import windows
    cli.add_typer(windows)
