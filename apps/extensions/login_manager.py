from starlette.middleware import Middleware
from starlette_login.backends import SessionAuthBackend
from starlette_login.middleware import AuthenticationMiddleware
from starlette_login.login_manager import LoginManager


def create_login_manager(secret_key: str, redirect_to: str = '/login'):
    return LoginManager(redirect_to, secret_key)


def get_middleware(login_manager: LoginManager, login_route: str = 'login'):
    return Middleware(
        AuthenticationMiddleware,
        backend=SessionAuthBackend(login_manager),
        login_manager=login_manager,
        excluded_dirs=['/static', 'favicon.ico', '/media']
    )
