from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_scoped_session,
    async_sessionmaker
)
from sqlalchemy.pool import NullPool


def create_db_engine(db_url):
    return create_async_engine(db_url, poolclass=NullPool)


def create_db_session(engine):
    return async_sessionmaker(engine, expire_on_commit=False)


def create_scope_session(db_session: async_sessionmaker):
    return async_scoped_session(db_session, scopefunc=current_task)
