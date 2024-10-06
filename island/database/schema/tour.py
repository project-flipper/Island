from __future__ import annotations

from sqlalchemy import String, Text, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from island.database import Base

class TourMessagesTable(Base):
    __tablename__ = "tour_messages"
    
    key: Mapped[str] = mapped_column(String(256), primary_key=True)
    message: Mapped[str] = mapped_column(Text)
    language: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
