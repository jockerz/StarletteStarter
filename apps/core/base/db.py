from datetime import datetime, timedelta
from enum import Enum

from passlib.hash import bcrypt
from sqlalchemy import (
    func, select, Boolean, Column, DateTime, Enum as DBEnum,
    ForeignKey, Integer, String
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.utils.string import gen_random


@as_declarative()
class Base:
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
    EMAIL = 1


class ValidationMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
    code = Column(String(32), unique=True, default=gen_random)
    secret = Column(String(150))
    notif_type = Column(
        DBEnum(NotificationTypeEnum), default=NotificationTypeEnum.EMAIL
    )
    # Target by `reset_type`, e.g. email address
    target = Column(String(255), nullable=False)

    create_date = Column(DateTime, server_default=func.now(), nullable=False)
    refresh_date = Column(DateTime)
    expired_date = Column(DateTime, default=datetime.now() + timedelta(days=3))
    complete_date = Column(DateTime)
    is_complete = Column(Boolean, default=False)

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
