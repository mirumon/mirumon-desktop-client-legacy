from pydantic import BaseModel


def to_camel(string: str) -> str:
    return "".join(word.capitalize() for word in string.split("_"))


class BaseModelWMI(BaseModel):
    class Config:  # noqa: WPS431
        orm_mode = True
        alias_generator = to_camel
