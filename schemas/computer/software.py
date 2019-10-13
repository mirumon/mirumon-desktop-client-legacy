from pydantic import Schema

from schemas.computer.base import BaseComponent


class StartupCommandModel(BaseComponent):
    caption: str
    description: str
    user: str
    command: str
    location: str


class EnvironmentModel(BaseComponent):
    name: str
    username: str
    variable_value: str = Schema(..., alias="VariableValue")
    system_variable: bool = Schema(..., alias="SystemVariable")


class InstalledProgramModel(BaseComponent):
    name: str
    vendor: str
    version: str
