from loguru import logger
import secrets

from island.core.world import WorldBase, WorldMeta, WorldMiddleware
from island.database import db
from island.database.schema.world import World
from island.core.config import WORLD_ACCESS_KEY


async def world_setup(redis):
    logger.debug(
        f"Fetching world server details. [ACCESS_KEY = {WORLD_ACCESS_KEY}]")
    async with db.transaction():
        world_meta_list = World.query.where(
            World.access_key == WORLD_ACCESS_KEY
        ).gino.iterate()
        async for world_meta in world_meta_list:
            world_meta = WorldMeta.from_orm(world_meta)
            world = WorldBase(redis, key=secrets.token_hex(8), meta=world_meta)

            try:
                await world.setup()
            except RuntimeWarning as e:
                logger.warning(f"Unable to setup world. {str(e)}")
                continue

            WorldMiddleware.worlds[world.world_key] = world
            logger.debug(f"World {str(world)} added to WorldMiddleware")


async def world_unset(redis):
    logger.debug(
        f"Unset and stopping all world servers. [ACCESS_KEY = {WORLD_ACCESS_KEY}]"
    )
    if WorldMiddleware.worlds:
        await redis.delete(*map(lambda x: x.redis_key, WorldMiddleware.worlds.values()))
