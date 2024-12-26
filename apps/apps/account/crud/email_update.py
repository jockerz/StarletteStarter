import typing as t
from datetime import datetime

from passlib.hash import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.utils.string import gen_random
from ..models import EmailUpdate, User


class EmailUpdateCRUD:
    @staticmethod
    async def create(
        db: AsyncSession, user: User, email: str, commit: bool = True
    ) -> t.Tuple[EmailUpdate, str]:
        result = EmailUpdate()
        secret = gen_random(32)

        result.user = user
        result.secret = bcrypt.hash(secret)
        result.target = email

        if commit:
            db.add(result)
            await db.commit()

        return result, secret

    @staticmethod
    async def get(db: AsyncSession, code: str) -> t.Optional[EmailUpdate]:
        query = select(EmailUpdate).where(EmailUpdate.code == code)
        entry = await db.scalars(query)
        return entry.one_or_none()

    @staticmethod
    def validate_secret(
        token: EmailUpdate, secret: str
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
        db: AsyncSession, token: EmailUpdate, user: User
    ) -> None:
        user.email = token.target
        token.is_complete = True
        token.complete_date = datetime.now()
        db.add(user)
        db.add(token)
        await db.commit()
