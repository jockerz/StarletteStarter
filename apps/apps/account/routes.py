from starlette.routing import Route

from .views import (
    profile_page,
    profile_settings_page,
    update_photo_page
)


routes = [
    Route("/", profile_page, name='profile', methods=['GET', 'POST']),
    Route("/settings", profile_settings_page, name='profile_settings',
          methods=['GET', 'POST']),
    Route('/photo', update_photo_page, name='update_photo', methods=['POST']),
]
