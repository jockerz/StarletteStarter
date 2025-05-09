import typing as t
from datetime import datetime

from passlib.hash import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette_babel import gettext_lazy as _

from apps.utils.string import gen_random
from ..models import Activation, User


class ActivationCRUD:
    @staticmethod
    async def create(
        db: AsyncSession, user: User, commit: bool = True
    ) -> t.Tuple[Activation, str]:
        activation = Activation()
        secret = gen_random(32)

        activation.user = user
        activation.secret = bcrypt.hash(secret)
        activation.target = user.email

        if commit:
            db.add(activation)
            await db.commit()

        return activation, secret

    @staticmethod
    async def get(db: AsyncSession, code: str) -> t.Optional[Activation]:
        query = select(Activation).where(Activation.code == code)
        entry = await db.scalars(query)
        return entry.one_or_none()

    @staticmethod
    def validate_secret(
        token: Activation, secret: str, skip_expiration: bool = False,
    ) -> t.Tuple[bool, str]:
        if not skip_expiration and token.is_expired():
            return False, _('Activation has been expired')
        elif token.is_complete:
            return False, _('Activation has already been complete')
        elif token.check_secret(secret) is True:
            return True, _('Activation is ready')
        else:
            return False, _('False Activation secret')

    @staticmethod
    async def set_as_complete(
        db: AsyncSession, activation: Activation, user: User,
    ) -> None:
        user.is_active = True
        activation.is_complete = True
        activation.complete_date = datetime.now()
        db.add(user)
        db.add(activation)
        await db.commit()

    @staticmethod
    async def refresh(db: AsyncSession, activation: Activation) -> str:
        secret = activation.refresh()
        db.add(activation)
        await db.commit()
        return secret
