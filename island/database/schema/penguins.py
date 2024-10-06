from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from island.database import Base
from sqlalchemy import Integer


class PenguinColorTable(Base):
    __tablename__ = "penguin_colors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    color: Mapped[int] = mapped_column(Integer)
