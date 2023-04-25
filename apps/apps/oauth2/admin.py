from apps.core.base.admin import BaseModel

from .models import OAuth2Account, OAuth2Token


class OAuth2AccountAdmin(BaseModel, model=OAuth2Account):
    icon = "fa fa-link"
    name = 'Social Account'

    column_list = [
        OAuth2Account.provider,
        OAuth2Account.username,
        OAuth2Account.uid,
        OAuth2Account.last_login,
        OAuth2Account.date_joined,
    ]
    form_excluded_columns = [
        OAuth2Account.id,
        OAuth2Account.provider,
        OAuth2Account.username,
        OAuth2Account.uid,
        OAuth2Account.user,
        OAuth2Account.extra_data
    ]


class OAuth2TokenAdmin(BaseModel, model=OAuth2Token):
    icon = "fa fa-universal-access"
    name = 'Social Token'

    column_list = [
        OAuth2Token.account,
        OAuth2Token.user,
        OAuth2Token.expires_at,
        OAuth2Token.created_at
    ]
    form_excluded_columns = [
        OAuth2Token.id,
        OAuth2Token.user,
        OAuth2Token.account,
        OAuth2Token.account_id,
        OAuth2Token.created_at,
        OAuth2Token.access_token,
        OAuth2Token.refresh_token,
    ]
