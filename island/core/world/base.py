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
    scopes: List[Scope]
    grant_scopes: List[Scope]
    access_key: str

    class Config:
        orm_mode = True

class WorldBase(BaseModel):
    
    meta: WorldMeta
    world_key: str
    clients: Set[int]

    redis: Redis
    redis_key: Optional[str]

    def __init__(self, redis, *, key: str, meta: WorldMeta):        
        super().__init__(world_key = key, meta = meta, clients = set(), redis = redis)
    
    async def setup(self):
        # first check if this world is already running in same broadcast env
        self.redis_key = f"world:{self.meta.id}"
        running_key = await self.redis.hget(self.redis_key, "key")
        if running_key is not None:
            raise RuntimeWarning(f"The server {str(self)} is already running")
        
        data = self.meta.dict(exclude={"scopes", "grant_scopes", "access_key"})
        data['key'] = self.world_key
        data['count'] = 0
        
        await self.redis.hmset_dict(self.redis_key, data)

        logger.info(f"Server {str(self)} setup successfully.")
    
    async def client_connected(self, client_id: int):
        if client_id in self.clients:
            raise ValueError(f"client_id: {client_id} already in the world server.")

        self.clients.add(client_id)
        await self.redis.hset(self.redis_key, "count", len(self.clients))

        logger.debug(f"client_id: {client_id} added to {str(self)}")
    
    async def client_disconnected(self, client_id: int):
        if client_id in self.clients:
            self.clients.remove(client_id)
            await self.redis.hset(self.redis_key, "count", len(self.clients))

            logger.debug(f"client_id: {client_id} removed from {str(self)}")
        
    def __str__(self):
        return f"{self.meta.name}#{self.meta.id}"

    class Config:
        arbitrary_types_allowed = True