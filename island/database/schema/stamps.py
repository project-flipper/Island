from __future__ import annotations

from sqlalchemy import String, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from island.database import Base


class StampTable(Base):
    __tablename__ = "stamps"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    collection_id: Mapped[int] = mapped_column(ForeignKey("stamps_collection.id"))
    name: Mapped[str] = mapped_column(String(256))
    member: Mapped[bool] = mapped_column(default=False)
    rank: Mapped[int] = mapped_column(SmallInteger)
    description: Mapped[str] = mapped_column(String(256))

    @property
    def rank_token(self) -> str:
        return {1: "easy", 2: "medium", 3: "hard", 4: "extreme"}.get(self.rank, "")


class StampCollectionTable(Base):
    __tablename__ = "stamps_collection"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256))
    display_name: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(String(256))
    parent_id: Mapped[int] = mapped_column(ForeignKey("stamps_collection.id"))
