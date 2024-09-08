from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

from island.database import Base


if TYPE_CHECKING:
    from island.database.schema.user import UserTable


class AvatarTable(Base):
    __tablename__ = "avatars"

    id: Mapped[int] = mapped_column(primary_key=True)
    color: Mapped[int] = mapped_column(default=1)
    head: Mapped[int] = mapped_column(default=0)
    face: Mapped[int] = mapped_column(default=0)
    neck: Mapped[int] = mapped_column(default=0)
    body: Mapped[int] = mapped_column(default=0)
    hand: Mapped[int] = mapped_column(default=0)
    feet: Mapped[int] = mapped_column(default=0)
    photo: Mapped[int] = mapped_column(default=0)
    flag: Mapped[int] = mapped_column(default=0)
    transformation: Mapped[str] = mapped_column(nullable=True)

    user: Mapped["UserTable"] = relationship(back_populates="avatar")
