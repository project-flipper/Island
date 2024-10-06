from __future__ import annotations

from sqlalchemy import String, SmallInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from island.database import Base

class CardTable(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(String(256))
    set_id: Mapped[int] = mapped_column(Integer, default=1)
    power_id: Mapped[int] = mapped_column(SmallInteger, default=0)
    element: Mapped[int] = mapped_column(SmallInteger, default=0)
    color: Mapped[str] = mapped_column(String(1), default="b")
    value: Mapped[list[int]] = mapped_column(SmallInteger, default=2)
