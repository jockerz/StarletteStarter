from secure import Secure
from secure.headers import (
    CacheControl,
    CrossOriginOpenerPolicy,
    # ContentSecurityPolicy,
    StrictTransportSecurity,
    PermissionsPolicy,
    ReferrerPolicy,
    Server,
    XContentTypeOptions,
    XFrameOptions
)


secure_headers_template = Secure.with_default_headers()
secure_headers = Secure(
    cache=CacheControl().no_store(),
    coop=CrossOriginOpenerPolicy().same_origin(),
    hsts=StrictTransportSecurity().max_age(31536000),
    permissions=PermissionsPolicy().geolocation().microphone().camera(),
    referrer=ReferrerPolicy().strict_origin_when_cross_origin(),
    server=Server().set(""),
    xcto=XContentTypeOptions().nosniff(),
    xfo=XFrameOptions().sameorigin(),
)
