from sqlalchemy import Column, Integer, String, Text, ARRAY, Enum
from citext import CIText
from typing import List

from island.database import Base
from island.core.constants.scope import Scope


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(12), nullable=False, unique=True)
    nickname = Column(String(20), nullable=False)
    password = Column(Text(), nullable=False)
    email = Column(CIText(), nullable=False)

    _scopes = Column("scopes", ARRAY(String(30)),
                     nullable=False, server_default="{}")

    @property
    def scopes(self) -> List[Scope]:
        return list(map(Scope, self._scopes))
