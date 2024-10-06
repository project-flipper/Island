from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, String
from island.database import Base


class GameTable(Base):
    __tablename__ = "games"

    key: Mapped[str] = mapped_column(String(256), primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    path: Mapped[str] = mapped_column(String(256))
    room_id: Mapped[int] = mapped_column(Integer)
    music_id: Mapped[int] = mapped_column(Integer)
    stamp_set_id: Mapped[int] = mapped_column(Integer)
    show_player_in_room: Mapped[bool] = mapped_column(default=False)
