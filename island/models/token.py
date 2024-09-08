from pydantic import BaseModel

from island.models import Error, Response


class Token(BaseModel):
    access_token: str
    token_type: str
    session_key: str | None = None


class TokenResponse(Response[Token]):
    pass
