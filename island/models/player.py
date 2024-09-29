from pydantic import BaseModel

from island.models.action import Action
from island.models.user import MyUser, User


class Player(BaseModel):
    user: User | MyUser
    x: float
    y: float
    action: Action
