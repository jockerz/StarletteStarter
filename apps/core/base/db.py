from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


metadata = Base.metadata


class BaseDRUD:
    model: Base = None

    @classmethod
    async def get_count_all(cls, db: AsyncSession):
        stmt = select([func.count()]).select_from(cls.model)
        entry = await db.execute(stmt)
        return entry.scalar()
