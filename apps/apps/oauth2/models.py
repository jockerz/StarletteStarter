import enum
import typing as t
from datetime import datetime

from sqlalchemy import (
    ForeignKey, ForeignKeyConstraint, JSON, String, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from apps.apps.account.models import User
from apps.core.base.db import Base

TABLE_PREFIX = 'oauth2'
UQ_PROVIDER_USERID = 'uq_provider_userid'


class ProviderEnum(enum.Enum):
    github = 'github'
    google = 'google'


class OAuth2Account(Base):
    __tablename__ = f'{TABLE_PREFIX}_account'
    __table_args__ = (
        # multiple column for Unique key
        UniqueConstraint('provider', 'user_id', name=UQ_PROVIDER_USERID),
    )

    # unique keys
    provider: Mapped[ProviderEnum] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("account_user.id"), primary_key=True
    )

    uid: Mapped[str] = mapped_column(String(191))
    last_login: Mapped[datetime]
    date_joined: Mapped[datetime] = mapped_column(server_default=func.now())
    extra_data: Mapped[t.Optional[dict]] = mapped_column(JSON)


class OAuth2Token(Base):
    __tablename__ = f'{TABLE_PREFIX}_token'
    __table_args__ = (
        # Foreignkey to multiple column
        ForeignKeyConstraint(['account_provider', 'account_user_id'], [
            f'{TABLE_PREFIX}_account.provider',
            f'{TABLE_PREFIX}_account.user_id'
        ]),
    )

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True)

    # foreign keys
    account_provider: Mapped[str]
    account_user_id: Mapped[int]

    access_token: Mapped[str]
    refresh_token: Mapped[t.Optional[str]]
    expires_at: Mapped[datetime]
