from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse

from apps.core.dependencies import get_user
from apps.extensions.dependencies import get_oauth2
from apps.extensions.template import templates
from apps.utils.notification import Notification
from apps.utils.url import validate_next_url


logged_in_notif = Notification(
    icon='success', title='Your are already logged in'
)


async def authorize(request):
    provider = request.path_params['provider']
    oauth2 = get_oauth2(request)
    client = oauth2.create_client(provider)
    # TODO: if github is None, return error template
    if client is None:
        return PlainTextResponse(f'authorize[{provider}] - client is None')

    token = await client.authorize_access_token(request)
    print(f'{provider}-token: {token}')

    # TODO: login / register + login

    next_url = validate_next_url(request.query_params.get('next')) \
               or request.url_for('home')
    return RedirectResponse(next_url, status_code=302)


async def login(request: Request):
    user = get_user(request)
    if user.is_authenticated:
        # handle authenticated user
        next_url = validate_next_url(request.query_params.get('next')) \
                   or request.url_for('home')
        logged_in_notif.push(request)
        return RedirectResponse(next_url, status_code=302)

    provider = request.path_params['provider']
    oauth2 = get_oauth2(request)
    print(f'oauth2_clients: {oauth2._clients}')
    print(f'oauth2_registry: {oauth2._registry}')

    from authlib.integrations.starlette_client.apps import StarletteOAuth2App as s
    client: s = oauth2.create_client(provider)
    if client is None:
        # return error template
        return PlainTextResponse(f'login[{provider}] - client is None')

    redirect_uri = request.url_for('oauth2:authorize', provider=provider)
    print(f'redirect_uri: {redirect_uri}')
    return await client.authorize_redirect(request, redirect_uri)
