from redis.asyncio import Redis

REDIS_CLIENT_POOL: Redis


def get_redis_pool() -> Redis:
    return REDIS_CLIENT_POOL
