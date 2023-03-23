import typing as t
from string import ascii_uppercase
from starlette.config import Config

# Load the `env` file
env_config = Config('.env')


def handle_value_error(
    name: str, default: t.Optional[t.Any] = None,
    cast: type = None, allow_empty: bool = False
) -> t.Any:
    """
    Get an Env variable value

    :param name: variable name
    :param default: default value
    :param cast: type caster
    :param allow_empty: if the variable is found, allow empty string value
    :return: variable value
    """
    try:
        value = env_config(name, cast=cast, default=default)
        if allow_empty:
            return value or default
        else:
            return value
    except ValueError:
        return default


class Base:
    DEBUG = False
    TESTING = False
    SECRET_KEY = env_config("SECRET_KEY")

    # Admin user
    ADMIN_NAME = env_config("ADMIN_USERNAME", default='admin')
    ADMIN_USERNAME = env_config("ADMIN_USERNAME")
    ADMIN_PASSWORD = env_config("ADMIN_PASSWORD")
    ADMIN_EMAIL = env_config("ADMIN_EMAIL")

    # Database
    DATABASE_URL = env_config("DATABASE_URL")

    # Redis
    REDIS_HOST = env_config('REDIS_HOST', default='127.0.0.1') or '127.0.0.1'
    REDIS_PORT = handle_value_error('REDIS_PORT', cast=int, default=6379)
    REDIS_USER = env_config('REDIS_USER')
    REDIS_PASS = env_config('REDIS_PASS')
    # REDIS_DB = handle_value_error('REDIS_DB', cast=int, default=0)
    REDIS_DB_ARQ = handle_value_error('REDIS_DB_ARQ', cast=int, default=0)

    # SMTP
    SMTP_HOST = handle_value_error('SMTP_HOST', cast=str, default='localhost')
    SMTP_PORT = handle_value_error('SMTP_PORT', cast=int, default=25)
    SMTP_USER = env_config('SMTP_USER')
    SMTP_PASS = env_config('SMTP_PASS')
    SMTP_SSL = handle_value_error('SMTP_SSL', cast=bool, default=False)
    SMTP_START_SSL = handle_value_error('SMTP_START_SSL', cast=bool, default=False)

    def dict(self) -> dict:
        result = {}
        for prop_meth in dir(self):
            if prop_meth[0] in ascii_uppercase:
                value = getattr(self, prop_meth)
                result[prop_meth] = value
        return result


class Development(Base):
    """Configuration for development"""
    DEBUG = True


class Production(Base):
    """Live configuration"""
    pass


class Testing(Base):
    """Configuration for testing"""
    DEBUG = True
    TESTING = True
    # DATABASE_URL = 'sqlite+aiosqlite:///:memory:'
    DATABASE_URL = 'sqlite+aiosqlite:///./test.db'

    #
    REDIS_DB_ARQ = 14

    # SMTP:
    SMTP_HOST = 'localhost'
    SMTP_PORT = 1025
    SMTP_SSL = False
    SMTP_START_SSL = False


if env_config('ENV') in ['DEV', 'dev', 'Development']:
    configs = Development()
else:
    configs = Production()
