from authlib.integrations.starlette_client import OAuth

from apps.core.configs import Base


def create_oauth2(config: Base) -> OAuth:
    oauth2 = OAuth(config)
    for provider, client_id in [
        ('github', 'GITHUB_CLIENT_ID'),
        ('google', 'GOOGLE_CLIENT_ID'),
    ]:
        if config.get(client_id):
            oauth2.register(provider)
    return oauth2
