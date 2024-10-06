from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from island.database import Base


class PostcardTable(Base):
    __tablename__ = "postcards"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subject: Mapped[str] = mapped_column(String(256))
    in_catalog: Mapped[bool] = mapped_column(default=False)
