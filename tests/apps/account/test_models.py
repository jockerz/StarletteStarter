from apps.apps.account.models import DEFAULT_AVATAR


class TestUser:
    async def test_user_data(self, user):
        assert user.username == 'user'
        assert user.check_password('password') is True
        assert user.is_active
        assert not user.is_staff
        assert not user.is_admin

    async def test_staff_data(self, staff):
        assert staff.is_admin is False
        assert staff.is_staff is True

    async def test_admin_data(self, admin):
        assert admin.is_admin is True
        assert admin.is_staff is True

    async def test_identity(self, admin):
        assert admin.identity == admin.id
        assert admin.display_name == admin.name

    async def test_password(self, user):
        assert user.check_password('password') is True

    async def test_avatar(self, admin):
        assert admin.get_avatar() == f'/{DEFAULT_AVATAR}'
        assert admin.get_avatar_thumbnail() == f'/{DEFAULT_AVATAR}'

        admin.avatar = 'changed'
        assert admin.get_avatar() == f'/account/{admin.avatar}'
        assert admin.get_avatar_thumbnail() == f'/account/{admin.avatar}-thumb'
