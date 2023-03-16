import pytest


@pytest.mark.parametrize('path', [
    '/',
    '/login',
    '/register',
    '/forgot'
])
async def test_public_accessible(http, path):
    resp = await http.get(path, allow_redirects=False)
    assert resp.status_code == 200


# TODO: activation_page, reset_password_page
