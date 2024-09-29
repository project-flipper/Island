from typing import Any, overload
from island.core.realtime.redis import get_redis_pool


class BaseEntity:
    __prefix__ = ""

    @classmethod
    def __get_cache_prefix(cls) -> str:
        prefix = (BaseEntity.__prefix__ + ":") if BaseEntity.__prefix__ else ""

        return prefix + cls.__name__ + ":"

    @overload
    @classmethod
    def get_cache_key(cls, keys: str, /) -> str: ...

    @overload
    @classmethod
    def get_cache_key(cls, *keys: str) -> list[str]: ...

    @classmethod
    def get_cache_key(cls, *keys: str) -> list[str] | str:
        if len(keys) == 0:
            raise ValueError("No keys provided")
        else:
            fkey = keys[0]

        prefix = cls.__get_cache_prefix()

        return [prefix + k for k in keys] if len(keys) > 1 else prefix + fkey

    @classmethod
    async def cache_exists(cls, cache_key: str) -> bool:
        raise NotImplementedError

    @classmethod
    async def get_cache(cls, key: str):
        raise NotImplementedError

    @classmethod
    async def set_cache(cls, key: str, value: Any):
        raise NotImplementedError


class Entity(BaseEntity):
    @classmethod
    async def cache_exists(cls, cache_key: str) -> bool:
        key = cls.get_cache_key(cache_key)
        return await get_redis_pool().exists(key)

    @classmethod
    async def execute_cache(cls, key: str, /, *subkeys, command: str):
        key = cls.get_cache_key(key)
        redis = get_redis_pool()

        if not hasattr(redis, command):
            raise ValueError(f"Redis pool has no command: {command}")

        return await getattr(redis, command)(key, *subkeys)

    @classmethod
    async def get_cache(cls, key: str, /, *subkeys, command: str):
        return await cls.execute_cache(key, *subkeys, command=command)

    @classmethod
    async def set_cache(cls, key: str, /, *subkeys, command: str):
        return await cls.execute_cache(key, *subkeys, command=command)


local_cache = {}


class LocalEntity(BaseEntity):
    @classmethod
    async def cache_exists(cls, cache_key: str) -> bool:
        key = cls.get_cache_key(cache_key)
        return key in local_cache

    @classmethod
    async def get_cache(cls, key: str):
        key = cls.get_cache_key(key)
        return local_cache[key]

    @classmethod
    async def set_cache(cls, key: str, value: Any):
        key = cls.get_cache_key(key)
        local_cache[key] = value
