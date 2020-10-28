from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from citext import CIText
from typing import List

from island.database import Base # pylint: disable=import-error
from island.database.schema.scope import UserScope

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(12), nullable=False, unique=True)
    nickname = Column(String(20), nullable=False)
    password = Column(Text(), nullable=False)
    email = Column(CIText(), nullable=False)

    @property
    async def scopes(self) -> List[UserScope]:
        """Get list of all children UserScope, joined by `UserScope.user_id == User.id`

        Returns:
            List[UserScope]
        """
        return await UserScope.query.where(UserScope.user_id == self.id).gino.all()
