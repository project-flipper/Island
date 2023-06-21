from typing import Optional
from pydantic import BaseModel, EmailStr, validator
import strawberry

from island.models.graphql.avatar import Avatar
from island.core.i18n import _


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

    @validator("name")
    def username_alphanum(cls, value: str):
        value = value.strip()
        if not value.isidentifier():
            raise ValueError(_("error.username.alphanum"))

        return value

    @validator("password")
    def password_strength_check(cls, value: str):
        if not len(value) > 7:
            raise ValueError(_("error.password.lngth"))

        return value


@strawberry.experimental.pydantic.input(CreateUserModel, all_fields=True)
class CreateUserType:
    pass
