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
        interfaces = (relay.Node, )

class UserQuery(graphene.ObjectType):
    node = relay.Node.Field()

    user = graphene.Field(
        UserDataType,
        id = graphene.Int(required=False),
        username = graphene.String(required=False)
    )
    
    current_user = graphene.Field(
        UserDataType
    )

    async def resolve_user(ctx, info, id:int=None, username:str=None) -> Union[User, None]:
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
        print(str(query))
        if id is not None:
            query = query.where(User.id == id)

        if username is not None:
            query = query.where(User.username == username)

        if id is None and username is None:
            return None

        return await query.gino.first()


UserQuerySchema = graphene.Schema(query=UserQuery)
