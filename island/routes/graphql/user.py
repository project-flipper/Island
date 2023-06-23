from typing import Any

import strawberry
from fastapi import HTTPException, status
from pydantic import ValidationError
from pydantic.error_wrappers import ErrorWrapper

from island.core.entities.avatar import AvatarEntity
from island.core.i18n import _
from island.database import ASYNC_SESSION
from island.database.schema.avatar import AvatarTable
from island.database.schema.user import UserTable
from island.models.errors.recaptcha import RecaptchaVerificationError
from island.models.graphql.avatar import Avatar
from island.models.graphql.user import CreateUserModel, CreateUserType, User, UserType
from island.utils.auth import get_password_hash
from island.utils.recaptcha import verify_google_recaptcha

from . import Schema


@strawberry.type
class Query:
    @strawberry.field
    async def ping(self) -> str:
        return "pong"


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create(self, user_data: CreateUserType) -> UserType:
        create = user_data.to_pydantic()
        if not await verify_google_recaptcha(create.token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=RecaptchaVerificationError(),
            )

        if not await AvatarEntity.check_color_exists(create.color):
            raise ValidationError(
                errors=[ErrorWrapper(ValueError(_("error.color.notexist")), "color")],
                model=CreateUserModel,
            )

        async with ASYNC_SESSION.begin() as session:
            avatar = AvatarTable(color=create.color)
            user = UserTable(
                username=create.name,
                nickname=create.name,
                password=get_password_hash(create.password),
                email=create.email,
                avatar=avatar,
            )

            session.add(avatar)
            session.add(user)

        return UserType.from_pydantic(User.from_orm(user))


schema = Schema(Query, Mutation)
