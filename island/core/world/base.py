from pydantic import BaseModel
from typing import List
from starlette.websockets import WebSocket

from island.core.constants.scope import Scope

class WorldMeta(BaseModel):
    id: int
    name: str
    capacity: int
    lang: int
    scopes: List[Scope]
    grant_scopes: List[Scope]
    access_key: str

    class Config:
        orm_mode = True

class WorldBase(BaseModel):
    
    meta: WorldMeta
    world_key: str
    clients: List[WebSocket] 

    def __init__(self):
        pass

    class Config:
        arbitrary_types_allowed = True