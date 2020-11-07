from pydantic import BaseModel


class Shutdown(BaseModel):
    status: str
