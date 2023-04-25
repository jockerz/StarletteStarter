from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette_login.decorator import login_required
from starlette_login.utils import login_user

from apps.apps.account.crud.user import UserCRUD
from apps.core.dependencies import get_user
from apps.extensions.dependencies import get_db, get_oauth2
from apps.extensions.template import templates
from apps.utils.notification import Notification
from apps.utils.url import validate_next_url
from .crud import OAuth2AccountCRUD, OAuth2TokenCRUD
from .exceptions import InvalidOAuth2ProviderError
from .models import ProviderEnum
from .utils import (
    parse_account_data,
    parse_user_data,
    get_oauth_client,
    get_oauth_token,
    get_provider,
    get_all_accounts,
    get_expires_at,
)

logged_in_notif = Notification(
    icon='success', title='Your are already logged in'
)
login_notif = Notification(
    icon='success', title='Third party authentication complete'
)
register_notif = Notification(
    icon='success', title='Third party registration complete'
)
link_success_notif = Notification(
    icon='success', title='Third party account is linked'
)
linked_error_notif = Notification(
    icon='error', title='The third party account has already been linked'
)
unlinked_notif = Notification(
    icon='success', title='The third party account has already been unlinked'
)
unlinked_error_notif = Notification(icon='error', title='Invalid third party')


async def authorize(request):
    db = get_db(request)
    oauth2 = get_oauth2(request)

    provider_name = request.path_params['provider']

    provider = get_provider(provider_name)
    print(f'provider: {provider}')
    client = get_oauth_client(oauth2, provider_name)
    # Authorize access token
    token = await get_oauth_token(client, request)
    print(f'{provider}-token: {token}\n')

    resp = await client.get('user', token=token)
    profile = resp.json()
    print(f'profile: {profile}')
    if provider == ProviderEnum.github:
        resp = await client.get('user/public_emails', token=token)
        public_emails = resp.json()
    else:
        public_emails = {}
    print(f'public_emails: {public_emails}')

    if provider == ProviderEnum.github:
        provider_uid = profile['id']
    else:
        provider_uid = profile['id']

    account = await OAuth2AccountCRUD.get(db, provider_uid, provider)
    if account is None:
        user_data = parse_user_data(provider, profile, public_emails)
        print(f'user_data: {user_data}\n')
        account_data = parse_account_data(provider, profile)
        print(f'account_data: {account_data}\n')

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
            db, provider, user, provider_uid, user_data['username'], profile,
            commit=False
        )
        db.add(provider_account)
        print(f'provider_account: {provider_account}')

        # Save OAuth token
        token = await OAuth2TokenCRUD.create(
            db, account=provider_account,
            access_token=token['access_token'],
            refresh_token=token.get('refresh_token'),
            expires_at=get_expires_at(token.get('expires_at'))
        )
        print(f'token: {token}')
        if user and user.is_authenticated:
            # User is already authenticated, 3party account is linked
            link_success_notif.push(request)
            next_url = validate_next_url(request.query_params.get('next')) \
                       or request.url_for('oauth2:linked_accounts')
            return RedirectResponse(next_url, status_code=302)
        else:
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
    # print(f'redirect_uri: {redirect_uri}')
    # redirecting to provider authorize_url
    return await client.authorize_redirect(request, redirect_uri)


@login_required
async def linked_accounts(request: Request):
    db = get_db(request)
    user = get_user(request)
    accounts = await OAuth2AccountCRUD.get_user_accounts(db, user.id)
    context = {'request': request}
    context.update(get_all_accounts(accounts))
    return templates.TemplateResponse(
        'oauth2/link_social_account.html', context=context
    )


@login_required
async def link_account(request: Request):
    """Link 3party account to current user"""

    provider_name = request.path_params['provider']
    # validate provider
    provider = get_provider(provider_name)

    oauth2 = get_oauth2(request)
    client = oauth2.create_client(provider_name)
    if client is None:
        # return error template
        raise InvalidOAuth2ProviderError

    # check account
    db = get_db(request)
    user = get_user(request)
    account = await OAuth2AccountCRUD.get_by_user_id(db, user.id, provider)
    if account is not None:
        linked_error_notif.push(request)
        return RedirectResponse(request.url_for('oauth2:linked_accounts'))

    redirect_uri = request.url_for('oauth2:authorize', provider=provider_name)
    # redirecting to provider authorize_url
    return await client.authorize_redirect(request, redirect_uri)


@login_required
async def unlink_account(request: Request):
    """Unlink the third party account from current user"""

    provider_name = request.path_params['provider']
    # validate provider
    provider = get_provider(provider_name)

    db = get_db(request)
    user = get_user(request)
    account = await OAuth2AccountCRUD.get_by_user_id(db, user.id, provider)
    if account is None:
        unlinked_error_notif.push(request)
    else:
        await OAuth2AccountCRUD.remove(db, account, commit=False)
        await OAuth2TokenCRUD.remove_by_account(db, account.id)
        # remove oauth2 account and tokens
        unlinked_notif.push(request)
    return RedirectResponse(request.url_for('oauth2:linked_accounts'))
