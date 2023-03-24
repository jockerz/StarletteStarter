from sqladmin import Admin

from apps.apps.account.admin import ActivationAdmin, UserAdmin


def register_models(admin: Admin):
    admin.add_view(ActivationAdmin)
    admin.add_view(UserAdmin)
