import typing

from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.applications import Starlette
from starlette.middleware import Middleware


def create_admin(
    app: Starlette, engine: AsyncEngine, middlewares: typing.List[Middleware],
    debug: bool = False
) -> Admin:
    return Admin(
        app, engine, middlewares=middlewares, debug=debug,
        title='Admin',
    )
