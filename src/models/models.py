import datetime
from src.models.base import  Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, TIMESTAMP, Boolean


class Tasks(Base):

    __tablename__ = "tasks"

    name: Mapped[str] = mapped_column(String(50),nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    term: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    executor: Mapped[str] = mapped_column(String(50),nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True,nullable=False)
