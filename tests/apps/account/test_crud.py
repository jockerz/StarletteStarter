from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError
from apps.apps.account.crud.activation import ActivationCRUD
from apps.apps.account.crud.email_update import EmailUpdateCRUD
from apps.apps.account.crud.reset import ResetCRUD
from apps.apps.account.crud.user import UserCRUD


class TestActivationCRUD:
    async def test_create_success(self, db, inactive_user):
        a, secret = await ActivationCRUD.create(db, inactive_user, False)

        assert a.secret != secret
        assert a.user.id == inactive_user.id

    async def test_success_get(self, db, user):
        a, secret = await ActivationCRUD.create(db, user)
        a = await ActivationCRUD.get(db, a.code)

        assert a is not None
        assert a.user_id == user.id
        assert a.is_complete is False

    async def test_fail_get_not_found(self, db):
        a = await ActivationCRUD.get(db, 'not_exist')
        assert a is None

    async def test_validate_secret(self, db, user):
        a, secret = await ActivationCRUD.create(db, user)

        success, reason = ActivationCRUD.validate_secret(a, secret)
        assert success is True

        success, reason = ActivationCRUD.validate_secret(a, 'invalid secret')
        assert success is False

    async def test_validate_secret_expired(self, db, user):
        a, secret = await ActivationCRUD.create(db, user)
        a.expired_date = datetime.now()

        success, reason = ActivationCRUD.validate_secret(a, secret)
        assert success is False
        assert 'expired' in reason

    async def test_validate_secret_already_complete(self, db, user):
        a, secret = await ActivationCRUD.create(db, user)
        a.is_complete = True

        assert a.is_expired() is False

        success, reason = ActivationCRUD.validate_secret(a, secret)
        assert success is False
        assert 'complete' in reason

    async def test_set_as_complete(self, db, user):
        a, secret = await ActivationCRUD.create(db, user)
        await ActivationCRUD.set_as_complete(db, a, user)
        a = await ActivationCRUD.get(db, a.code)

        assert user.is_active
        assert a.is_complete is True


class TestEmailUpdateCRUD:
    async def test_create_success(self, db, user):
        a, secret = await EmailUpdateCRUD.create(
            db, user, 'new@mail.com', False
        )

        assert a.secret != secret
        assert a.user.id == user.id

    async def test_success_get(self, db, user):
        a, secret = await EmailUpdateCRUD.create(db, user, 'new@mail.com')
        a = await EmailUpdateCRUD.get(db, a.code)

        assert a is not None
        assert a.user_id == user.id
        assert a.is_complete is False

    async def test_fail_get_not_found(self, db):
        a = await EmailUpdateCRUD.get(db, 'not_exist')
        assert a is None

    async def test_validate_secret(self, db, user):
        a, secret = await EmailUpdateCRUD.create(db, user, 'new@mail.com')

        success, reason = EmailUpdateCRUD.validate_secret(a, secret)
        assert success is True

        success, reason = EmailUpdateCRUD.validate_secret(a, 'invalid secret')
        assert success is False

    async def test_validate_secret_expired(self, db, user):
        a, secret = await EmailUpdateCRUD.create(db, user, 'new@mail.com')
        a.expired_date = datetime.now()

        assert a.is_expired()

        success, reason = EmailUpdateCRUD.validate_secret(a, secret)
        assert success is False
        assert 'expired' in reason

    async def test_validate_secret_already_complete(self, db, user):
        a, secret = await EmailUpdateCRUD.create(db, user, 'new@mail.com')
        a.is_complete = True

        assert a.is_expired() is False

        success, reason = EmailUpdateCRUD.validate_secret(a, secret)
        assert success is False
        assert 'complete' in reason

    async def test_set_as_complete(self, db, user):
        a, secret = await EmailUpdateCRUD.create(db, user, 'new@mail.com')
        await EmailUpdateCRUD.set_as_complete(db, a, user)
        a = await EmailUpdateCRUD.get(db, a.code)

        assert user.is_active
        assert a.is_complete is True


class TestResetCRUD:
    async def test_create_success(self, db, inactive_user):
        a, secret = await ResetCRUD.create(db, inactive_user, False)

        assert a.secret != secret
        assert a.user.id == inactive_user.id

    async def test_success_get(self, db, user):
        a, secret = await ResetCRUD.create(db, user)
        a = await ResetCRUD.get(db, a.code)

        assert a is not None
        assert a.user_id == user.id
        assert a.is_complete is False

    async def test_fail_get_not_found(self, db):
        a = await ResetCRUD.get(db, 'not_exist')
        assert a is None

    async def test_validate_secret(self, db, user):
        a, secret = await ResetCRUD.create(db, user)

        success, reason = ResetCRUD.validate_secret(a, secret)
        assert success is True

        success, reason = ResetCRUD.validate_secret(a, 'invalid secret')
        assert success is False

    async def test_validate_secret_expired(self, db, user):
        a, secret = await ResetCRUD.create(db, user)
        a.expired_date = datetime.now()

        assert a.is_expired()

        success, reason = ResetCRUD.validate_secret(a, secret)
        assert success is False
        assert 'expired' in reason

    async def test_validate_secret_already_complete(self, db, user):
        a, secret = await ResetCRUD.create(db, user)
        a.is_complete = True

        assert a.is_expired() is False

        success, reason = ResetCRUD.validate_secret(a, secret)
        assert success is False
        assert 'complete' in reason

    async def test_set_as_complete(self, db, user):
        a, secret = await ResetCRUD.create(db, user)
        await ResetCRUD.set_as_complete(db, a, user)
        a = await ResetCRUD.get(db, a.code)

        assert a.is_complete is True


class TestUserCRUD:
    async def test_create(self, db):
        user = await UserCRUD.create(
            db, 'created_new', 'password', 'user@mail.com', 'Name',
            is_active=True,
        )
        assert user is not None
        assert user.username == 'created_new'
        assert user.check_password('password') is True
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_admin is False

    async def test_create_duplicate_username(self, db, user):
        with pytest.raises(IntegrityError):
            await UserCRUD.create(
                db, user.username, 'password', 'user@mail.com', 'Name'
            )

    async def test_create_duplicate_email(self, db, user):
        with pytest.raises(IntegrityError):
            await UserCRUD.create(
                db, 'new_user', 'password', user.email, 'Name'
            )

    async def test_get_by_id(self, db, user):
        # Found
        assert await UserCRUD.get_by_id(db, user.id) is not None
        # Not found
        assert await UserCRUD.get_by_id(db, 1000) is None

    async def test_get_by_email(self, db, user):
        # Found
        assert await UserCRUD.get_by_email(db, user.email) is not None
        # Not found
        assert await UserCRUD.get_by_email(db, 'not_exist@any') is None

    async def test_get_by_username(self, db, user):
        # Found
        assert await UserCRUD.get_by_username(db, user.username) is not None
        # Not found
        assert await UserCRUD.get_by_username(db, 'not_exist') is None

    async def test_update_data(self, db, user):
        old_data = user.name
        await UserCRUD.update_data(db, user.id, 'new name')

        assert user.name != old_data

    async def test_update_email(self, db, user):
        old_data = user.email
        await UserCRUD.update_email(db, user.id, 'new@mail.com')

        assert user.email != old_data

    async def test_update_avatar(self, db, user):
        old_data = user.avatar
        await UserCRUD.update_photo(db, user.id, 'filename')

        assert user.avatar != old_data
