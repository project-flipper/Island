from typing import Callable

from fastapi import APIRouter, Request, Response
from fastapi.routing import APIRoute
from loguru import logger
from pydantic import ValidationError
from strawberry import Schema as StrawberrySchema

from island.routes import graphql
from island.utils.routes import get_graphql_routers


class Schema(StrawberrySchema):
    def process_errors(
        self,
        errors: "list[GraphQLError]",
        execution_context: "ExecutionContext" = None,
    ) -> None:
        super().process_errors(errors, execution_context)

        for error in errors:
            if isinstance(error, (ValidationError)) or getattr(error, "original_error"):
                raise getattr(error, "original_error")


class GraphQLAPIRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response: Response = await original_route_handler(request)
            print("hello", response)
            return response

        return custom_route_handler


router = APIRouter(route_class=GraphQLAPIRoute)
router.include_router(get_graphql_routers(graphql))
