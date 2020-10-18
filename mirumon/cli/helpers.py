import os
import pathlib


def current_dir() -> pathlib.Path:
    return pathlib.Path(os.getcwd())


def create_logs_dir() -> pathlib.Path:
    logs_dir = current_dir() / "logs"
    logs_dir.mkdir(exist_ok=True)
    return logs_dir
