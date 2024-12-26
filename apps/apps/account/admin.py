from sqladmin import Admin

from apps.core.base.admin import BaseModel
from .models import Activation, Reset, EmailUpdate, User


CATEGORY = 'Accounts'


class ActivationAdmin(BaseModel, model=Activation):
    icon = "fa fa-check"
    name = 'Activation'
    name_plural = 'Activations'
    category = CATEGORY

    can_create = False

    # Column on list view
    column_list = [
        Activation.user_id, Activation.code, Activation.target,
        Activation.create_date, Activation.is_complete,
        Activation.expired_date, Activation.refresh_date
    ]

    column_details_exclude_list = [Activation.secret]
    column_searchable_list = [
        Activation.code, Activation.target, Activation.user_id
    ]
    form_excluded_columns = [
        Activation.user, Activation.secret, Activation.create_date,
    ]


class EmailUpdateAdmin(BaseModel, model=EmailUpdate):
    icon = "fa fa-envelope"
    name = 'EmailUpdate'
    name_plural = 'EmailUpdates'
    category = CATEGORY

    can_create = False

    # Column on list view
    column_list = [
        EmailUpdate.user_id, EmailUpdate.code, EmailUpdate.target,
        EmailUpdate.create_date, EmailUpdate.is_complete,
        EmailUpdate.expired_date, EmailUpdate.refresh_date
    ]

    column_details_exclude_list = [EmailUpdate.secret]
    column_searchable_list = [
        EmailUpdate.code, EmailUpdate.target, EmailUpdate.user_id
    ]
    form_excluded_columns = [
        EmailUpdate.user, EmailUpdate.secret, EmailUpdate.create_date,
    ]


class ResetAdmin(BaseModel, model=Reset):
    icon = "fa fa-refresh"
    name = 'Reset'
    category = CATEGORY

    can_create = False

    # Column on list view
    column_list = [
        Reset.user_id, Reset.code, Reset.target,
        Reset.create_date, Reset.is_complete,
        Reset.expired_date, Reset.refresh_date
    ]

    column_details_exclude_list = [Reset.secret]
    column_searchable_list = [
        Reset.code, Reset.target, Reset.user_id
    ]
    form_excluded_columns = [
        Reset.user, Reset.secret, Reset.create_date,
    ]


class UserAdmin(BaseModel, model=User):
    icon = "fa-solid fa-user"
    name = 'User'
    name_plural = 'Users'
    category = CATEGORY

    # Column on list view
    column_list = [
        User.username, User.email, User.name,
        User.is_active, User.is_staff, User.is_admin,
    ]

    # exclude some columns on detail page
    column_details_exclude_list = [User.password]

    # Searchable column on list view
    column_searchable_list = [
        User.username, User.email, User.name,
    ]

    # exclude some columns on edit
    form_excluded_columns = [
        User.password, User.date_joined, User.avatar,
        User.is_admin, User.update_date
    ]


def register_admin_models(admin: Admin):
    admin.add_view(ActivationAdmin)
    admin.add_view(EmailUpdateAdmin)
    admin.add_view(ResetAdmin)
    admin.add_view(UserAdmin)
