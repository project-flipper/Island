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


class UserScope(Base):
    __tablename__ = "user_scopes"

    user_id = Column(Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    scope_id = Column(Integer, ForeignKey("scopes.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    user = relationship("User")
    scope = relationship("Scope")
