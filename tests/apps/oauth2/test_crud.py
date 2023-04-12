import pytest

from apps.apps.oauth2.exceptions import DBIntegrityError
from apps.apps.oauth2.crud import OAuth2AccountCRUD, ProviderEnum


class TestOAuth2AccountCRUD:
    async def test_create(self, db, user):
        account = await OAuth2AccountCRUD.create(
            db, provider=ProviderEnum.github, user=user, uid='UID',
            extra_data={'extra': 'data'}, commit=False
        )
        assert account is not None

    async def test_create_fail_multiple_account(self, db, user):
        await OAuth2AccountCRUD.create(
            db, provider=ProviderEnum.github, user=user, uid='UID_1'
        )

        with pytest.raises(DBIntegrityError):
            await OAuth2AccountCRUD.create(
                db, provider=ProviderEnum.github, user=user, uid='UID_1'
            )

    async def test_get(self, db, user):
        provider = ProviderEnum.google
        try:
            if await OAuth2AccountCRUD.get(db, user.id, provider) is None:
                await OAuth2AccountCRUD.create(
                    db, provider=provider, user=user, uid='UID_2'
                )
        except DBIntegrityError:
            pass

        account = await OAuth2AccountCRUD.get(db, 'UID_2', provider)
        assert account is not None

    async def test_get_by_user_id(self, db, user):
        provider = ProviderEnum.github
        try:
            if await OAuth2AccountCRUD.get(db, user.id, provider) is None:
                await OAuth2AccountCRUD.create(
                    db, provider=provider, user=user, uid='UID_2'
                )
        except DBIntegrityError:
            pass

        account = await OAuth2AccountCRUD.get_by_user_id(db, user.id, provider)
        assert account is not None

    async def test_get_user_accounts(self, db, user):
        try:
            if await OAuth2AccountCRUD.get(
                db, user.id, ProviderEnum.github
            ) is None:
                await OAuth2AccountCRUD.create(
                    db, provider=ProviderEnum.github, user=user, uid='UID_2'
                )
        except DBIntegrityError:
            pass

        accounts = await OAuth2AccountCRUD.get_user_accounts(db, user.id)
        assert isinstance(accounts, list)
        assert len(accounts) > 0
