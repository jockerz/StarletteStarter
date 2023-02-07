import typing as t
from datetime import datetime

from passlib.hash import bcrypt, pbkdf2_sha256
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

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
        result = await db.execute(query)
        return None if result is None else result.scalars().first()

    @staticmethod
    def validate_secret(
        token: Activation, secret: str
    ) -> t.Tuple[bool, str]:
        if token.is_expired():
            return False, 'Activation has been expired'
        elif token.is_complete:
            return False, 'Activation has already been complete'
        elif token.check_secret(secret) is True:
            return True, 'Activation is ready'
        else:
            return False, 'False Activation secret'

    @staticmethod
    async def set_as_complete(
        db: AsyncSession, activation: Activation, user: User
    ) -> None:
        user.is_active = True
        activation.is_complete = True
        activation.complete_date = datetime.now()
        db.add(user)
        db.add(activation)
        await db.commit()
