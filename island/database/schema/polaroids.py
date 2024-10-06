from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, SmallInteger, ForeignKey
from island.database import Base


class PolaroidTable(Base):
    __tablename__ = "polaroids"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    collection_id: Mapped[int] = mapped_column(ForeignKey("polaroids_collection.id"))
    stamp_count: Mapped[int] = mapped_column(SmallInteger)
    description: Mapped[str] = mapped_column(String(256))
    earnable_by_client: Mapped[bool] = mapped_column(default=False)

    collection: Mapped["PolaroidCollectionTable"] = relationship(
        "PolaroidCollectionTable", back_populates="polaroids"
    )


class PolaroidCollectionTable(Base):
    __tablename__ = "polaroids_collection"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(String(256))
    display: Mapped[str] = mapped_column(String(256))

    polaroids: Mapped["PolaroidTable"] = relationship(
        "PolaroidTable", back_populates="collection"
    )
