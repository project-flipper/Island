from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import ARRAY, ForeignKey, String, Text, func, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, joinedload
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from island.core.config import DATABASE_SECRET_KEY
from island.core.constants.scope import Scope
from island.database import ASYNC_SESSION, Base

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

    bans: Mapped[list[BanTable]] = relationship(
        back_populates="user", lazy="selectin"
    )
    avatar: Mapped[AvatarTable] = relationship(back_populates="user", lazy="joined")

    @property
    def scopes(self) -> list[Scope]:
        return list(map(Scope, self._scopes))

    @classmethod
    async def query_by_id(cls, user_id: int) -> UserTable | None:
        from island.database.schema.ban import BanTable
        async with ASYNC_SESSION() as session:
            user_query = (
                select(UserTable)
                .options(
                    joinedload(UserTable.bans.and_(BanTable.ban_expire > datetime.now()))
                )
                .where(UserTable.id == user_id)
            )

            return (await session.execute(user_query)).scalar()

    @classmethod
    async def query_by_username(cls, username: str) -> UserTable | None:
        from island.database.schema.ban import BanTable
        async with ASYNC_SESSION() as session:
            now = datetime.now()
            user_query = (
                select(UserTable)
                .options(joinedload(UserTable.bans.and_(BanTable.ban_expire > now)))
                .where(func.lower(UserTable.username) == username.lower())
            )

            return (await session.execute(user_query)).scalar()
