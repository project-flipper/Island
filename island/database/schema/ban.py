import datetime
from sqlalchemy import Column, Integer, Text, Enum, DateTime, ForeignKey, sql
from sqlalchemy.orm import Mapped, mapped_column, relationship
from citext import CIText
from typing import List

from sqlalchemy.sql.sqltypes import Date

from island.database import Base
from island.core.constants.ban import BanType


class Ban(Base):
    __tablename__ = "bans"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    ban_type: Mapped[BanType] = mapped_column(default=BanType.MANUAL_BAN)
    ban_date: Mapped[datetime.datetime] = mapped_column(
        server_default=sql.func.now())
    ban_expire: Mapped[datetime.datetime]
    ban_user: Mapped[int] = mapped_column(default=0)
    ban_comment: Mapped[str]

    user: Mapped["User"] = relationship(back_populates="bans")
