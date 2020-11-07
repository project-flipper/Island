from island.models.graphql import user
import graphene
from graphene import relay
from graphene_pydantic import PydanticObjectType
from typing import List

from island.core.world import WorldMeta
from island.core.world import WorldMiddleware

class WorldMetaModel(WorldMeta):
    world_key: str
    user_count: int

class WorldDataType(PydanticObjectType):
    population = graphene.Int(required=True, max_count=graphene.Int())

    def resolve_population(ctx, info, max_count: int) -> int:
        return int(ctx.user_count / ctx.capacity) * max_count

    class Meta:
        model = WorldMetaModel
        exclude_fields = ("access_key", "_grant_scopes", "_scopes", "grant_scopes", "scopes")

class WorldQuery(graphene.ObjectType):
    node = relay.Node.Field()

    worlds = graphene.List(WorldDataType)

    async def resolve_worlds(ctx, info) -> List[WorldMetaModel]:
        user_scopes = info.context['request'].scope['oauth'] or {}
        user_scopes = user_scopes.get('scopes', None)

        if user_scopes is None:
            return None
        
        user_scopes = set(user_scopes)

        worlds = list(
            WorldMetaModel(world_key=key, user_count=len(world.clients), **world.meta.dict())
            for key, world in WorldMiddleware.worlds.items()
            if world.meta.scopes.issubset(user_scopes)
        )

        return worlds


WorldQuerySchema = graphene.Schema(query=WorldQuery)
