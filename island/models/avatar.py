
from pydantic import BaseModel


class Avatar(BaseModel):
    color: int
    head: int
    face: int
    neck: int
    body: int
    hand: int
    feet: int
    photo: int
    flag: int
    transformation: str | None
