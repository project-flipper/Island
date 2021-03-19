from enum import unique
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from typing import List

from island.database import Base
from island.core.constants.scope import Scope


class World(Base):
    __tablename__ = "worlds"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    capacity = Column(Integer, nullable=False, default=200)
    lang = Column(Integer, nullable=False, default=1)
    is_safe = Column(Boolean, nullable=False, default=False)

    access_key = Column(String(32), unique=True, nullable=False)
    _grant_scopes = Column(
        "grant_scopes", ARRAY(String(30)), nullable=False, server_default="{}"
    )
    _scopes = Column("scopes", ARRAY(String(30)),
                     nullable=False, server_default="{}")

    @property
    def grant_scopes(self):
        return list(map(Scope, self._grant_scopes))

    @property
    def scopes(self) -> List[Scope]:
        return list(map(Scope, self._scopes))
