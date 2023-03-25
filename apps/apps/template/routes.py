from starlette.routing import Route

from .views import auth_required

routes = [
    Route('/change_me', auth_required, name='change_me'),
]
