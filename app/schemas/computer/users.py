from typing import List

from pydantic import Schema

from app.schemas.computer.base import BaseComponent


class GroupModel(BaseComponent):
    status: str
    caption: str
    description: str
    domain: str
    name: str
    local_account: bool = Schema(..., alias="LocalAccount")

    def __str__(self):
        return self.name


class UserAccountModel(BaseComponent):
    status: str
    name: str
    fullname: str
    domain: str
    disabled: bool
    local_account: bool = Schema(..., alias="LocalAccount")
    lockout: bool
    groups: List[GroupModel] = []
    password_changeable: str = Schema(..., alias="PasswordChangeable")
    password_expires: str = Schema(..., alias="PasswordExpires")
    password_required: str = Schema(..., alias="PasswordRequired")
