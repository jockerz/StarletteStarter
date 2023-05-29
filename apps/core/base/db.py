import typing as t
from datetime import datetime, timedelta
from enum import Enum

from passlib.hash import bcrypt
from sqlalchemy import (
    func, select, Column, Enum as DBEnum,
    ForeignKey, String
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    as_declarative, declared_attr, Mapped, mapped_column, relationship
)

from apps.utils.string import gen_random


@as_declarative()
class Base:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BaseDRUD:
    model: Base = None

    @classmethod
    async def get_count_all(cls, db: AsyncSession):
        stmt = select([func.count()]).select_from(cls.model)
        entry = await db.execute(stmt)
        return entry.scalar()


class NotificationTypeEnum(Enum):
    EMAIL = 'EMAIL'


class ValidationMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, default=gen_random)
    secret: Mapped[str] = mapped_column(String(150))
    notif_type: Mapped[NotificationTypeEnum] = mapped_column(
        default=NotificationTypeEnum.EMAIL
    )
    # Target by `reset_type`, e.g. email address
    target: Mapped[str] = mapped_column(String(255), nullable=False)

    create_date: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    refresh_date: Mapped[datetime] = mapped_column(nullable=True)
    expired_date: Mapped[datetime] = mapped_column(
        default=datetime.now() + timedelta(days=3)
    )
    complete_date: Mapped[t.Optional[datetime]] = mapped_column()
    is_complete: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("account_user.id"))

    @declared_attr
    def user(self):
        return relationship("User")

    def refresh(self) -> str:
        plain_secret = gen_random(32)
        self.secret = bcrypt.hash(plain_secret)
        self.refresh_date = datetime.now()
        self.expired_date = datetime.now() + timedelta(days=3)
        return plain_secret

    def check_secret(self, secret: str):
        return bcrypt.verify(secret, self.secret)

    def is_expired(self):
        return self.expired_date <= datetime.now()
