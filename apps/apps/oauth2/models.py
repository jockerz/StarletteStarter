import enum
import typing as t
from datetime import datetime

from sqlalchemy import ForeignKey, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from apps.apps.account.models import User
from apps.core.base.db import Base

TABLE_PREFIX = 'oauth2'


class ProviderEnum(enum.Enum):
    github = 'github'
    # google = 'google'


class OAuth2Account(Base):
    __tablename__ = f'{TABLE_PREFIX}_account'
    __table_args__ = (
        # multiple column for Unique key
        UniqueConstraint('provider', 'user_id', name='uq_provider_userid'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    # unique keys
    provider: Mapped[ProviderEnum]
    username: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("account_user.id"), index=True
    )
    user: Mapped['User'] = relationship()

    uid: Mapped[str] = mapped_column(String(191))
    last_login: Mapped[datetime] = mapped_column(
        server_default=func.now(), server_onupdate=func.now()
    )
    date_joined: Mapped[datetime] = mapped_column(server_default=func.now())
    extra_data: Mapped[t.Optional[dict]] = mapped_column(JSON)


class OAuth2Token(Base):
    __tablename__ = f'{TABLE_PREFIX}_token'

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True)
    access_token: Mapped[str]
    refresh_token: Mapped[t.Optional[str]]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    expires_at: Mapped[t.Optional[datetime]] = mapped_column()

    provider_id: Mapped[str] = mapped_column(
        ForeignKey(f'{TABLE_PREFIX}_account.id')
    )
    provider: Mapped[OAuth2Account] = relationship()

    user_id: Mapped[int] = mapped_column(ForeignKey("account_user.id"), index=True)
    user: Mapped['User'] = relationship()
