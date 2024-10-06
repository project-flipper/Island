from __future__ import annotations

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from island.database import Base


class RoomTable(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(256))
    name: Mapped[str] = mapped_column(String(256))
    short_name: Mapped[str] = mapped_column(String(256))
    display_name: Mapped[str] = mapped_column(String(256))
    path: Mapped[str] = mapped_column(String(256))
    spawn: Mapped[bool] = mapped_column(default=False)
    member: Mapped[bool] = mapped_column(default=False)
    jump_enabled: Mapped[bool] = mapped_column(default=False)
    music_id: Mapped[int] = mapped_column(Integer)
    max_users: Mapped[int] = mapped_column(Integer, default=100)
    required_item: Mapped[int] = mapped_column(
        Integer, ForeignKey("items.id"), nullable=True
    )
    safe_start_x: Mapped[int] = mapped_column(Integer)
    safe_end_x: Mapped[int] = mapped_column(Integer)
    safe_start_y: Mapped[int] = mapped_column(Integer)
    safe_end_y: Mapped[int] = mapped_column(Integer)
