from asyncio import gather

from aiohttp.web_app import Application
from aiohttp.web_middlewares import middleware
from aiohttp.web_response import json_response

from stack_over_search.api_client import StackClient
from stack_over_search.data import MySQLClient, CacheRedisClient
from stack_over_search.view import RequestsView, ShowAllView


__all__ = [
    'create_app',
]


@middleware
async def _error_middleware(request, handler):
    try:
        return await handler(request)

    except Exception as err:
        return json_response({'error': str(err)})


async def _on_shutdown(app):
    await gather(
        app['stack_client'].close(),
        app['mysql_client'].close(),
        app['redis_client'].close(),
    )


async def create_app(config):
    app = Application(middlewares=[_error_middleware])
    app.router.add_view('/request/{intitle}', RequestsView)
    app.router.add_view('/show_all', ShowAllView)

    app['stack_client'] = StackClient()
    app['mysql_client'] = await MySQLClient.from_config(config)
    app['redis_client'] = await CacheRedisClient.from_config(config)

    app.on_shutdown.append(_on_shutdown)

    return app
