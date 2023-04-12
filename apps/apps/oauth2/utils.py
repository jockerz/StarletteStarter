from typing import List, Optional, Union, Sequence
from datetime import datetime, timedelta

from authlib.integrations.base_client.errors import MismatchingStateError
from authlib.integrations.starlette_client.apps import StarletteOAuth2App
from starlette.requests import Request

from apps.utils.datetime import timestamp_to_datetime
from apps.utils.string import gen_random
from .exceptions import InvalidOAuth2ProviderError, OAuth2MismatchingStateError
from .models import ProviderEnum, OAuth2Account


def _parse_github_public_emails(public_emails: Union[dict, List[dict]] = None):
    """Get verified emails"""

    if isinstance(public_emails, dict):
        if 'message' in public_emails:
            raise ValueError(public_emails['message'])
        raise ValueError(f'Invalid email')
    for data in public_emails or []:
        email_data = data.get('email')
        print(f'email_data: {email_data} - {data.get("verified", False)}')
        if not email_data:
            continue
        elif 'noreply.github' in email_data:
            # Github internal email
            continue
        elif data.get('verified', False) is False:
            raise ValueError('Your Auth Provider Email is not verified')
        return email_data


def parse_user_data(
    provider: ProviderEnum, data: dict, public_emails: List[dict] = None
) -> dict:
    """Get user data for us to consume"""

    if provider == ProviderEnum.github:
        username = data['login']
        return {
            'username': username,
            'password': gen_random(),
            'email': data['email'] or _parse_github_public_emails(public_emails),
            'name': data.get('name', username),
        }
    # elif provider == ProviderEnum.google:
    #     raise ValueError('Google is not set up yet')
    else:
        raise ValueError('The third party is not integrated yet')


def parse_account_data(provider: ProviderEnum, data: dict) -> dict:
    if provider == ProviderEnum.github:
        return {
            'provider': provider,
            'uid': data['id'],
            'extra_data': data
        }
    elif provider == ProviderEnum.google:
        raise ValueError('Google is not set up yet')


def get_provider(provider_name: str) -> ProviderEnum:
    try:
        return ProviderEnum(provider_name)
    except ValueError:
        # Invalid OAuth provider
        raise InvalidOAuth2ProviderError


def get_oauth_client(oauth2, provider_name: str) -> StarletteOAuth2App:
    client = oauth2.create_client(provider_name)
    if client is None:
        # Not integrated with the Oauth Provider
        raise InvalidOAuth2ProviderError
    return client


async def get_oauth_token(client: StarletteOAuth2App, request: Request):
    try:
        return await client.authorize_access_token(request)
    except MismatchingStateError:
        raise OAuth2MismatchingStateError


def get_all_accounts(accounts: Sequence[OAuth2Account]):
    unlinked = [
        ProviderEnum.github.value
    ]
    linked = []
    for account in accounts:
        provider = account.provider.value
        if provider in unlinked:
            unlinked.remove(provider)
            linked.append(provider)
    return {'unlinked': unlinked, 'linked': linked}


def get_expires_at(data: Optional[Union[float, int]]) -> datetime:
    if data is None:
        return datetime.utcnow() + timedelta(days=3)
    else:
        return timestamp_to_datetime(data)
