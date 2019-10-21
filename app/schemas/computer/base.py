from pydantic import BaseModel


class BaseComponent(BaseModel):
    class Config:
        orm_mode = True
