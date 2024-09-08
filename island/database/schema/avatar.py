from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

from island.database import Base


if TYPE_CHECKING:
    from island.database.schema.user import UserTable


class AvatarTable(Base):
    __tablename__ = "avatars"

    id: Mapped[int] = mapped_column(primary_key=True)
    color: Mapped[int] = mapped_column(default=1)

    user: Mapped["UserTable"] = relationship(back_populates="avatar")
