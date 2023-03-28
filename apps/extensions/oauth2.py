from authlib.integrations.starlette_client import OAuth
from starlette.exceptions import HTTPException

from apps.core.configs import Base


OAUTH2_PROVIDERS = {
    'github': {
        'client_kwargs': {'scope': 'user user:email'},
        'api_base_url': 'https://api.github.com',
        'authorize_url': 'https://github.com/login/oauth/authorize',
        'access_token_url': 'https://github.com/login/oauth/access_token'
    }
}


def create_oauth2(config: Base) -> OAuth:
    oauth2 = OAuth(config)
    for provider in ['github', 'google']:
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
