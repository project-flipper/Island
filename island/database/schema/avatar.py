from sqlalchemy import Column, ForeignKey, Integer
from island.database import Base


class Avatar(Base):
    __tablename__ = "avatars"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    color = Column(Integer, default=1, nullable=False)
