from pydantic import BaseModel


class Action(BaseModel):
    player: str | None
    frame: int
    fromX: float | None
    fromY: float | None
    destinationX: float | None
    destinationY: float | None
