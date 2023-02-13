from starlette.routing import Route

from .views import ProfilePage


routes = [
    Route("/", ProfilePage, name='profile', methods=['GET', 'POST']),
]
