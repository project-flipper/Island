from pydantic import BaseModel, EmailStr, validator
import strawberry
from strawberry.types import Info
from island.models.graphql.avatar import Avatar
from island.models.graphql.user import CreateUserModel, CreateUserType, UserType


@strawberry.type
class Query:
    @strawberry.field
    async def ping(self) -> str:
        return "pong"


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create(self, user_data: CreateUserType) -> UserType:
        user = user_data.to_pydantic()
        
        return UserType(
            id=1,
            username="test",
            nickname="test",
            avatar = Avatar(color = 1)
        )

schema = strawberry.Schema(Query, Mutation)