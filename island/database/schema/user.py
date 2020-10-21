from sqlalchemy import Column, Integer, String, Text
from citext import CIText

from island.database import Base # pylint: disable=import-error

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(12), nullable=False, unique=True)
    nickname = Column(String(20), nullable=False)
    password = Column(Text(), nullable=False)
    email = Column(CIText(), nullable=False)