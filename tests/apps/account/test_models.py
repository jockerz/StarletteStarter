from apps.apps.account.models import (
    User, Activation, Reset, EmailUpdate,
    DEFAULT_AVATAR
)


class TestUser:
    async def test_identity(self, user):
        assert user.identity == user.id
        assert user.display_name == user.name == 'User'
        assert user.username == 'user'

    async def test_password(self, user):
        assert user.check_password('password') is True
        user.set_password('new_password')
        assert user.check_password('new_password') is True

    async def test_avatar(self, user):
        assert user.get_avatar() == f'/{DEFAULT_AVATAR}'
        assert user.get_avatar_thumbnail() == f'/{DEFAULT_AVATAR}'

        user.avatar = 'changed'
        assert user.get_avatar() == f'/account/{user.avatar}'
        assert user.get_avatar_thumbnail() == f'/account/{user.avatar}-thumb'
