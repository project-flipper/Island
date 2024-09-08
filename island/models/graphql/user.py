from typing import Optional

import strawberry
from pydantic import BaseModel, EmailStr, validator

from island.core.entities.avatar import AvatarEntity
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
    email: str
    color: int
    token: str

    @validator("name")
    def username_check(cls, value: str):
        value = value.strip()
        if not value.isidentifier():
            raise ValueError(_("error.username.invalid"))

        if not 3 < len(value) < 13:
            raise ValueError(_("error.username.length"))

        return value

    @validator("password")
    def password_strength_check(cls, value: str):
        if not 3 < len(value) < 33:
            raise ValueError(_("error.password.length"))

        return value

    @validator("email")
    def email_valid(cls, value: str):
        try:
            EmailStr.validate(value)
        except ValueError as e:
            raise ValueError(_("error.email.invalid")) from e

        return value


@strawberry.experimental.pydantic.input(CreateUserModel, all_fields=True)
class CreateUserType:
    pass
