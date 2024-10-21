from __future__ import annotations

from island.core.constants.stamps import StampRank
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Enum
from island.database import Base


class StampTable(Base):
    __tablename__ = "stamps"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    collection_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(256))
    member: Mapped[bool] = mapped_column(default=False)
    rank: Mapped[StampRank] = mapped_column(Enum(StampRank))
    description: Mapped[str] = mapped_column(String(256))
    earnable_by_client: Mapped[bool] = mapped_column(default=False)
