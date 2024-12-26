import typing as t
from datetime import datetime

from passlib.hash import pbkdf2_sha256
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.utils.string import gen_random
from ..models import User


class UserCRUD:
    @staticmethod
    async def create(
        db: AsyncSession,
        username: str, password: str, email: str, name: str,
        is_active: bool = False, is_staff: bool = False,
        is_admin: bool = False,
        commit: bool = True
    ) -> User:
        user = User()
        user.username = username.strip().lower()
        user.email = email.strip().lower()
        if name:
            user.name = name.strip()
        user.is_active = is_active
        user.is_staff = is_staff or is_admin
        user.is_admin = is_admin
        user.set_password(password)

        if commit:
            db.add(user)
            await db.commit()

        return user

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> t.Optional[User]:
        return await db.get(User, user_id)

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> t.Optional[User]:
        stmt = select(User).where(User.email == email.lower())
        entry = await db.scalars(stmt)
        return entry.one_or_none()

    @staticmethod
    async def get_by_username(
        db: AsyncSession, username: str
    ) -> t.Optional[User]:
        stmt = select(User).where(User.username == username.lower())
        entry = await db.scalars(stmt)
        return entry.one_or_none()

    @staticmethod
    async def email_is_registered(db: AsyncSession, email: str) -> bool:
        stmt = select(User.email).where(User.email == email.lower())
        entry = await db.scalars(stmt)
        return entry.one_or_none() is not None

    @staticmethod
    async def username_is_registered(db: AsyncSession, email: str) -> bool:
        stmt = select(User.email).where(User.email == email.lower())
        entry = await db.scalars(stmt)
        return entry.one_or_none() is not None

    @staticmethod
    async def update_data(
        db: AsyncSession, user_id: int, name: str
    ) -> None:
        query = update(User).values(name=name).where(User.id == user_id)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def update_email(
        db: AsyncSession, user_id: int, email: str, commit: bool = True
    ):
        query = update(User).values(email=email).where(User.id == user_id)
        if commit:
            await db.execute(query)
            await db.commit()
        return query

    @staticmethod
    async def update_password(
        db: AsyncSession, user_id: int, password: str, commit: bool = True
    ):
        query = update(User).values(
            password=pbkdf2_sha256.hash(password),
            update_date=datetime.now()
        ).where(User.id == user_id)
        if commit:
            await db.execute(query)
            await db.commit()
        return query

    @staticmethod
    async def update_photo(db: AsyncSession, user_id: int, filename: str):
        query = update(User).values(avatar=filename).where(User.id == user_id)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def get_unique_username(db: AsyncSession, username: str) -> str:
        added_underscore = False
        while True:
            query = select(User.id).where(User.username == username.lower())
            result = await db.scalars(query)
            if result.one_or_none() is None:
                break
            if added_underscore is False:
                username = username + '_'
                added_underscore = True
            username = username + gen_random(1)
        return username
