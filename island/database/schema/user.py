from sqlalchemy import Column, Integer, String, Text, ARRAY, DateTime, sql
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
from citext import CIText
from typing import List

from island.database import Base
from island.core.constants.scope import Scope
from island.core.config import DATABASE_SECRET_KEY


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(12), nullable=False, unique=True)
    nickname = Column(String(20), nullable=False)
    password = Column(Text(), nullable=False)
    email = Column(
        StringEncryptedType(String, DATABASE_SECRET_KEY, AesEngine, "pkcs5"),
        nullable=False,
    )

    created_timestamp = Column(
        DateTime, server_default=sql.func.now(), nullable=False)
    updated_timestamp = Column(DateTime, onupdate=sql.func.now())

    _scopes = Column("scopes", ARRAY(String(30)),
                     nullable=False, server_default="{}")

    @property
    def scopes(self) -> List[Scope]:
        return list(map(Scope, self._scopes))
