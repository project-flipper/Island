from __future__ import annotations

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from island.database import Base

class IglooTable(Base):
    __tablename__ = "igloos"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256))
    cost: Mapped[int] = mapped_column(Integer, default=0)

class IglooFloorTable(Base):
    __tablename__ = "igloo_floors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256))
    cost: Mapped[int] = mapped_column(Integer, default=0)

class IglooLocationTable(Base):
    __tablename__ = "igloo_locations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    igloo_id: Mapped[int] = mapped_column(Integer, ForeignKey("igloos.id"))
    name: Mapped[str] = mapped_column(String(256))
    cost: Mapped[int] = mapped_column(Integer, default=0)
