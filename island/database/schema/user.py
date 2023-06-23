from typing import List, Optional

from citext import CIText
from sqlalchemy import (
    ARRAY,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    null,
    sql,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from island.core.config import DATABASE_SECRET_KEY
from island.core.constants.scope import Scope
from island.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(12), unique=True)
    nickname: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(Text())
    email: Mapped[str] = mapped_column(
        StringEncryptedType(String, str(
            DATABASE_SECRET_KEY), AesEngine, "pkcs5")
    )

    _scopes: Mapped[List[str]] = mapped_column(
        "scopes", ARRAY(String(30)), server_default="{}"
    )

    avatar_id: Mapped[int] = mapped_column(ForeignKey("avatars.id"))

    bans: Mapped[List["Ban"]] = relationship(back_populates="user")
    avatar: Mapped["Avatar"] = relationship(back_populates="user")

    @property
    def scopes(self) -> List[Scope]:
        return list(map(Scope, self._scopes))
