from aiohttp.web import View
from aiohttp.web_response import json_response

from stack_over_search.cache import request_cache

__all__ = [
    'RequestsView',
    'ShowAllView',
]

_PAGE_SIZES = {'25', '50', '100'}
_SORT = {None, 'asc', 'desc'}


class RequestsView(View):

    def __init__(self, request):
        super().__init__(request)
        self.page = request.query.get('page', '1')
        self.page_size = request.query.get('page_size', '25')
        self.intitle = request.match_info["intitle"]

        if self.page_size not in _PAGE_SIZES:
            raise ValueError(self.page_size)

    @request_cache('request', 'intitle', 'page_size', 'page')
    async def get(self):
        intitle = self.intitle
        app = self.request.app

        await app['mysql_client'].record_intitle(intitle)
        return json_response(
            await app['stack_client'].request(intitle,
                                              self.page,
                                              self.page_size)
        )


class ShowAllView(View):

    def __init__(self, request):
        super().__init__(request)
        self.sort = request.query.get('sort')
        if self.sort not in _SORT:
            raise ValueError(self.sort)

    @request_cache('showall', 'sort')
    async def get(self):
        return json_response(
            await self.request.app['mysql_client'].select_intitle(self.sort)
        )
