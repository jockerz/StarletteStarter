from starlette.requests import Request
from starlette.responses import RedirectResponse

from apps.extensions.template import templates
from apps.core.base.exception import BaseAPIException, BaseAppException


# @app.exception_handler(404)
def handle_not_found(request: Request, exc):
    return templates.TemplateResponse(
        'errors/404.html',
        context={"request": request},
        status_code=404,
    )


def handle_app_exceptions(request: Request, exc: BaseAppException):
    exc.send_log_message()
    if 300 < exc.status_code < 310:
        return RedirectResponse(
            url=exc.redirect_url,
            status_code=exc.status_code,
            headers=getattr(exc, 'headers', None)
        )
    else:
        return templates.TemplateResponse(
            'errors/default.html',
            exc.get_context(request),
            status_code=exc.status_code,
            headers=getattr(exc, 'headers', None),
        )


def handle_api_exceptions(request: Request, exc: BaseAPIException):
    exc.send_log_message()
    return exc.as_response()


def get_error_handlers() -> dict:
    return {
        404: handle_not_found,
        BaseAPIException: handle_api_exceptions,
        BaseAppException: handle_app_exceptions,
    }
