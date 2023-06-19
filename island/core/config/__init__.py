from typing import List, Union
from unittest.mock import Base

from island.core.realtime.redis import get_redis_pool


class BaseConfig:
    __prefix__ = ""

    @classmethod
    def __get_cache_prefix(cls) -> str:
        prefix = (BaseConfig.__prefix__ + ":") if BaseConfig.__prefix__ else ""

        return prefix + cls.__name__ + ":"

    @classmethod
    def get_cache_key(cls, *keys: List[str]) -> Union[List[str], str]:
        if not keys:
            raise ValueError("No keys provided")

        prefix = cls.__get_cache_prefix()

        return [prefix + k for k in keys] if len(keys) > 1 else prefix + keys[0]

    @classmethod
    async def cache_exists(cls, cache_key: str) -> bool:
        key = cls.get_cache_key(cache_key)
        return await get_redis_pool().exists(key)

    @classmethod
    async def get_cache(cls, key, /, *subkeys, command):
        key = cls.get_cache_key(key)
        redis = get_redis_pool()

        if not hasattr(redis, command):
            raise ValueError(f"Redis pool has no command: {command}")

        return await getattr(redis, command)(key, *subkeys)
