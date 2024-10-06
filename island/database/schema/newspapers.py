from __future__ import annotations

from sqlalchemy import String, DateTime, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from island.database import Base
from datetime import datetime


class NewspaperTable(Base):
    __tablename__ = "newspapers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(256))
    path: Mapped[str] = mapped_column(String(256))
    key: Mapped[str] = mapped_column(String(256))
    issue: Mapped[str] = mapped_column(String(256))
    date: Mapped[datetime] = mapped_column(DateTime, server_default="now()")
