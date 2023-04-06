from datetime import datetime, timedelta
from authlib.integrations.base_client.errors import MismatchingStateError
from authlib.integrations.starlette_client.apps import StarletteOAuth2App
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette_login.utils import login_user

from apps.apps.account.crud.user import UserCRUD
from apps.core.dependencies import get_user
from apps.extensions.dependencies import get_db, get_oauth2
from apps.utils.notification import Notification
from apps.utils.url import validate_next_url
from .crud import OAuth2AccountCRUD, OAuth2TokenCRUD
from .exceptions import InvalidOAuth2ProviderError, OAuth2MismatchingStateError
from .models import ProviderEnum
from .utils import parse_account_data, parse_user_data

logged_in_notif = Notification(
    icon='success', title='Your are already logged in'
)
login_notif = Notification(
    icon='success', title='Third party authentication complete'
)
register_notif = Notification(
    icon='success', title='Third party registration complete'
)


async def authorize(request):
    db = get_db(request)
    oauth2 = get_oauth2(request)

    provider_name = request.path_params['provider']
    try:
        provider = ProviderEnum(provider_name)
    except ValueError:
        # Invalid OAuth provider
        raise InvalidOAuth2ProviderError

    client: StarletteOAuth2App = oauth2.create_client(provider_name)
    if client is None:
        # Not integrated with the Oauth Provider
        raise InvalidOAuth2ProviderError

    try:
        token = await client.authorize_access_token(request)
    except MismatchingStateError as e:
        raise OAuth2MismatchingStateError

    print(f'{provider}-token: {token}\n')
    resp = await client.get('user', token=token)
    profile = resp.json()
    resp = await client.get('user/public_emails', token=token)
    email = resp.json()

    if provider == ProviderEnum.github:
        provider_uid = profile['id']
    else:
        provider_uid = profile['id']

    account = await OAuth2AccountCRUD.get(db, provider_uid, provider)
    if account is None:
        user_data = parse_user_data(provider, profile, email)
        print(f'user_data: {user_data}\n')
        account_data = parse_account_data(provider, profile)
        print(f'account_data: {account_data}\n')
        # TODO:
        #  - if already authenticated, link account provider to current user
        #  - create user, account, token
        #  - notif password is still random, go to setup

        # if already logged in, link provider account to current user
        user = get_user(request)
        if user is None or not user.is_authenticated:
            # Add new user
            user = await UserCRUD.create(
                db, user_data['username'], user_data['password'],
                user_data.get('email', None), user_data.get('Name', ''),
                is_active=True, commit=False
            )
            db.add(user)
        print(f'user: {user}')
        # Save provider account
        provider_account = await OAuth2AccountCRUD.create(
            db, provider, user, provider_uid, profile, commit=False
        )
        db.add(provider_account)
        print(f'provider_account: {provider_account}')
        # Save OAuth token
        token = await OAuth2TokenCRUD.create(
            db, provider_account, token['access_token'],
            token.get('refresh_token'), token.get(
                'expires_at', datetime.now() + timedelta(days=3)
            ),
        )
        print(f'token: {token}')
        # Registration notification
        register_notif.push(request)
    else:
        user = await UserCRUD.get_by_id(db, account.user_id)
        await OAuth2AccountCRUD.update_last_login(db, account)

    # logging in user
    await login_user(request, user)
    login_notif.push(request)

    next_url = validate_next_url(request.query_params.get('next')) \
               or request.url_for('home')
    return RedirectResponse(next_url, status_code=302)


async def login(request: Request):
    provider_name = request.path_params['provider']
    try:
        provider = ProviderEnum(provider_name)
    except ValueError:
        # Invalid OAuth provider
        raise InvalidOAuth2ProviderError

    user = get_user(request)
    # user is already authenticated
    if user.is_authenticated:
        next_url = validate_next_url(request.query_params.get('next')) \
                   or request.url_for('home')
        logged_in_notif.push(request)
        return RedirectResponse(next_url, status_code=302)

    oauth2 = get_oauth2(request)
    client = oauth2.create_client(provider_name)
    if client is None:
        # return error template
        raise InvalidOAuth2ProviderError

    redirect_uri = request.url_for('oauth2:authorize', provider=provider.value)
    # redirecting to provider authorize_url
    provider_url = await client.authorize_redirect(request, redirect_uri)
    print(dir(provider_url))
    print(f'redirect_uri={redirect_uri}\nprovider_url={provider_url}')
    return provider_url
