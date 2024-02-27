from apps.core.base.exception import BaseAppException


class DBIntegrityError(BaseAppException):
    status_code = 400
    title = 'Authentication failed'
    detail = 'You have created an account with the provider'


class EmailDBIntegrityError(BaseAppException):
    status_code = 400
    title = 'Authentication failed'
    detail = 'Your email from this third party provider has been registered'


class InvalidOAuth2ProviderError(BaseAppException):
    status_code = 403
    title = 'Authentication failed'
    detail = 'Invalid authentication provider'


class OAuth2MismatchingStateError(BaseAppException):
    status_code = 403
    title = 'Invalid OAuth2 authentication state'
    detail = 'Invalid OAuth2 authentication state'
