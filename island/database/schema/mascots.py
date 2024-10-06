from __future__ import annotations

from sqlalchemy import String, SmallInteger, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from island.database import Base

class MascotTable(Base):
    __tablename__ = "mascots"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256))
    title: Mapped[str] = mapped_column(String(256))
    gift_id: Mapped[int] = mapped_column(Integer, ForeignKey("items.id"))
