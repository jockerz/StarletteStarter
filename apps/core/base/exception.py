import logging
import typing

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as _HTTPException

logger = logging.getLogger('uvicorn.error')


class _BaseException(_HTTPException):
    headers: typing.Optional[typing.Mapping[str, str]]
    status_code: int = 500
    detail: str = 'Internal server error'
    log_level: int = logging.DEBUG
    log_data: dict = None

    def __init__(
        self,
        status_code: int = None,
        detail: str = None,
        **kwargs
    ):
        if status_code:
            self.status_code = status_code
        if detail:
            self.detail = detail
        self.log_data = kwargs
        if 'headers' in kwargs:
            self.headers = kwargs['headers']
        else:
            self.headers = None

    @property
    def log_message(self):
        return f'detail={self.detail} data="{self.log_data}"'

    def send_log_message(self):
        if self.log_level == logging.DEBUG:
            logger.debug(self.log_message)
        elif self.log_level == logging.INFO:
            logger.info(self.log_message)
        elif self.log_level == logging.ERROR:
            logger.error(self.log_message)
        elif self.log_level == logging.WARNING:
            logger.warning(self.log_message)
        elif self.log_level == logging.CRITICAL:
            logger.critical(self.log_message)
        else:
            logger.exception(self)


class BaseAPIException(_BaseException):
    error_code: str = 'APIError'
    errors: typing.Optional[typing.List[str]] = None

    def __init__(
        self,
        status_code: int = None,
        message: str = None,
        errors: typing.Optional[typing.List[str]] = None,
        **kwargs
    ):
        super().__init__(status_code, message, **kwargs)
        self.errors = errors

    def as_response(self) -> JSONResponse:
        response = {
            "success": False,
            "message": self.detail,
        }
        if self.errors:
            response["errors"] = self.errors
        return JSONResponse(
            response,
            status_code=self.status_code,
            headers=getattr(self, 'headers', None)
        )


class BaseAppException(_BaseException):
    # Only for status code 301 - 308
    redirect_url: typing.Optional[str]
    title: str = 'Internal server error'

    def __init__(
        self,
        status_code: int = None,
        message: str = None,
        title: str = None,
        **kwargs
    ):
        super().__init__(status_code, message, **kwargs)
        if title:
            self.title = title

    def get_context(self, request: Request) -> dict:
        return {
            'request': request,
            'title': self.title,
            'message': self.detail,
        }
