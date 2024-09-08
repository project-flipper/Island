from pydantic import BaseModel

from island.models import Response


class Token(BaseModel):
    access_token: str
    token_type: str
    session_key: str | None = None


class TokenResponse(Response[Token]):
    access_token: str | None = None
    token_type: str | None = None
    session_key: str | None = None
