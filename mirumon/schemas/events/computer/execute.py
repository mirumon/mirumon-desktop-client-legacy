from typing import List

from pydantic import BaseModel


class ExecuteCommand(BaseModel):
    command: str
    args: List[str]

    @property
    def args_str(self) -> str:
        return " ".join(self.args)


class ExecuteResult(BaseModel):
    status: str
