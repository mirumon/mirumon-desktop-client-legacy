from pydantic import BaseModel


class BaseComponent(BaseModel):
    class Config:  # noqa: WPS431
        orm_mode = True
