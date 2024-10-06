from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from island.database import Base
from sqlalchemy import Text

class JokeTable(Base):
    __tablename__ = "jokes"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text)
