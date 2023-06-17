import strawberry
from strawberry.types import Info
from island.models.graphql.user import UserType


@strawberry.type
class Query:
    @strawberry.field
    async def ping(self) -> str:
        return "pong"


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create(self) -> UserType:
        return UserType(
            id=1,
            username="test",
            nickname="test",
        )