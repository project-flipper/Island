from fastapi import APIRouter
from sqlalchemy import func, select
from starlette.endpoints import WebSocketEndpoint

from island.core.constants.scope import Scope
from island.database import ASYNC_SESSION
from island.database.schema.world import WorldTable
from island.models import Response
from island.models.world import World
from island.utils.auth import require_oauth_scopes

router = APIRouter()


@router.get("/", dependencies=[require_oauth_scopes(Scope.WorldAccess)])
async def get_worlds(lang: int) -> Response[list[World]]:
    async with ASYNC_SESSION() as session:
        world_query = select(WorldTable).where(WorldTable.lang.op("&")(lang) == lang)
        worlds = (await session.execute(world_query)).scalars()

    return Response(data=[await World.from_orm(w) for w in worlds], success=True)


@router.websocket_route("/<world_key>")
class WorldEndpoint(WebSocketEndpoint):
    pass
