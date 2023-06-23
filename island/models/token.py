from typing import Optional

from pydantic import BaseModel

from island.models import Error, Response


class Token(BaseModel):
    access_token: str
    token_type: str
    session_key: Optional[str] = None


class TokenResponse(Response[Token]):
    pass
