from typing import Optional
from pydantic import BaseModel, EmailStr, validator
import strawberry

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

    @validator('name')
    def username_alphanum(cls, value: str):
        value = value.strip()
        if not value.isidentifier():
            raise ValueError("name can only contain alphabets, numbers, space and a dash (_)")

        return value

    @validator('password')
    def password_strength_check(cls, value: str):
        if not len(value) > 7:
            raise ValueError("password must be a minimum of 8 characters long") #TODO: implement i18n for these strings

        return value

@strawberry.experimental.pydantic.input(CreateUserModel, all_fields=True)
class CreateUserType:
    pass
