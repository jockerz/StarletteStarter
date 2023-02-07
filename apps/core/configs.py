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
    ADMIN_USERNAME = env_config("ADMIN_USERNAME")
    ADMIN_PASSWORD = env_config("ADMIN_PASSWORD")
    ADMIN_EMAIL = env_config("ADMIN_EMAIL")

    # Database
    DATABASE_URL = env_config("DATABASE_URL")

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

    REDIS_DB = 14


if env_config('ENV') in ['DEV', 'dev', 'Development']:
    configs = Development()
else:
    configs = Production()
