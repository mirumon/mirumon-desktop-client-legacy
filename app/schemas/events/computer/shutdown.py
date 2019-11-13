from typing import Optional

from pydantic import BaseModel


class Shutdown(BaseModel):
    shutdown: Optional[str] = "ok"
