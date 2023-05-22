import os
import typing

from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette_babel import LocaleFromHeader, LocaleFromCookie, LocaleMiddleware
from starlette_wtf import CSRFProtectMiddleware

from apps.core.configs import Base

ALLOWED_HOSTS = [host for host in os.getenv('ALLOWED_HOSTS', '')]


def build_middlewares(config: Base) -> typing.List[Middleware]:
    middlewares = [
        Middleware(SessionMiddleware, secret_key=config.SECRET_KEY),
        Middleware(
            CSRFProtectMiddleware,
            csrf_secret=config.SECRET_KEY,
            enabled=not config.TESTING
        ),
        Middleware(
            LocaleMiddleware, locales=['id', 'en_US'], selectors=[
                LocaleFromCookie(),
                LocaleFromHeader(supported_locales=['id', 'en_US']),
            ]
        )
    ]
    if not config.TESTING and not config.DEBUG and len(ALLOWED_HOSTS) > 0:
        middlewares += [
            Middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS),
        ]
    return middlewares
