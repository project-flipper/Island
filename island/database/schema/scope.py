from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from citext import CIText

from island.database import Base # pylint: disable=import-error

class Scope(Base):
    __tablename__ = 'scopes'

    id = Column(Integer, primary_key=True)

    tag = Column(CIText(), nullable=False, unique=True)
    description = Column(Text(), nullable=False, default="Scope TAG for JWT Token")

    group_id = Column(Integer, ForeignKey('scopes.id'), nullable=True)
    group = relationship("Scope")

    def __str__(self):
        return self.tag.lower()

class UserScope(Base):
    __tablename__ = "user_scopes"

    user_id = Column(Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False, primary_key=True)
    scope_id = Column(Integer, ForeignKey("scopes.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False, primary_key=True)

    @property
    async def scope(self):
        return await Scope.query.where(Scope.id == self.scope_id).gino.first()

    @property
    async def tag(self):
        return str(await self.scope)
