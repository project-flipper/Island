from fastapi import APIRouter, HTTPException
from fastapi import Response as HTTPResponse
from fastapi import status

from island.database.schema.user import UserTable
from island.models import Error

router = APIRouter()


@router.get("/")
async def get_my_user_avatar(user_id: int, size: int, photo: bool) -> HTTPResponse:
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

    # TODO: render user avatar for Disney friends
    # avatar = user.avatar
    return HTTPResponse(content=b"", media_type="image/png")


@router.get("/{user_id}")
async def get_user_avatar(user_id: int, size: int, photo: bool) -> HTTPResponse:
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

    # TODO: render user avatar for Disney friends
    # avatar = user.avatar
    return HTTPResponse(content=b"", media_type="image/png")
