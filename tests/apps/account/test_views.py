import pytest


PATH = [
    '/account/',
    '/account/settings',
    '/account/password',
    '/account/settings/email',
]


@pytest.mark.parametrize(
    'path', PATH + ['/account/settings/email_update/{code}.{secret}']
)
async def test_not_authenticated(http, path: str):
    resp = await http.get(path, allow_redirects=False)
    assert resp.status_code == 302


@pytest.mark.parametrize('path', PATH)
async def test_authenticated(http_auth, user, path: str):
    resp = await http_auth.get(path, allow_redirects=False)
    assert resp.status_code == 200
    assert bytes(user.username, 'utf8') in resp.content


class TestEmailUpdatePage:
    URL = '/account/settings/email_update/{code}.{secret}'

    async def test_no_code_or_secret(self, http_auth):
        path = self.URL.format(code='', secret='')
        resp = await http_auth.get(path, allow_redirects=False)
        assert resp.status_code == 404

    async def test_not_found(self, http_auth):
        path = self.URL.format(code='not', secret='found')
        resp = await http_auth.get(path, allow_redirects=False)
        assert resp.status_code == 404
