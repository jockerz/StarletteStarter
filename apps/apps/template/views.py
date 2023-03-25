from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette_login.decorator import login_required

from apps.extensions.template import templates


@login_required
async def auth_required(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('TEMPLATE_FILE.html', context)
