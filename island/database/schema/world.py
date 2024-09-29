from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY

from island.core.constants.scope import Scope
from island.database import Base


class WorldTable(Base):
    __tablename__ = "worlds"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    capacity: Mapped[int] = mapped_column(default=200)
    lang: Mapped[int] = mapped_column(default=1)
    is_safe: Mapped[bool] = mapped_column(default=False)
    url: Mapped[str] = mapped_column()

    access_key: Mapped[str] = mapped_column(String(32), unique=True)
    _grant_scopes: Mapped[list[str]] = mapped_column(
        "grant_scopes", ARRAY(String(30)), server_default="{}"
    )
    _scopes: Mapped[list[str]] = mapped_column(
        "scopes", ARRAY(String(30)), server_default="{}"
    )

    @property
    def grant_scopes(self) -> list[Scope]:
        # type: ignore
        return list(map(Scope, self._grant_scopes))

    @property
    def scopes(self) -> list[Scope]:
        return list(map(Scope, self._scopes))
