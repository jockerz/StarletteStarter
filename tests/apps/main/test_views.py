import pytest

from apps.apps.account.crud.activation import ActivationCRUD
from apps.apps.account.crud.reset import ResetCRUD


@pytest.mark.parametrize('path', [
    '/',
    '/login',
    '/register',
    '/forgot'
])
async def test_public_accessible(http, path):
    resp = await http.get(path, allow_redirects=False)
    assert resp.status_code == 200


class TestActivationPage:
    URL = f'/activate'

    async def test_success(self, db, http, user):
        activation, secret = await ActivationCRUD.create(db, user)

        url = f'{self.URL}/{activation.code}.{secret}'
        resp = await http.get(url)
        assert resp.status_code == 200

    async def test_not_found_no_code_secret(self, http):
        url = f'{self.URL}'
        resp = await http.get(url)
        assert resp.status_code == 404

    async def test_not_found_not_exist_activation(self, http):
        url = f'{self.URL}/not.exist'
        resp = await http.get(url)
        assert resp.status_code == 404


class TestResetPasswordPage:
    URL = '/reset'

    async def test_success(self, db, http, user):
        reset, secret = await ResetCRUD.create(db, user)
        url = f'{self.URL}/{reset.code}.{secret}'
        resp = await http.get(url)
        assert resp.status_code == 200

    async def test_not_found_no_code_secret(self, http):
        url = f'{self.URL}'
        resp = await http.get(url)
        assert resp.status_code == 404

    async def test_not_found_not_exist_activation(self, http):
        url = f'{self.URL}/not.exist'
        resp = await http.get(url)
        assert resp.status_code == 404
