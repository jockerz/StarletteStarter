from datetime import datetime

import pytest

from apps.apps.oauth2.exceptions import DBIntegrityError
from apps.apps.oauth2.crud import (
    OAuth2AccountCRUD,
    OAuth2TokenCRUD,
    ProviderEnum
)

now = datetime.now()


class TestOAuth2AccountCRUD:
    async def test_create(self, db, user):
        account = await OAuth2AccountCRUD.create(
            db, provider=ProviderEnum.github, user=user, uid='UID_0',
            username='username0', extra_data={'extra': 'data'}, commit=False
        )
        assert account is not None

    async def test_create_fail_multiple_account(self, db, user):
        await OAuth2AccountCRUD.create(
            db, provider=ProviderEnum.github, user=user, uid='UID_1',
            username='username1',
        )

        with pytest.raises(DBIntegrityError):
            await OAuth2AccountCRUD.create(
                db, provider=ProviderEnum.github, user=user, uid='UID_1',
                username='username1',
            )

    async def test_get(self, db, user):
        provider = ProviderEnum.google
        try:
            if await OAuth2AccountCRUD.get(db, 'UID_2', provider) is None:
                await OAuth2AccountCRUD.create(
                    db, provider=provider, user=user, uid='UID_2',
                    username='username2',
                )
        except DBIntegrityError:
            await db.rollback()

        #
        account = await OAuth2AccountCRUD.get(db, 'UID_2', provider)
        assert account is not None

        # get by user_id
        account = await OAuth2AccountCRUD.get_by_user_id(db, user.id, provider)
        assert account is not None

        # get user accounts
        accounts = await OAuth2AccountCRUD.get_user_accounts(db, user.id)
        assert isinstance(accounts, list)
        assert len(accounts) > 0

    async def test_update_last_login(self, db, user):
        provider = ProviderEnum.google
        account = await OAuth2AccountCRUD.get_by_user_id(db, user.id, provider)
        if account is None:
            account = await OAuth2AccountCRUD.create(
                db, provider=provider, user=user, uid='UID',
                username='username',
            )

        assert account is not None
        last_login = account.last_login

        await OAuth2AccountCRUD.update_last_login(db, account)
        account = await OAuth2AccountCRUD.get_by_user_id(db, user.id, provider)

        assert account.last_login != last_login


class TestOAuth2TokenCRUD:
    async def test_create(self, db, social_account):
        token = await OAuth2TokenCRUD.create(
            db, social_account, 'access_token', 'refresh_token',
            expires_at=datetime(now.year, now.month, now.day + 3, 0, 0, 0)
        )
        assert token.access_token == 'access_token'
        assert token.refresh_token == 'refresh_token'

    async def test_get(self, db, social_account):
        await OAuth2TokenCRUD.get_by_access_token(db, 'access_token') \
            or await OAuth2TokenCRUD.create(
                db, social_account, 'access_token', 'refresh_token',
                expires_at=datetime(now.year, now.month, now.day + 3, 0, 0, 0)
            )

        assert await OAuth2TokenCRUD.get_by_access_token(db, 'access_token') \
               is not None
        assert await OAuth2TokenCRUD.get_by_refresh_token(db, 'refresh_token') \
               is not None

    async def test_remove_by_account(self, db, social_account):
        await OAuth2TokenCRUD.get_by_access_token(db, 'access_token') \
            or await OAuth2TokenCRUD.create(
                db, social_account, 'access_token', 'refresh_token',
                expires_at=datetime(now.year, now.month, now.day + 3, 0, 0, 0)
            )
        assert await OAuth2TokenCRUD.get_by_access_token(db, 'access_token') \
               is not None

        # remove token data
        await OAuth2TokenCRUD.remove_by_account(db, social_account.id)

        assert await OAuth2TokenCRUD.get_by_access_token(db, 'access_token') \
               is None
        assert await OAuth2TokenCRUD.get_by_refresh_token(db, 'refresh_token') \
               is None
