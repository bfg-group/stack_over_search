from contextlib import suppress
from operator import methodcaller

from datetime import datetime

from aiomysql.sa import create_engine
from pymysql import InternalError
from sqlalchemy import select, desc
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.sql.ddl import CreateTable

from stack_over_search.data import RequestsData, AbstractSQLModel

__all__ = [
    'init_db',
    'MySQLClient',
]


async def _create_engine_from_config(config):
    return await create_engine(
        host=config['mysql.host'],
        port=config['mysql.port'],
        db=config['mysql.db'],
        user=config['mysql.user'],
        password=config['mysql.password'],
    )


async def init_db(config):
    """Create all tables in database."""
    sa_engine = await _create_engine_from_config(config)
    try:
        async with sa_engine.acquire() as conn:
            async with conn.begin():
                for table in reversed(AbstractSQLModel.metadata.sorted_tables):
                    with suppress(InternalError):
                        # suppress error for already existed tables
                        await conn.execute(CreateTable(table))
    finally:
        sa_engine.close()
        await sa_engine.wait_closed()


class MySQLClient(object):

    @classmethod
    async def from_config(cls, config):
        return cls(await _create_engine_from_config(config))

    def __init__(self, sa_engine):
        self._sa_engine = sa_engine

    async def close(self):
        self._sa_engine.close()
        await self._sa_engine.wait_closed()

    async def _perform_request(self, query, fetch_method='scalar'):
        async with self._sa_engine.acquire() as conn:
            async with await conn.begin():
                result = await conn.execute(query)
                if result.closed:
                    return
                return await methodcaller(fetch_method)(result)

    async def record_intitle(self, intitle):
        await self._perform_request(
            insert(
                RequestsData
            ).values(
                request=intitle
            ).on_duplicate_key_update(
                request_time=datetime.now()
            )
        )

    async def select_intitle(self, sort):
        query = select([
            RequestsData.request,
            RequestsData.request_time,
        ])
        if sort is not None:
            query = query.order_by(
                desc(RequestsData.request_time)
                if sort == 'desc' else RequestsData.request_time
            )
        return [
            {
                'request': item['request'],
                'request_time': item['request_time'].isoformat(),
            } for item in await self._perform_request(
                query, fetch_method='fetchall',
            )
        ]
