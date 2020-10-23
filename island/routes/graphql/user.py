from fastapi import APIRouter, Request
from starlette.graphql import GraphQLApp
from graphql.execution.executors.asyncio import AsyncioExecutor

from island.models.graphql.user import UserQuerySchema

router = APIRouter()
userQLApp = GraphQLApp(
    schema = UserQuerySchema,
    executor_class = AsyncioExecutor
)

@router.get("/")
@router.post("/")
async def handle_user_data_request(request: Request):

    return await userQLApp.handle_graphql(request=request)
