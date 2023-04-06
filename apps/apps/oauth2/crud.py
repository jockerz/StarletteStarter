import typing as t
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from apps.apps.account.models import User
from .exceptions import DBIntegrityError
from .models import OAuth2Account, OAuth2Token, ProviderEnum


class OAuth2AccountCRUD:
    @staticmethod
    async def create(
        db: AsyncSession, provider: ProviderEnum, user: User,
        uid: str, extra_data: dict = None, commit: bool = True
    ) -> OAuth2Account:
        account = OAuth2Account(
            provider=provider, uid=uid, user=user, extra_data=extra_data
        )
        if commit:
            try:
                db.add(account)
                await db.commit()
            except IntegrityError:
                await db.rollback()
                raise DBIntegrityError
        return account

    @staticmethod
    async def get(
        db: AsyncSession, uid: str, provider: ProviderEnum
    ) -> t.Optional[OAuth2Account]:
        stmt = select(OAuth2Account).where(
            OAuth2Account.provider == provider,
            OAuth2Account.uid == uid,
        )
        entry = await db.scalars(stmt)
        return None if entry is None else entry.first()

    @staticmethod
    async def get_by_user_id(
        db: AsyncSession, user_id: int, provider: ProviderEnum
    ) -> t.Optional[OAuth2Account]:
        stmt = select(OAuth2Account).where(
            OAuth2Account.provider == provider,
            OAuth2Account.user_id == user_id,
        )
        entry = await db.scalars(stmt)
        return None if entry is None else entry.first()

    @staticmethod
    async def get_user_accounts(
        db: AsyncSession, user_id: int
    ) -> t.Sequence[OAuth2Account]:
        stmt = select(OAuth2Account).where(OAuth2Account.user_id == user_id)
        entry = await db.scalars(stmt)
        return entry.all()

    @staticmethod
    async def update_last_login(
        db: AsyncSession, account: OAuth2Account, commit: bool = True
    ) -> None:
        # TODO: test
        stmt = update(OAuth2Account).where(
            OAuth2Account.provider == account.provider,
            OAuth2Account.user_id == account.user_id,
        ).values(
            last_login=datetime.now()
        )
        await db.execute(stmt)
        if commit:
            await db.commit()


class OAuth2TokenCRUD:
    @staticmethod
    async def create(
        db: AsyncSession, account: OAuth2Account,
        access_token: str, refresh_token: t.Optional[str],
        expires_at: datetime, commit: bool = True
    ) -> OAuth2Token:
        token = OAuth2Token(
            provider=account,
            user=account.user,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
        )
        if commit:
            db.add(token)
            await db.commit()
        return token

    @staticmethod
    async def get_by_access_token(
        db: AsyncSession, access_token: str
    ) -> t.Optional[OAuth2Token]:
        stmt = select(OAuth2Token).where(
            OAuth2Token.access_token == access_token,
        )
        entry = await db.scalars(stmt)
        return None if entry is None else entry.first()

    @staticmethod
    async def get_by_refresh_token(
        db: AsyncSession, refresh_token: str
    ) -> t.Optional[OAuth2Token]:
        stmt = select(OAuth2Token).where(
            OAuth2Token.refresh_token == refresh_token,
        )
        entry = await db.scalars(stmt)
        return None if entry is None else entry.first()
