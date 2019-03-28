from asyncio import get_event_loop

from aiohttp.web import run_app

from stack_over_search.data import init_db
from stack_over_search.web_server import create_app


__all__ = [
    'run_webserver',
    'run_init_db',
]

_DUMMY_CONFIG = {
    'redis.dsn': 'redis://localhost:6382',
    'redis.cache_time': 60,
    'mysql.host': 'localhost',
    'mysql.port': 3307,
    'mysql.db': 'db',
    'mysql.user': 'user',
    'mysql.password': 'somepass',
}


def run_webserver():
    app = create_app(_DUMMY_CONFIG)
    run_app(app, host='127.0.0.1', port=8080)


def run_init_db():
    get_event_loop().run_until_complete(
        init_db(_DUMMY_CONFIG)
    )
