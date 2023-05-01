AUTH_RED_URL = \
    '/authorize/google' \
    '?state=mOk1Vv0bhIPdhnB7mfYdbmdkWVN8qN' \
    '&code=4%2F0AbUR2VOPYJ2d8VKsmxSU8c3DWjaG8DBDFHXy1883YUbyFjTRGNc7sABhv8LI2MQccW7p5A' \
    '&scope=email+profile+openid' \
    '+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile' \
    '+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email' \
    '&authuser=0'


class TestAuthorize:
    url = f'/social/authorize'

    async def test_invalid_provider(self, http):
        url = f'{self.url}/invalid'
        resp = await http.get(url, allow_redirects=False)
        assert resp.status_code == 403
        assert 'Invalid authentication provider' in resp.text

    async def test_invalid_state(self, http):
        url = f'{self.url}/invalid'
        resp = await http.get(url, allow_redirects=False)
        assert resp.status_code == 403


class TestLogin:
    url = f'/social/login'

    async def test_valid_provider(self, http_auth):
        url = f'{self.url}/github'
        resp = await http_auth.get(url, allow_redirects=False)
        assert resp.status_code == 302

        url = f'{self.url}/google'
        resp = await http_auth.get(url, allow_redirects=False)
        assert resp.status_code == 302

    async def test_invalid_provider(self, http_auth):
        url = f'{self.url}/invalid'
        resp = await http_auth.get(url, allow_redirects=False)
        assert resp.status_code == 403
        assert 'Invalid authentication provider' in resp.text

    async def test_authenticated_user(self, http_auth):
        url = f'{self.url}/google'
        resp = await http_auth.get(url, allow_redirects=False)
        assert resp.status_code == 302
        assert 'location' in resp.headers

    async def test_non_authenticated_user(self, http):
        url = f'{self.url}/google'
        resp = await http.get(url, allow_redirects=False)
        assert resp.status_code == 302
        assert 'google.com' in resp.headers['location']

        url = f'{self.url}/github'
        resp = await http.get(url, allow_redirects=False)
        assert resp.status_code == 302
        assert 'github.com' in resp.headers['location']


class TestLinkAccount:
    url = f'/social/link_account'

    async def test_auth_required(self, http):
        url = self.url + '/github'

        resp = await http.get(url, allow_redirects=False)
        assert resp.status_code == 302
        assert '/login' in resp.headers['location']


class TestLinkedAccounts:
    url = f'/social/link_account'

    async def test_auth_required(self, http):
        resp = await http.get(self.url, allow_redirects=False)
        assert resp.status_code == 302
        assert '/login' in resp.headers['location']

    async def test_get_accounts(self, http_auth):
        resp = await http_auth.get(self.url, allow_redirects=False)
        assert resp.status_code == 200


class TestUnlinkAccount:
    url = f'/social/unlink_account'

    async def test_auth_required(self, http):
        url = self.url + '/github'

        resp = await http.get(url, allow_redirects=False)
        assert resp.status_code == 302
        assert '/login' in resp.headers['location']
