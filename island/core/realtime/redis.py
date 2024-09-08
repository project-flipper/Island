from redis.asyncio import Redis

REDIS_CLIENT_POOL: Redis

def set_redis_pool(redis: Redis) -> None:
    global REDIS_CLIENT_POOL
    REDIS_CLIENT_POOL = redis

def get_redis_pool() -> Redis:
    global REDIS_CLIENT_POOL
    return REDIS_CLIENT_POOL
