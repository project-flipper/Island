from enum import unique
from sqlalchemy import Column, Integer, String, Text, ARRAY, Enum
from typing import List

from island.database import Base
from island.core.constants.scope import Scope

class World(Base):
    __tablename__ = "worlds"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    capacity = Column(Integer, nullable=False, default=200)
    lang = Column(Integer, nullable=False, default=1)
    
    access_key = Column(String(32), unique=True, nullable=False)
    _scopes = Column("scopes", ARRAY(String(30)), nullable=False, server_default="{}")

    @property
    def scopes(self) -> List[Scope]:
        return list(map(Scope, self._scopes))