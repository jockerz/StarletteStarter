import typing as t

from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from apps.core.configs import Base
from apps.apps.main.views import (
    home_page,
    login_page,
    logout_page,
    register_page,
    activation_page,
    forgot_password_page,
    reset_password_page
)
from apps.apps.errors.views import error_500, value_error

routes = [
    # Static files routes
    Mount('/media', StaticFiles(directory='media'), name='media'),
    Mount('/static', StaticFiles(directory='static'), name='static'),

    # Web APP routes
    Route('/', home_page, name='home'),
    Route('/login', login_page, name='login', methods=["GET", "POST"]),
    Route('/logout', logout_page, name='logout'),
    Route('/register', register_page, name='register',
          methods=["GET", "POST"]),
    Route('/activate/{code}.{secret}', activation_page,
          name='activation'),
    Route('/forgot', forgot_password_page, name='forgot_password',
          methods=['GET', 'POST']),
    Route('/reset/{code}.{secret}', reset_password_page, name='reset_password',
          methods=['GET', 'POST']),
]


def get_routes(config: Base) -> t.List[t.Union[Mount, Route]]:
    if config.DEBUG:
        return routes + [
            Route('/error/500', error_500, name='error_500'),
            Route('/value_error', value_error, name='value_error'),
        ]
    return routes
