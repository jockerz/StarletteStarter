from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from apps.core.base.db import Base

TABLE_PREFIX = 'ChangeMe'


class NewModel(Base):
    # TODO: Change the table name
    __tablename__ = f'{TABLE_PREFIX}_changeme'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
