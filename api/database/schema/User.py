from sqlalchemy import Column, Integer, String

from api.database import Base # pylint: disable=import-error

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(12), nullable=False, unique=True)
    nickname = Column(String(20), nullable=False)
