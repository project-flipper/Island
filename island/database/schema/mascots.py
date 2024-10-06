from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from island.database import Base

if TYPE_CHECKING:
    from island.database.schema.items import ItemTable
    from island.database.schema.user import UserTable


class MascotTable(Base):
    __tablename__ = "mascots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256))
    title: Mapped[str] = mapped_column(String(256))
    gift_id: Mapped[int] = mapped_column(Integer, ForeignKey("items.id"))

    gift: Mapped[ItemTable] = relationship("ItemTable")
    user: Mapped[UserTable] = relationship("UserTable", back_populates="mascot")
