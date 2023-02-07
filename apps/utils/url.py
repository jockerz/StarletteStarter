from urllib.parse import urlparse


def validate_next_url(next_url: str, allow_hostname: bool = False):
    """
    Parse for url path if `allow_hostname` is False

    :param next_url: next url
    :param allow_hostname: different host is allowed, return immediately
    :return: parsed `next_ur` if `allow_hostname` is False
             or else return plain `next_url`
    """
    if not next_url:
        return None
    if allow_hostname:
        return next_url
    parsed = urlparse(next_url, allow_fragments=True)
    return f'{parsed.path}?{parsed.query}#{parsed.fragment}'
