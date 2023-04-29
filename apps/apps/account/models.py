import typing as t
from datetime import datetime
from os import path

from passlib.hash import pbkdf2_sha256
from starlette_login.mixins import UserMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy_utils.types.email import EmailType

from apps.core.base.db import Base, ValidationMixin


DEFAULT_AVATAR = 'default-150x150.png'
TABLE_PREFIX = 'account'


class User(Base, UserMixin):
    __tablename__ = f'{TABLE_PREFIX}_user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True)
    password: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(EmailType, unique=True)
    name: Mapped[str] = mapped_column(String(256), nullable=True)
    # file name only
    avatar: Mapped[str] = mapped_column(String(256), nullable=True)

    is_staff: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

    is_active: Mapped[bool] = mapped_column(default=False)
    date_joined: Mapped[datetime] = mapped_column(server_default=func.now())
    update_date: Mapped[t.Optional[datetime]] = mapped_column()

    def __str__(self):
        return f'<User id={self.identity}>'

    @property
    def identity(self) -> int:
        return self.id

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.name or ''

    def set_password(self, password: str) -> None:
        self.password = pbkdf2_sha256.hash(password)

    def check_password(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password, self.password)

    def get_avatar(self) -> str:
        if not self.avatar:
            return f'/{DEFAULT_AVATAR}'
        return f'/account/{self.avatar}'

    def get_avatar_thumbnail(self) -> str:
        if not self.avatar:
            return f'/{DEFAULT_AVATAR}'

        name, ext = path.splitext(self.avatar)
        if ext:
            return f'/account/{self.avatar.replace(ext, f"-thumb{ext}")}'
        else:
            return f'/account/{self.avatar}-thumb'


class Activation(ValidationMixin, Base):
    __tablename__ = f'{TABLE_PREFIX}_activation'


class Reset(ValidationMixin, Base):
    __tablename__ = f'{TABLE_PREFIX}_reset'


class EmailUpdate(ValidationMixin, Base):
    __tablename__ = f'{TABLE_PREFIX}_email_update'
