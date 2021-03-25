import graphene
from graphene import relay
from graphene_gino import GinoConnectionField, GinoObjectType
from typing import Union

from island.database.schema.user import User
from island.database import db


class UserDataType(GinoObjectType):
    class Meta:
        model = User
        exclude_fields = ("password",)
        interfaces = (relay.Node,)


class UserQuery(graphene.ObjectType):
    node = relay.Node.Field()

    user = graphene.Field(
        UserDataType,
        id=graphene.Int(required=False),
        username=graphene.String(required=False),
    )

    current_user = graphene.Field(UserDataType)

    async def resolve_user(
        ctx, info, id: int = None, username: str = None
    ) -> Union[User, None]:
        """Get user data based on given data.

        Args:
            ctx:
            info:
            id (int, optional): Filter by user id. Defaults to None.
            username (str, optional): Filter by username. Defaults to None.

        Returns:
            Union[User, None]
        """
        query = User.query

        if id is not None:
            query = query.where(User.id == id)
        elif username is not None:
            query = query.where(User.username == username)
        else:
            return None

        return await query.gino.first()

    async def resolve_me(ctx, info) -> Union[User, None]:
        user_data = info.context["request"].scope.get(
            "oauth", {}).get("data", None)

        if user_data is None:
            return None

        username, _ = user_data["sub"].split("#")
        return await User.query.where(User.username == username).gino.first()


UserQuerySchema = graphene.Schema(query=UserQuery)
