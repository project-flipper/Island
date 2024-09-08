from enum import unique

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY

from island.core.constants.scope import Scope
from island.database import Base


class World(Base):
    __tablename__ = "worlds"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    capacity: Mapped[int] = mapped_column(default=200)
    lang: Mapped[int] = mapped_column(default=1)
    is_safe: Mapped[bool] = mapped_column(default=False)

    access_key: Mapped[str] = mapped_column(String(32), unique=True)
    grant_scopes: Mapped[list[Scope]] = mapped_column(
        ARRAY(String(30)), server_default="{}"
    )
    scopes: Mapped[list[Scope]] = mapped_column(ARRAY(String(30)), server_default="{}")
