from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(Token):
    id: str
    username: str