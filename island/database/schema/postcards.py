from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, SmallInteger
from island.database import Base


class PostcardTable(Base):
    __tablename__ = "postcards"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    collection_id: Mapped[int] = mapped_column(ForeignKey("postcards_collection.id"))
    subject: Mapped[str] = mapped_column(String(256))
    in_catalog: Mapped[bool] = mapped_column(default=False)

    collection: Mapped["PostcardCollectionTable"] = relationship("PostcardCollectionTable", back_populates="postcards")


class PostcardCollectionTable(Base):
    __tablename__ = "postcards_collection"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256))
    order_position: Mapped[int] = mapped_column(SmallInteger)

    postcards: Mapped["PostcardTable"] = relationship("PostcardTable", back_populates="collection")
