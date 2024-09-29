from pydantic import BaseModel


class Action(BaseModel):
    player_id: int | None = None
    frame: int
    from_x: float | None = None
    from_y: float | None = None
    destination_x: float | None = None
    destination_y: float | None = None
