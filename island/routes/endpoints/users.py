from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response as HTTPResponse
from sqlalchemy import select, func
from starlette import status

from island.database import ASYNC_SESSION
from island.database.schema.user import UserTable
from island.models import Error, Response
from island.models.user import MyUser, User
from island.utils.auth import get_current_user, get_current_user_id, require_oauth_scopes

router = APIRouter()

@router.get("/@me", dependencies=[require_oauth_scopes()])
async def get_my_user(user: Annotated[UserTable, Depends(get_current_user)]) -> Response[MyUser]:
    my_user = await MyUser.from_user_table(user)
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
async def get_user_by_id(user_id: str, my_user_id: Annotated[str, Depends(get_current_user_id)]) -> Response[User | MyUser]:
    if user_id == my_user_id:
        async with ASYNC_SESSION() as session:
            user_query = (
                select(UserTable)
                .where(UserTable.id == int(user_id))
            )

            user = (await session.execute(user_query)).scalar()

            assert user is not None

            my_user = await MyUser.from_user_table(user)
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

            user_model = await User.from_user_table(user)
            return Response(data=user_model, success=True)

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
            user_model = await MyUser.from_user_table(user)
        else:
            user_model = await User.from_user_table(user)

        return Response(data=user_model, success=True)
