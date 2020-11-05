from fastapi import APIRouter, Request
from starlette.graphql import GraphQLApp
from graphql.execution.executors.asyncio import AsyncioExecutor

from island.models.graphql.world import WorldQuerySchema
from island.core.constants.scope import Scope
from island.utils.auth import require_oauth_scopes

router = APIRouter()
worldQLApp = GraphQLApp(
    schema=WorldQuerySchema,
    executor_class=AsyncioExecutor
)

@router.get("/")
#@router.post("/", dependencies=[require_oauth_scopes(Scope.UserRead)]) # comment this for testing
@router.post("/") # uncomment this for testing
async def handle_user_data_request(request: Request):
    return await worldQLApp.handle_graphql(request=request)
