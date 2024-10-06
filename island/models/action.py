from pydantic import BaseModel


class Action(BaseModel):
    player_id: int | None = None
    frame: int
    x: float | None = None
    y: float | None = None
