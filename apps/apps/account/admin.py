from apps.core.base.admin import BaseModel
from .models import User


class UserAdmin(BaseModel, model=User):
    icon = "fa-solid fa-user"
    name = 'User'

    # Column on list view
    column_list = [
        User.id, User.username, User.email, User.name,
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
