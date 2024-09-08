from contextlib import asynccontextmanager
from typing import Callable

import redis.asyncio as redis_async
from fastapi import FastAPI
from loguru import logger

from island.core.config import (
    REDIS_HOST,
    REDIS_PASSWORD,
    REDIS_PORT,
    REDIS_SSL_REQUIRED,
)
from island.core.constants.events import EventEnum
from island.core.realtime import redis
from island.database import *
from island.events import dispatch


@asynccontextmanager
async def manage_app_lifespan(app: FastAPI):
    """FastAPI app lifespan manager

    Args:
        app (FastAPI)
    """

    logger.info("Connecting to database")
    app.state.db_engine = ASYNC_ENGINE
    app.state.db_session = ASYNC_SESSION

    async with ASYNC_ENGINE.begin() as conn:
        logger.info("Database connection successful")

    logger.info("Connecting to redis")
    app.state.redis = redis.REDIS_CLIENT_POOL = redis_async.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=str(REDIS_PASSWORD) if REDIS_PASSWORD is not None else REDIS_PASSWORD,
        ssl=REDIS_SSL_REQUIRED,
    )
    await app.state.redis.ping()
    logger.info("Redis connection established")

    logger.info("Dispatching APP_START_EVENT")
    dispatch(EventEnum.APP_START_EVENT)

    yield

    logger.info("Disconnecting from database")
    await app.state.db_engine.dispose()
    logger.info("Disconnected database connection")

    logger.info("Closing redis connection")
    await app.state.redis.close()
    logger.info("Redis connection closed")

    logger.info("Dispatching APP_STOP_EVENT")
    dispatch(EventEnum.APP_STOP_EVENT)
