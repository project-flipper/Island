from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response as HTTPResponse
from sqlalchemy import func, insert, select
from starlette import status

from island.core.config import MAX_EMAIL_USAGE, SKIP_RECAPTCHA_ON_DEVELOPMENT
from island.core.i18n import _
from island.database import ASYNC_SESSION
from island.database.schema.avatar import AvatarTable
from island.database.schema.user import UserTable
from island.models import Error, Response, RuntimeValidationError
from island.models.create import CreateUser
from island.models.errors.recaptcha import RecaptchaVerificationError
from island.models.user import MyUser, User
from island.utils.auth import (
    get_current_user,
    get_current_user_id,
    get_password_hash,
    require_oauth_scopes,
)
from island.utils.recaptcha import verify_google_recaptcha

router = APIRouter()


@router.put("/")
async def create_user(r: HTTPResponse, create_form: CreateUser) -> Response[int]:
    if (
        (create_form.token is None and SKIP_RECAPTCHA_ON_DEVELOPMENT is not True)
        or (create_form.token is not None and not await verify_google_recaptcha(create_form.token))
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=RecaptchaVerificationError(),
        )

    async with ASYNC_SESSION() as session:
        await session.begin()

        username = create_form.name.strip()
        find_username_query = select(UserTable).where(
            func.lower(UserTable.username) == username.lower()
        )

        if ((await session.execute(find_username_query)).scalar()) is not None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[
                    RuntimeValidationError(
                        input=create_form.name,
                        type="value_error",
                        msg=_("error.username.taken"),
                        loc=["body", "name"],
                        ctx={},
                    )
                ],
            )

        email = create_form.email.strip()
        count_email_usage_query = (
            select(func.count()).select_from(UserTable).where(UserTable.email == email)
        )

        emails = (await session.execute(count_email_usage_query)).scalar()
        if emails is not None and emails > MAX_EMAIL_USAGE:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[
                    RuntimeValidationError(
                        input=create_form.name,
                        type="value_error",
                        msg=_("error.email.max-usage"),
                        loc=["body", "email"],
                        ctx={},
                    )
                ],
            )

        avatar_query = (
            insert(AvatarTable)
            .values(color=create_form.color)
            .returning(AvatarTable.id)
        )
        avatar_id = (await session.execute(avatar_query)).scalar()

        create_user_query = (
            insert(UserTable)
            .values(
                username=username,
                nickname=username,
                email=email,
                password=get_password_hash(create_form.password),
                avatar_id=avatar_id,
            )
            .returning(UserTable.id)
        )
        user_id = (await session.execute(create_user_query)).scalar()

        await session.commit()

        return Response(data=user_id, success=True)


@router.get("/", dependencies=[require_oauth_scopes()])
async def get_my_user(
    user: Annotated[UserTable, Depends(get_current_user)]
) -> Response[MyUser]:
    my_user = await MyUser.from_table(user)
    return Response(data=my_user, success=True)


@router.get("/search", dependencies=[require_oauth_scopes()])
async def get_user_by_name(
    username: str, my_user_id: Annotated[int, Depends(get_current_user_id)]
) -> Response[User | MyUser]:
    user = await UserTable.query_by_username(username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Error(
                error_type="users.query.not_found",
                error_code=404,
                error_description="User not found",
            ),
        )

    if user.id == my_user_id:
        user_model = await MyUser.from_table(user)
    else:
        user_model = await User.from_table(user)

    return Response(data=user_model, success=True)


@router.get("/{user_id}", dependencies=[require_oauth_scopes()])
async def get_user_by_id(
    user_id: int, my_user_id: Annotated[int, Depends(get_current_user_id)]
) -> Response[User | MyUser]:
    user = await UserTable.query_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Error(
                error_type="users.query.not_found",
                error_code=404,
                error_description="User not found",
            ),
        )

    if user.id == my_user_id:
        my_user = await MyUser.from_table(user)
        return Response(data=my_user, success=True)
    else:
        user_model = await User.from_table(user)
        return Response(data=user_model, success=True)
