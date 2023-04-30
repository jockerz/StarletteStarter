from starlette.requests import Request
from starlette.routing import Route

from apps.core.base.exception import BaseAppException


class Err400(BaseAppException):
    status_code = 400


class Err302(BaseAppException):
    status_code = 302
    redirect_url = '/redirected'


async def err400(request: Request):
    raise Err400


async def err302(request: Request):
    raise Err302


class TestNotFound:
    async def test_not_found(self, http):
        resp = await http.get('/should_404')
        assert resp.status_code == 404


class TestHandleAPPExceptions:
    async def test_test_400(self, application, http):
        application.router.routes.append(Route('/err400', err400))
        resp = await http.get('/err400')
        assert resp.status_code == 400

    async def test_test_302(self, application, http):
        application.router.routes.append(Route('/err302', err302))
        resp = await http.get('/err302', allow_redirects=False)
        assert resp.status_code == 302
