from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response as HTTPResponse
from sqlalchemy import select
from starlette import status

from island.database import ASYNC_SESSION
from island.database.schema.user import UserTable
from island.models import Error, Response
from island.models.avatar import Avatar
from island.models.user import MyUser, User
from island.utils.auth import get_current_user, require_oauth_scopes

router = APIRouter()

@router.get("/@me", dependencies=[require_oauth_scopes()])
async def get_my_user(user: Annotated[UserTable, Depends(get_current_user)]) -> Response[MyUser]:
    async with ASYNC_SESSION() as session:
        user = await session.merge(user)

        my_user = MyUser(
            id=str(user.id),
            username=user.username,
            nickname=user.nickname,
            avatar=Avatar.model_validate(user.avatar, from_attributes=True),
            member=None,
            iglooId=0,
            mascotId=None,
            moderator=True,
            stealth=False
        )

    return Response(data=my_user, success=True)

@router.get("/@me/friends", dependencies=[require_oauth_scopes()])
async def get_friends() -> Response[list[User]]:
    return Response(data=[], success=True)

@router.put("/@me/friends", dependencies=[require_oauth_scopes()])
async def add_friends(friend: dict[str, str]) -> HTTPResponse:
    return HTTPResponse(status_code=200)

@router.delete("/@me/friends/{user_id}", dependencies=[require_oauth_scopes()])
async def remove_friend(user_id: str) -> HTTPResponse:
    return HTTPResponse(status_code=200)

@router.get("/{user_id}", dependencies=[require_oauth_scopes()])
async def get_user(user_id: str) -> Response[User]:
    async with ASYNC_SESSION() as session:
        user_query = (
            select(UserTable)
            .where(UserTable.id == user_id)
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

        user_model = User(
            id=str(user.id),
            username=user.username,
            nickname=user.nickname,
            avatar=Avatar.model_validate(user.avatar, from_attributes=True),
            member=None,
            iglooId=0,
            mascotId=None,
            relationship=None,
            publicStampbook=False,
            presence=None
        )

    return Response(data=user_model, success=True)
