from pydantic import BaseModel
from typing import List, Set, Optional
from loguru import logger
from aioredis import Redis

from island.core.constants.scope import Scope


class WorldMeta(BaseModel):
    id: int
    name: str
    capacity: int
    lang: int
    scopes: Set[Scope]
    grant_scopes: Set[Scope]
    access_key: str

    class Config:
        orm_mode = True


class WorldBase(BaseModel):

    meta: WorldMeta
    world_key: str

    redis: Redis
    redis_key: Optional[str]

    def __init__(self, redis, *, key: str, meta: WorldMeta):
        super().__init__(world_key=key, meta=meta, redis=redis)

    async def setup(self):
        # first check if this world is already running in same broadcast env
        self.redis_key = f"world:{self.meta.id}"
        world_count = await self.redis.scard(self.redis_key)
        if world_count > 0:
            logger.warn(
                f"Server {str(self)} is already running, and has ({world_count}) members in it. Not overriding existing data."
            )
        else:
            logger.debug(f"Server {str(self)} doesn't exist in memory.")

        logger.info(f"Server {str(self)} setup successfully.")

    async def client_connected(self, client_id: int):
        if await self.redis.sismember(self.redis_key, client_id):
            raise ValueError(
                f"client_id: {client_id} already in the world server.")

        await self.redis.redis_key.sadd(client_id)

        logger.debug(f"client_id: {client_id} added to {str(self)}")

    async def client_disconnected(self, client_id: int):
        if await self.redis.srem(self.redis_key, client_id):
            logger.debug(f"client_id: {client_id} removed from {str(self)}")

    def __str__(self):
        return f"{self.meta.name}#{self.meta.id}"

    class Config:
        arbitrary_types_allowed = True
