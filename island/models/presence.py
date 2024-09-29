from pydantic import BaseModel


class Presence(BaseModel):
    world_id: int
    room_id: int
    is_mobile: bool
