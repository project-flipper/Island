from __future__ import annotations

from sqlalchemy import SmallInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from island.database import Base


class FurnitureTable(Base):
    __tablename__ = "furniture"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256))
    type: Mapped[int] = mapped_column(SmallInteger, default=1)
    sort: Mapped[int] = mapped_column(SmallInteger, default=1)
    cost: Mapped[int] = mapped_column(Integer, default=0)
    member: Mapped[bool] = mapped_column(default=False)
    bait: Mapped[bool] = mapped_column(default=False)
    max_quantity: Mapped[int] = mapped_column(SmallInteger, default=100)
