from sqladmin import Admin

from apps.apps.account.admin import ActivationAdmin, UserAdmin
from apps.apps.oauth2.admin import OAuth2AccountAdmin, OAuth2TokenAdmin


def register_models(admin: Admin):
    admin.add_view(ActivationAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(OAuth2AccountAdmin)
    admin.add_view(OAuth2TokenAdmin)
