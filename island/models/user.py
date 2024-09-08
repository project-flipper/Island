from pydantic import BaseModel

from island.models.avatar import Avatar
from island.models.presence import Presence
from island.models.relationship import Relationship
from island.models.membership import Membership

class BaseUser(BaseModel):
    id: str
    username: str
    nickname: str
    avatar: Avatar
    member: Membership | None
    iglooId: int | None
    mascotId: int | None

class User(BaseUser):
    relationship: Relationship | None
    publicStampbook: bool
    presence: Presence | None

class MyUser(BaseUser):
    moderator: bool
    iglooId: int
    stealth: bool
