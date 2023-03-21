from starlette.requests import Request

from apps.core.base.exception import BaseAppException


class Exc500(BaseAppException):
    status_code = 400


async def error_500(request: Request):
    raise Exc500


async def value_error(request: Request):
    raise ValueError
