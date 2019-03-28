from aiohttp import ClientSession

__all__ = [
    'StackClient',
]

_API_URL = 'http://api.stackexchange.com/2.2/search'


def _get_params(name, page, pagesize, sort='desc'):
    return {
        'page': page,
        'pagesize': pagesize,
        'order': sort,
        'sort': 'creation',
        'intitle': name,
        'site': 'stackoverflow',
    }


class StackClient(object):
    """
    Client for StackExchange api requests.
    """
    def __init__(self):
        self._session = ClientSession()

    async def close(self):
        await self._session.close()

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *_):
        await self.close()

    async def request(self, name, page, pagesize):
        async with self._session.get(
            _API_URL,
            params=_get_params(name, page, pagesize),
        ) as resp:
            return await resp.json()
