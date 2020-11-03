from typing import Callable

from fastapi import FastAPI
from loguru import logger
import aioredis

from island.database import *
from island.core.world.events import world_setup, world_unset


def create_start_app_handler(app: FastAPI) -> Callable:
    """FastAPI start app event

    Args:
        app (FastAPI)

    Returns:
        Callable
    """
    async def start_app() -> None:
        logger.info("Connecting to database")
        app.state.database = db
        await app.state.database.set_bind(DB_DSN)
        logger.info("Database connection established")

        logger.info("Connecting to redis")
        app.state.redis = await aioredis.create_redis_pool('redis://localhost')
        logger.info("Redis connection established")

        await world_setup(app.state.redis)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    """FastAPI shutdown event

    Args:
        app (FastAPI)

    Returns:
        Callable
    """
    @logger.catch
    async def stop_app() -> None:
        logger.info("Disconnecting from database")
        await app.state.database.pop_bind().close()
        logger.info("Disconnected database connection")

        await world_unset(app.state.redis)

        logger.info("Closing redis connection")
        app.state.redis.close()
        await app.state.redis.wait_closed()
        logger.info("Redis connection closed")

    return stop_app
