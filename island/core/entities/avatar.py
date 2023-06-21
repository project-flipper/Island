from typing import Set
from island.core.config import BaseEntity
from island.core.realtime.redis import get_redis_pool


class AvatarEntity(BaseEntity):
    @staticmethod
    async def check_color_exists(color_id: int) -> bool:
        colors = AvatarEntity.get_all_colors()
        return color_id in colors

    @staticmethod
    async def get_all_colors() -> Set[int]:
        colors_cache_exists = await AvatarEntity.cache_exists("colors")
        if not colors_cache_exists:
            # TODO: Populate the cache from database
            raise NotImplementedError()

        colors = await AvatarEntity.get_cache("colors", command="smembers")
        return set(map(int, colors))
