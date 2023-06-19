import redis.asyncio as redis_async
from typing import Callable
from fastapi import FastAPI
from loguru import logger
from island.core.realtime import redis
from island.database import *
from island.core.config import (
    REDIS_HOST,
    REDIS_PASSWORD,
    REDIS_PORT,
    REDIS_SSL_REQUIRED,
)


def create_start_app_handler(app: FastAPI) -> Callable:
    """FastAPI start app event

    Args:
        app (FastAPI)

    Returns:
        Callable
    """

    async def start_app() -> None:
        logger.info("Connecting to database")
        app.state.db_engine = ASYNC_ENGINE
        app.state.db_session = ASYNC_SESSION

        async with ASYNC_ENGINE.begin() as conn:
            logger.info("Database connection successful")

        logger.info("Connecting to redis")
        app.state.redis = redis.REDIS_CLIENT_POOL = redis_async.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=str(REDIS_PASSWORD),
            ssl=REDIS_SSL_REQUIRED,
        )
        await app.state.redis.ping()
        logger.info("Redis connection established")

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
        await app.state.db_engine.dispose()
        logger.info("Disconnected database connection")

        logger.info("Closing redis connection")
        await app.state.redis.close()
        logger.info("Redis connection closed")

    return stop_app
