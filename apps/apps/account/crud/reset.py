import typing as t
from datetime import datetime

from passlib.hash import bcrypt
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.utils.string import gen_random
from ..models import Reset, User


class ResetCRUD:
    @staticmethod
    async def create(
        db: AsyncSession, user: User, commit: bool = True
    ) -> t.Tuple[Reset, str]:
        reset = Reset()
        secret = gen_random(32)

        reset.user = user
        reset.secret = bcrypt.hash(secret)
        reset.target = user.email

        if commit:
            db.add(reset)
            await db.commit()

        return reset, secret

    @staticmethod
    async def get(db: AsyncSession, code: str) -> t.Optional[Reset]:
        query = select(Reset).where(Reset.code == code)
        result = await db.execute(query)
        return None if result is None else result.scalars().first()

    @staticmethod
    def validate_secret(
        token: Reset, secret: str
    ) -> t.Tuple[bool, str]:
        if token.is_expired():
            return False, 'Reset token has been expired'
        elif token.is_complete:
            return False, 'Reset token has already been complete'
        elif token.check_secret(secret) is True:
            return True, 'Password reset is ready'
        else:
            return False, 'False token secret'

    @staticmethod
    async def set_as_complete(
        db: AsyncSession, reset: Reset, commit: bool = True
    ) -> None:
        reset.is_complete = True
        reset.complete_date = datetime.now()

        if commit:
            db.add(reset)
            await db.commit()
