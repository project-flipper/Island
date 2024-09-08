from pydantic import BaseModel


class Membership(BaseModel):
    since: str
    level: int
