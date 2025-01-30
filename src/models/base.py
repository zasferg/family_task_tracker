import uuid
from datetime import datetime
from sqlalchemy import func, TIMESTAMP,UUID
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(UUID, primary_key=True, default=uuid.uuid4())
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )
    @classmethod
    @property
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'