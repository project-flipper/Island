from sqlalchemy import Column, Integer, Text, Enum, DateTime, ForeignKey, sql
from citext import CIText
from typing import List

from sqlalchemy.sql.sqltypes import Date

from island.database import Base
from island.core.constants.ban import BanType


class Ban(Base):
    __tablename__ = "bans"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) # banned user

    ban_type = Column(Enum(BanType), nullable=False, default=BanType.MANUAL_BAN)
    ban_date = Column(DateTime, server_default=sql.func.now(), nullable=False)
    ban_expire = Column(DateTime, nullable=False)
    ban_user = Column(Integer, default=0, nullable=False) # moderator who banned (0 for sys)
    ban_comment = Column(Text, nullable=False)
