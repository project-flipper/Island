import datetime
from typing import List

from citext import CIText
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Text, sql
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Date

from island.core.constants.ban import BanType
from island.database import Base


class Ban(Base):
    __tablename__ = "bans"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    ban_type: Mapped[BanType] = mapped_column(default=BanType.MANUAL_BAN)
    ban_date: Mapped[datetime.datetime] = mapped_column(server_default=sql.func.now())
    ban_expire: Mapped[datetime.datetime]
    ban_user: Mapped[int] = mapped_column(default=0)
    ban_comment: Mapped[str]

    user: Mapped["User"] = relationship(back_populates="bans")
