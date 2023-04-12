from apps.core.base.admin import BaseModel
from .models import Activation, User


class ActivationAdmin(BaseModel, model=Activation):
    icon = "fa fa-check"
    name = 'Activation'

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


class UserAdmin(BaseModel, model=User):
    icon = "fa-solid fa-user"
    name = 'User'

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
        User.is_admin
    ]
