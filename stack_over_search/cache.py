from functools import wraps

from aiohttp.web_response import json_response

__all__ = [
    'request_cache',
]


def request_cache(prefix, *args):
    """Simple api response cache decorator."""
    def fetch_args(f):
        @wraps(f)
        async def decorated(self):
            key = f'cache:{prefix}:' \
                f'{":".join(str(getattr(self, arg)) for arg in args)}'

            redis = self.request.app['redis_client']
            data = await redis.get(key)
            if data:
                return json_response(text=data.decode('utf-8'))

            result = await f(self)
            await redis.set(key, result.text, ttl=60)
            return result
        return decorated
    return fetch_args
