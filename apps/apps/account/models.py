from os import path

from passlib.hash import pbkdf2_sha256
from starlette_login.mixins import UserMixin
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy_utils.types.email import EmailType

from apps.core.base.db import Base, ValidationMixin


DEFAULT_AVATAR = 'default-150x150.png'
TABLE_PREFIX = 'account'


class User(Base, UserMixin):
    __tablename__ = f'{TABLE_PREFIX}_user'

    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True)
    password = Column(String(128))
    email = Column(EmailType, unique=True)
    name = Column(String(256))
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
        return self.name or ''

    def set_password(self, password: str):
        self.password = pbkdf2_sha256.hash(password)

    def check_password(self, password: str):
        return pbkdf2_sha256.verify(password, self.password)

    def get_avatar(self):
        if not self.avatar:
            return f'/{DEFAULT_AVATAR}'
        return f'/account/{self.avatar}'

    def get_avatar_thumbnail(self):
        if not self.avatar:
            return f'/{DEFAULT_AVATAR}'
        name, ext = path.splitext(self.avatar)
        return f'/account/{self.avatar.replace(ext, f"-thumb{ext}")}'


class Activation(ValidationMixin, Base):
    __tablename__ = f'{TABLE_PREFIX}_activation'


class Reset(ValidationMixin, Base):
    __tablename__ = f'{TABLE_PREFIX}_reset'


class EmailUpdate(ValidationMixin, Base):
    __tablename__ = f'{TABLE_PREFIX}_email_update'
