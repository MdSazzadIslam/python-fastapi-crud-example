import logging
import json
from aioredis import Redis, create_redis_pool
from typing import Optional, Any
from uuid import UUID

logging.basicConfig(level=logging.info)
logger = logging.getLogger(__name__)

REDIS_URL = "redis://localhost:6379"


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)


async def create_redis_connection() -> Optional[Redis]:
    try:
        redis = await create_redis_pool(REDIS_URL, encoding="utf8")
        return redis
    except Exception as e:
        logger.error(f"Failed to connect Redis: {e}")
        return None


async def close_redis_connection(redis: Redis):
    if redis:
        redis.close()
        await redis.wait_closed()
        logger.info("Disconnected from Redis")


def get_redis_instance(redis: Optional[Redis] = None) -> Redis:
    if redis is None:
        raise ValueError("Redis instance is not provided")
    return redis


async def get_cache(redis: Redis, key: str):
    cached_value = await redis.get(key)
    if cached_value:
        return json.loads(cached_value)
    return None


async def set_cache(redis: Redis, key: str, value, expire: int = 300):
    await redis.set(key, json.dumps(value, cls=UUIDEncoder))
    await redis.expire(key, expire)
