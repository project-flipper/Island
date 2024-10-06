from __future__ import annotations

from sqlalchemy import String, SmallInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column
from island.database import Base


class ItemTable(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256))
    type: Mapped[int] = mapped_column(SmallInteger, default=1)
    cost: Mapped[int] = mapped_column(Integer, default=0)
    layer: Mapped[int] = mapped_column(SmallInteger, default=1)
    member: Mapped[bool] = mapped_column(default=False)
    bait: Mapped[bool] = mapped_column(default=False)
    epf: Mapped[bool] = mapped_column(default=False)
    tour: Mapped[bool] = mapped_column(default=False)
    treasure: Mapped[bool] = mapped_column(default=False)
