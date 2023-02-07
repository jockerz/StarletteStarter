import typing
from datetime import datetime, timedelta
from enum import Enum
from os import path

from passlib.hash import bcrypt, pbkdf2_sha256
from starlette_login.mixins import UserMixin
from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, Integer, String, Enum as DBEnum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils.types.email import EmailType

from apps.core.base.db import Base
from apps.utils.string import gen_random


DEFAULT_AVATAR = 'default-150x150.png'
TABLE_PREFIX = 'account'


class User(Base, UserMixin):
    __tablename__ = f'{TABLE_PREFIX}_user'

    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True)
    password = Column(String(128))
    email = Column(EmailType, unique=True)
    first_name = Column(String(256))
    last_name = Column(String(256))
    # file name only
    avatar = Column(String(256), nullable=True)

    is_staff = Column(Boolean(), default=False)
    is_admin = Column(Boolean(), default=False)

    is_active = Column(Boolean(), default=True)
    date_joined = Column(DateTime, server_default=func.now())
    update_date = Column(DateTime)

    @property
    def identity(self):
        return self.id

    @property
    def is_authenticated(self):
        return True

    @property
    def display_name(self) -> str:
        return ' '.join([self.first_name or '', self.last_name or ''])

    def set_password(self, password: str):
        self.password = pbkdf2_sha256.hash(password)

    def check_password(self, password: str):
        return pbkdf2_sha256.verify(password, self.password)

    def get_avatar(self):
        if self.avatar is None:
            return DEFAULT_AVATAR
        return f'/account/{self.avatar}'

    def get_avatar_thumbnail(self):
        if self.avatar is None:
            return DEFAULT_AVATAR
        name, ext = path.splitext(self.avatar)
        return f'/account/{self.avatar.replace(ext, f"-thumb{ext}")}'


class NotificationTypeEnum(Enum):
    EMAIL = 1


class Activation(Base):
    __tablename__ = f'{TABLE_PREFIX}_activation'

    id = Column(Integer, primary_key=True)
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

    user = relationship('User')
    user_id = Column(
        Integer, ForeignKey(f'{User.__tablename__}.id', ondelete='SET NULL')
    )

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


class Reset(Base):
    __tablename__ = f'{TABLE_PREFIX}_reset'

    id = Column(Integer, primary_key=True)
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

    user = relationship('User')
    user_id = Column(
        Integer, ForeignKey(f'{User.__tablename__}.id', ondelete='SET NULL')
    )

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
