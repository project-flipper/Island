from fastapi import APIRouter, Depends, Request, Response as HTTPResponse, status
from fastapi.responses import JSONResponse
from starlette.endpoints import WebSocketEndpoint

from island.core.constants.scope import Scope
from island.models import Response
from island.utils.auth import require_oauth_scopes

router = APIRouter()


@router.get("/", dependencies=[require_oauth_scopes(Scope.WorldAccess)])
async def get_worlds() -> Response[list]:
    return Response(
        data=[
            {
                "id": 0,
                "name": "Local test",
                "population": 1,
                "buddies": False,
                "safeChat": False,
            }
        ],
        success=True,
    )


@router.websocket_route("/<world_key>")
class WorldEndpoint(WebSocketEndpoint):
    pass
