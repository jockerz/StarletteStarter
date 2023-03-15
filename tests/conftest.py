import asyncio

import pytest
import pytest_asyncio
from async_asgi_testclient import TestClient

from apps.core.configs import Testing
from apps.core.base.db import Base
from apps.extensions.application import create_application
from apps.extensions.db import create_db_engine, create_db_session
from apps.apps.account.crud import UserCRUD

CONFIG = Testing()


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def db_engine():
    engine = create_db_engine(CONFIG.DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine


@pytest_asyncio.fixture(scope='session')
async def db_session_creator(db_engine):
    async with db_engine.connect() as conn:
        yield create_db_session(conn)


@pytest_asyncio.fixture
async def db(db_session_creator):
    return db_session_creator()


@pytest.fixture
async def application(db_session_creator):
    return create_application(
        CONFIG, db_session=db_session_creator,
    )


@pytest_asyncio.fixture
async def http(application):
    async with TestClient(application) as http_:
        return http_


@pytest_asyncio.fixture
async def staff(db):
    u = await UserCRUD.get_by_username(db, 'staff')
    u = u or await UserCRUD.create(
        db, 'staff', 'password', 'staff@test.local', 'Staff',
        is_active=True, is_staff=True
    )
    return u


@pytest_asyncio.fixture
async def admin(db):
    u = await UserCRUD.get_by_username(db, 'admin')
    u = u or await UserCRUD.create(
        db, 'admin', 'password', 'admin@test.local', 'Admin',
        is_active=True, is_admin=True,
    )
    return u


@pytest_asyncio.fixture
async def user(db):
    u = await UserCRUD.get_by_username(db, 'user')
    u = u or await UserCRUD.create(
        db, 'user', 'password', 'user@test.local', 'User',
        is_active=True
    )
    return u


@pytest_asyncio.fixture
async def http_auth(http, user):
    resp = await http.post('/login', form={
        'username': user.username, 'password': 'password'
    })
    assert resp.raise_for_status() is None
    return http


@pytest_asyncio.fixture
async def inactive_user(db):
    u = await UserCRUD.get_by_username(db, 'user')
    u = u or await UserCRUD.create(
        db, 'inactive', 'password', 'inactive@test.local', 'Inactive'
    )
    return u
