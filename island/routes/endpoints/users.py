from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response as HTTPResponse
from sqlalchemy import insert, select, func
from starlette import status

from island.core.config import MAX_EMAIL_USAGE
from island.core.i18n import _
from island.database import ASYNC_SESSION
from island.database.schema.avatar import AvatarTable
from island.database.schema.user import UserTable
from island.models import Error, Response
from island.models.errors.recaptcha import RecaptchaVerificationError
from island.models.user import MyUser, User
from island.models.create import CreateUser, Create
from island.utils.auth import get_current_user, get_current_user_id, require_oauth_scopes, encrypt_email, get_password_hash
from island.utils.recaptcha import verify_google_recaptcha

router = APIRouter()

@router.put("/")
async def create_user(r: HTTPResponse, create_form: CreateUser) -> Response[Create]:
    if not await verify_google_recaptcha(create_form.token):
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=RecaptchaVerificationError(),
            )

    async with ASYNC_SESSION() as session:
        await session.begin()

        username = create_form.name.strip()
        find_username_query = select(UserTable).where(func.lower(UserTable.username) == username.lower())

        if ((await session.execute(find_username_query)).scalar()) is not None:
            raise ValueError(_("error.username.taken"))

        encoded_email = encrypt_email(create_form.email.strip())
        count_email_usage_query = select(func.count()).select_from(UserTable).where(UserTable.email == encoded_email)

        emails = (await session.execute(count_email_usage_query)).scalar()
        if emails is not None and emails > MAX_EMAIL_USAGE:
            raise ValueError(_("error.email.max-usage"))

        avatar_query = insert(AvatarTable).values(color=create_form.color).returning(AvatarTable.id)
        avatar_id = (await session.execute(avatar_query)).scalar()

        create_uesr_query = insert(UserTable).values(
            username=username,
            nickname=username,
            email=encoded_email,
            password=get_password_hash(create_form.password),
            avatar_id=avatar_id
        ).returning(UserTable.id)
        user_id = str((await session.execute(create_uesr_query)).scalar())

        await session.commit()

        return Response(data=Create(user_id=user_id, validation_errors={}), success=True)

@router.get("/@me", dependencies=[require_oauth_scopes()])
async def get_my_user(user: Annotated[UserTable, Depends(get_current_user)]) -> Response[MyUser]:
    my_user = await MyUser.from_orm(user)
    return Response(data=my_user, success=True)

@router.get("/@me/friends", dependencies=[require_oauth_scopes()])
async def get_friends() -> Response[list[User]]:
    return Response(data=[], success=True)

@router.post("/@me/friends", dependencies=[require_oauth_scopes()])
async def add_friends(friend: dict[str, str]) -> HTTPResponse:
    return HTTPResponse(status_code=200)

@router.delete("/@me/friends/{user_id}", dependencies=[require_oauth_scopes()])
async def remove_friend(user_id: str) -> HTTPResponse:
    return HTTPResponse(status_code=200)

@router.get("/{user_id}", dependencies=[require_oauth_scopes()])
async def get_user_by_id(user_id: str, my_user_id: Annotated[str, Depends(get_current_user_id)]) -> Response[User | MyUser]:
    if user_id == my_user_id:
        async with ASYNC_SESSION() as session:
            user_query = (
                select(UserTable)
                .where(UserTable.id == int(user_id))
            )

            user = (await session.execute(user_query)).scalar()

            assert user is not None

            my_user = await MyUser.from_orm(user)
            return Response(data=my_user, success=True)
    else:
        async with ASYNC_SESSION() as session:
            user_query = (
                select(UserTable)
                .where(UserTable.id == int(user_id))
            )

            user = (await session.execute(user_query)).scalar()

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=Error(
                        error_type="users.query.not_found",
                        error_code=404,
                        error_description="User not found",
                    ),
                )

            user_model = await User.from_orm(user)
            return Response(data=user_model, success=True)

@router.get("/{user_id}/avatar")
async def get_user_avatar(user_id: str, size: int, language: str, photo: bool, bypassPlayerSettingCache: bool) -> HTTPResponse:
    async with ASYNC_SESSION() as session:
        user_query = (
            select(UserTable)
            .where(UserTable.id == int(user_id))
        )

        user = (await session.execute(user_query)).scalar()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=Error(
                    error_type="users.query.not_found",
                    error_code=404,
                    error_description="User not found",
                ),
            )

        # TODO: render user avatar for Disney friends
        #avatar = user.avatar
        return HTTPResponse(content=b"", media_type="image/png")

@router.get("/", dependencies=[require_oauth_scopes()])
async def get_user_by_name(username: str, my_user_id: Annotated[str, Depends(get_current_user_id)]) -> Response[User | MyUser]:
    async with ASYNC_SESSION() as session:
        user_query = (
            select(UserTable)
            .where(func.lower(UserTable.nickname) == username.lower())
        )

        user = (await session.execute(user_query)).scalar()

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
            user_model = await MyUser.from_orm(user)
        else:
            user_model = await User.from_orm(user)

        return Response(data=user_model, success=True)
