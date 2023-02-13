from starlette.requests import Request
from starlette.endpoints import HTTPEndpoint
from starlette_login.decorator import login_required

from apps.extensions.template import templates


class ProfilePage(HTTPEndpoint):
    template = 'account/profile.html'

    @login_required
    async def get(self, request: Request):
        context = {'request': request}
        return templates.TemplateResponse(self.template, context)
