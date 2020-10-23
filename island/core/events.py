from typing import Callable

from fastapi import FastAPI
from loguru import logger
import aioredis

from island.database import *
from island.core.config import DATABASE_URL


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        logger.info("Connecting to database")
        app.state.database = db
        await app.state.database.set_bind(DB_DSN,
            echo=DB_ECHO,
            ssl=DB_SSL
        )
        logger.info("Database connection established")

        logger.info("Connecting to redis")
        app.state.redis = await aioredis.create_redis_pool('redis://localhost')
        logger.info("Redis connection established")

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    @logger.catch
    async def stop_app() -> None:
        logger.info("Disconnecting from database")
        await app.state.database.pop_bind().close()
        logger.info("Disconnected database connection")

        logger.info("Closing redis connection")
        app.state.redis.close()
        await app.state.redis.wait_closed()
        logger.info("Redis connection closed")

    return stop_app