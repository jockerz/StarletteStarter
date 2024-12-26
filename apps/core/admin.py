from sqladmin import Admin

from apps.apps.account import admin as account_admin
from apps.apps.oauth2 import admin as oauth2_admin


def register_models(admin: Admin):
    account_admin.register_admin_models(admin)
    oauth2_admin.register_admin_models(admin)
