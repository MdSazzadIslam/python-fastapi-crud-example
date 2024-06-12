import pytest
import pytest_asyncio
import json
from aioredis import create_redis_pool
from uuid import uuid4


from src.utils.cache import (
    create_redis_connection,
    close_redis_connection,
    get_cache,
    set_cache,
    UUIDEncoder,
)

REDIS_TEST_URL = "redis://localhost:6379"


@pytest_asyncio.fixture
async def redis():
    redis = await create_redis_pool(REDIS_TEST_URL, encoding="utf8")
    yield redis
    redis.close()
    await redis.wait_closed()


@pytest.mark.asyncio
async def test_set_cache(redis):
    key = "test_key"
    value = {
        "id": str(uuid4()),
        "name": "Test Product",
        "description": "Test Description",
    }
    await set_cache(redis, key, value, expire=10)

    cached_value = await redis.get(key)
    assert cached_value is not None
    assert json.loads(cached_value) == value


@pytest.mark.asyncio
async def test_get_cache(redis):
    key = "test_key"
    value = {
        "id": str(uuid4()),
        "name": "Test Product",
        "description": "Test Description",
    }
    await redis.set(key, json.dumps(value, cls=UUIDEncoder))
    await redis.expire(key, 10)

    cached_value = await get_cache(redis, key)
    assert cached_value is not None
    assert cached_value == value


@pytest.mark.asyncio
async def test_cache_miss(redis):
    key = "non_existent_key"
    cached_value = await get_cache(redis, key)
    assert cached_value is None


@pytest.mark.asyncio
async def test_create_and_close_redis_connection():
    redis = await create_redis_connection()
    assert redis is not None
    await close_redis_connection(redis)
