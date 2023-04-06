from apps.core.base.admin import BaseModel

from .models import OAuth2Account, OAuth2Token


class OAuth2AccountAdmin(BaseModel, model=OAuth2Account):
    icon = "fa fa-user"
    name = 'OAuth2Account'


class OAuth2TokenAdmin(BaseModel, model=OAuth2Token):
    icon = "fa fa-user"
    name = 'OAuth2Token'
