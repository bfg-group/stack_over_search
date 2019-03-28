from sqlalchemy import Column, String, Integer, DateTime, func, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base, declared_attr

__all__ = [
    'AbstractSQLModel',
    'Requests',
    'RequestsData'
]


class AbstractSQLModel(declarative_base(name='DeclarativeBase')):
    __abstract__ = True
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
    }
    request = Column(String(100), nullable=False, unique=True)

    @declared_attr
    def id(cls):
        return Column(
            Integer,
            primary_key=True,
            autoincrement=True,
        )


class Requests(AbstractSQLModel):
    __tablename__ = 'requests'

    link = Column(String(200), nullable=False)
    author = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)

    last_activity = Column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False,
    )
    create_date = Column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False,
    )


class RequestsData(AbstractSQLModel):
    __tablename__ = 'requests_data'

    request_time = Column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False,
    )

