from redis.asyncio import Redis

REDIS_CLIENT_POOL: Redis


def get_redis_pool() -> Redis:
    global REDIS_CLIENT_POOL
    return REDIS_CLIENT_POOL
