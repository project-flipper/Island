from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from island.database import Base


class GameStringsTable(Base):
    __tablename__ = "game_strings"

    key: Mapped[str] = mapped_column(Text, primary_key=True)
    value: Mapped[str] = mapped_column(String(256))
    category: Mapped[str] = mapped_column(String(256))


class GameOptionsTable(Base):
    __tablename__ = "game_options"

    key: Mapped[str] = mapped_column(String(256), primary_key=True)
    value: Mapped[str] = mapped_column(Text)
