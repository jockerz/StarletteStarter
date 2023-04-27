import typing as t
from datetime import datetime

from passlib.hash import pbkdf2_sha256
from sqlalchemy import select, update, exists
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
        entry = await db.execute(stmt)
        return None if entry is None else entry.scalars().first()

    @staticmethod
    async def get_by_username(
        db: AsyncSession, username: str
    ) -> t.Optional[User]:
        stmt = select(User).where(User.username == username.lower())
        entry = await db.execute(stmt)
        return None if entry is None else entry.scalars().first()

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
        # existed = True
        # while existed:
        query = exists().where(User.username == username.lower())
        print(f'query: {query}')
        result = await db.execute(query)
        print(f'result: {result}')
        return username
