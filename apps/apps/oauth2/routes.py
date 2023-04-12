from starlette.routing import Route

from .views import (
    authorize,
    login,
    linked_accounts,
    link_account,
    unlink_account,
)


routes = [
    Route('/authorize/{provider}', authorize, name='authorize'),
    Route('/login/{provider}', login, name='login'),
    Route('/link_account/{provider}', link_account, name='link_account'),
    Route('/link_account', linked_accounts, name='linked_accounts'),
    Route('/unlink_account/{provider}', unlink_account, name='unlink_account'),
]
