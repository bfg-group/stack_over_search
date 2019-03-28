from aioredis import create_redis

__all__ = [
    'CacheRedisClient',
]


class CacheRedisClient(object):

    @classmethod
    async def from_config(cls, config):
        return cls(
            await create_redis(config['redis.dsn']),
            config['redis.cache_time'],
        )

    def __init__(self, redis, ttl):
        self._redis = redis
        self._ttl = ttl

    async def close(self):
        self._redis.close()
        await self._redis.wait_closed()

    async def get(self, key):
        return await self._redis.get(key)

    async def set(self, key, value):
        pipe = self._redis.pipeline()
        pipe.set(key, value)
        pipe.expire(key, self._ttl)
        return await pipe.execute()
