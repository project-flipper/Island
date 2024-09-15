from typing import TYPE_CHECKING
from sqlalchemy import ARRAY, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from island.core.config import DATABASE_SECRET_KEY
from island.core.constants.scope import Scope
from island.database import Base

if TYPE_CHECKING:
    from island.database.schema.ban import BanTable
    from island.database.schema.avatar import AvatarTable


class UserTable(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(12), unique=True)
    nickname: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(Text())
    email: Mapped[str] = mapped_column(
        StringEncryptedType(String, str(DATABASE_SECRET_KEY), AesEngine, "pkcs5")
    )

    lang: Mapped[int] = mapped_column(default=0)

    _scopes: Mapped[list[str]] = mapped_column(
        "scopes", ARRAY(String(30)), server_default="{}"
    )

    avatar_id: Mapped[int] = mapped_column(ForeignKey("avatars.id"))

    bans: Mapped[list["BanTable"]] = relationship(
        back_populates="user", lazy="selectin"
    )
    avatar: Mapped["AvatarTable"] = relationship(back_populates="user", lazy="selectin")

    @property
    def scopes(self) -> list[Scope]:
        return list(map(Scope, self._scopes))
