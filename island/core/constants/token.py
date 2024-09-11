from enum import Enum


class JWTTokenType(Enum):
    HS256 = "HS256"
    RS256 = "RS256"
