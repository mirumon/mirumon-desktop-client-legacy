from typing import Optional

from pydantic import BaseModel


class Shutdown(BaseModel):
    status: str
