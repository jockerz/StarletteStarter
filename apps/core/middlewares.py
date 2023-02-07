import typing

from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_wtf import CSRFProtectMiddleware

from apps.core.configs import Base


def build_middlewares(config: Base) -> typing.List[Middleware]:
    return [
        Middleware(SessionMiddleware, secret_key=config.SECRET_KEY),
        Middleware(
            CSRFProtectMiddleware,
            csrf_secret=config.SECRET_KEY,
            enabled=not config.TESTING
        ),
    ]
