import typing as t

from authlib.integrations.starlette_client import OAuth
from starlette.exceptions import HTTPException

from apps.core.configs import Base

GOOGLE_CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
OAUTH2_PROVIDERS = {
    'github': {
        'api_base_url': 'https://api.github.com',
        'authorize_url': 'https://github.com/login/oauth/authorize',
        'access_token_url': 'https://github.com/login/oauth/access_token'
    },
    # docs:
    #  - https://developers.google.com/identity/sign-in/web/server-side-flow
    #  - dont forget to add scopes on "OAuth consent screen" menu
    # example: https://github.com/authlib/demo-oauth-client/blob/master/starlette-google-login/app.py
    # https://console.cloud.google.com/apis/credentials
    'google': {
        'server_metadata_url': GOOGLE_CONF_URL,
        'client_kwargs': {
            'scope': 'openid profile email',
            'prompt': 'select_account',  # force to select account
        }
    }
}
PROVIDERS = ['github', 'google']


def enabled_providers(config: Base) -> t.List[str]:
    enabled = []
    for provider in PROVIDERS:
        if config.get(provider.upper() + '_CLIENT_ID') \
                and config.get(provider.upper() + '_CLIENT_SECRET'):
            try:
                _ = OAUTH2_PROVIDERS[provider]
                enabled.append(provider)
            except KeyError:
                continue
    return enabled


def create_oauth2(config: Base) -> OAuth:
    oauth2 = OAuth(config)
    for provider in PROVIDERS:
        # check for CLIENT_ID and CLIENT_SECRET for the provided
        if config.get(provider.upper() + '_CLIENT_ID') \
                and config.get(provider.upper() + '_CLIENT_SECRET'):
            try:
                kwargs = OAUTH2_PROVIDERS[provider]
            except KeyError:
                raise HTTPException(
                    404, detail='OAuth Provider is not supported'
                )
            oauth2.register(provider, **kwargs)
    return oauth2
