from pydantic import BaseModel


class Presence(BaseModel):
    worldId: int
    roomId: int
    isMobile: bool
