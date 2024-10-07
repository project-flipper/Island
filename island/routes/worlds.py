from fastapi import APIRouter
from sqlalchemy import select

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

    world_models = []
    for w in worlds:
        world = await World.from_table(w, population=0, has_buddies=False)
        world_models.append(world)

    return Response(data=world_models, success=True)

