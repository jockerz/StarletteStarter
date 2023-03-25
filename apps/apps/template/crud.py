import typing as t

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import NewModel


class NewModelCRUD:
    @staticmethod
    async def create(db: AsyncSession, name: str, commit: bool = True):
        data = NewModel()
        data.name = name
        if commit:
            db.add(data)
            await db.commit()
        return data

    @staticmethod
    async def get_by_id(db: AsyncSession, data_id: int) -> t.Optional[NewModel]:
        return await db.get(NewModel, data_id)

    @staticmethod
    async def get_by_username(
        db: AsyncSession, name: str
    ) -> t.Optional[NewModel]:
        stmt = select(NewModel).where(NewModel.name == name)
        entry = await db.execute(stmt)
        return None if entry is None else entry.scalars().first()
