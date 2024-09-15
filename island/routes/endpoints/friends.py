from fastapi import APIRouter
from fastapi import Response as HTTPResponse

from island.models import Response
from island.models.user import User
from island.utils.auth import require_oauth_scopes

router = APIRouter()


@router.get("/", dependencies=[require_oauth_scopes()])
async def get_friends() -> Response[list[User]]:
    return Response(data=[], success=True)


@router.put("/", dependencies=[require_oauth_scopes()])
async def add_friends(friend: dict[str, str]) -> HTTPResponse:
    return HTTPResponse(status_code=200)


@router.delete("/{user_id}", dependencies=[require_oauth_scopes()])
async def remove_friend(user_id: str) -> HTTPResponse:
    return HTTPResponse(status_code=200)
