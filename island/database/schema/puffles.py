from __future__ import annotations

from sqlalchemy import String, SmallInteger, Integer, ForeignKey, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from island.database import Base


class PuffleTable(Base):
    __tablename__ = "puffles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey("puffles.id"))
    description: Mapped[str] = mapped_column(String(256))
    color: Mapped[int] = mapped_column(Integer)
    member: Mapped[bool] = mapped_column(default=False)


class PuffleItemTable(Base):
    __tablename__ = "puffle_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256))
    path: Mapped[str] = mapped_column(String(256))
    cost: Mapped[int] = mapped_column(Integer, default=0)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    member: Mapped[bool] = mapped_column(default=False)
    play_external: Mapped[str] = mapped_column(String(256))
    consumption: Mapped[str] = mapped_column(String(256))
    class_name: Mapped[str] = mapped_column(String(256))
    root_item_id: Mapped[int] = mapped_column(Integer)
    only_purchase: Mapped[bool] = mapped_column(default=False)
    effect_food: Mapped[int] = mapped_column(SmallInteger)
    effect_rest: Mapped[int] = mapped_column(SmallInteger)
    effect_play: Mapped[int] = mapped_column(SmallInteger)
    effect_clean: Mapped[int] = mapped_column(SmallInteger)
    reaction: Mapped[list] = mapped_column(ARRAY(Integer))
