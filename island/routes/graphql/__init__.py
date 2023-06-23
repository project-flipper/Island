from fastapi import APIRouter
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


router = APIRouter()
router.include_router(get_graphql_routers(graphql))
