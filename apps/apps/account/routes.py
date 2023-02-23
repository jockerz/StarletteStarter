from starlette.routing import Route

from .views import (
    email_settings_page,
    email_update_page,
    profile_page,
    profile_settings_page,
    update_password_page,
    update_photo_page,
)


routes = [
    Route("/", profile_page, name='profile', methods=['GET', 'POST']),
    Route('/photo', update_photo_page, name='update_photo', methods=['POST']),
    Route("/password", update_password_page, name='update_password',
          methods=['GET', 'POST']),
    Route("/settings/email", email_settings_page, name='email_settings',
          methods=['GET', 'POST']),
    Route("/settings/email_update/{code}.{secret}", email_update_page,
          name='email_update'),
    Route("/settings", profile_settings_page, name='profile_settings',
          methods=['GET', 'POST']),
]
