from sqladmin import Admin

from apps.apps.account.admin import UserAdmin


def register_models(admin: Admin):
    admin.add_view(UserAdmin)
