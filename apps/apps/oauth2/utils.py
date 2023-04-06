from typing import List, Union
from .models import ProviderEnum

from apps.utils.string import gen_random


def _parse_github_email(email: Union[dict, List[dict]] = None):
    if isinstance(email, dict):
        if 'message' in email:
            raise ValueError(email['message'])
        raise ValueError(f'Invalid email')
    for e in email or []:
        email_data = e.get('email')
        if not email_data or 'noreply.github' in email_data:
            continue
        if e.get('verified', False):
            raise ValueError('Your Auth Provider Email is not verified')
        return email_data


def parse_user_data(
    provider: ProviderEnum, data: dict, email: List[dict] = None
) -> dict:
    if provider == ProviderEnum.github:
        username = data['login']
        return {
            'username': username,
            'password': gen_random(),
            'email': data['email'] or _parse_github_email(email),
            'name': data.get('name', username),
        }
    elif provider == ProviderEnum.google:
        raise ValueError('Google is not set up yet')


def parse_account_data(provider: ProviderEnum, data: dict) -> dict:
    if provider == ProviderEnum.github:
        return {
            'provider': provider,
            'uid': data['id'],
            'extra_data': data
        }
    elif provider == ProviderEnum.google:
        raise ValueError('Google is not set up yet')
