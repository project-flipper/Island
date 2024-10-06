from __future__ import annotations

from sqlalchemy import String, Text, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from island.database import Base

class GameStringsTable(Base):
    __tablename__ = "game_strings"

    key: Mapped[str] = mapped_column(Text, primary_key=True)
    value: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(256))
    language: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
