from starlette.routing import Route

from .views import authorize, login


routes = [
    Route('/authorize/{provider}', authorize, name='authorize'),
    Route('/login/{provider}', login, name='login'),
]
