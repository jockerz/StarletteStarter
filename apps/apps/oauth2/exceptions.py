from apps.core.base.exception import BaseAppException


class DBIntegrityError(BaseAppException):
    status_code = 400
    detail = 'You have created an account with the provider'


class InvalidOAuth2ProviderError(BaseAppException):
    status_code = 403
    title = 'Authentication failed'
    detail = 'Invalid authentication provider'


class OAuth2MismatchingStateError(BaseAppException):
    status_code = 403
    title = 'Authentication failed'
    detail = 'Invalid OAuth2 authentication state'
