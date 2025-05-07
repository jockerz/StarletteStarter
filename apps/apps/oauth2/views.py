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
from .exceptions import InvalidOAuth2ProviderError, EmailDBIntegrityError
from .models import ProviderEnum
from .utils import (
    get_oauth_client,
    get_oauth_token,
    get_provider,
    get_all_accounts,
    get_expires_at,
    parse_user_data,
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
    client = get_oauth_client(oauth2, provider_name)

    # Authorize access token
    token = await get_oauth_token(client, request)

    if provider == ProviderEnum.github:
        resp = await client.get('user', token=token)
        profile = resp.json()
        resp = await client.get('user/public_emails', token=token)
        public_emails = resp.json()
        provider_uid = profile['id']
    elif provider == ProviderEnum.google:
        # Google
        profile = token['userinfo']
        public_emails = {}
        # Docs: https://cloud.google.com/docs/authentication/token-types#id
        provider_uid = profile['sub']
    else:
        raise InvalidOAuth2ProviderError

    user_data = parse_user_data(provider, profile, public_emails)
    username = user_data['username']
    account = await OAuth2AccountCRUD.get_by_username(db, provider, username)
    if account is None:
        # if already logged in, link provider account to current user
        user = get_user(request)
        if user is None or not user.is_authenticated:
            email_addr = user_data.get('email')
            if await UserCRUD.email_is_registered(db, email_addr):
                raise EmailDBIntegrityError(email=email_addr)

            new_username = await UserCRUD.get_unique_username(db, username)
            # Add new user
            user = await UserCRUD.create(
                db, new_username, user_data['password'],
                email_addr, user_data.get('name', ''),
                is_active=True, commit=False
            )
            db.add(user)

        # Save provider account
        provider_account = await OAuth2AccountCRUD.create(
            db, provider, user, provider_uid, username, profile,
            commit=False
        )
        db.add(provider_account)

        # Save OAuth token
        token = await OAuth2TokenCRUD.create(
            db, account=provider_account,
            access_token=token['access_token'],
            refresh_token=token.get('refresh_token'),
            expires_at=get_expires_at(token.get('expires_at'))
        )

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

    redirect_uri = request.url_for('oauth2:authorize', provider=provider.value)
    # redirecting to provider authorize_url
    return await client.authorize_redirect(request, str(redirect_uri))


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
        # DB commit executed here
        await OAuth2TokenCRUD.remove_by_account(db, account.id)
        # remove oauth2 account and tokens
        unlinked_notif.push(request)
    return RedirectResponse(request.url_for('oauth2:linked_accounts'))
