from typing import Optional

import strawberry
from pydantic import BaseModel, EmailStr, validator

from island.core.i18n import _
from island.models.graphql.avatar import Avatar


class User(BaseModel):
    id: int
    username: Optional[str]
    nickname: str
    avatar: Avatar


@strawberry.experimental.pydantic.type(model=User, all_fields=True)
class UserType:
    pass


class CreateUserModel(BaseModel):
    name: str
    color: int
    password: str
    email: EmailStr
    color: int
    token: str

    @validator("name")
    def username_alphanum(cls, value: str):
        value = value.strip()
        if not value.isidentifier():
            raise ValueError(_("error.username.alphanum"))

        if not 3 < len(value) < 13:
            raise ValueError(_("error.username.length"))

        return value

    @validator("password")
    def password_strength_check(cls, value: str):
        if not len(value) > 7:
            raise ValueError(_("error.password.length"))

        return value


@strawberry.experimental.pydantic.input(CreateUserModel, all_fields=True)
class CreateUserType:
    pass
