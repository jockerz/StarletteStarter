from arq import ArqRedis
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession


def get_arq(request: Request) -> ArqRedis:
    return request.app.state.arq


def get_config(request: Request):
    return request.app.state.config


def get_db(request: Request) -> AsyncSession:
    return request.state.db


def get_oauth2(request: Request) -> OAuth:
    return request.app.state.oauth2
