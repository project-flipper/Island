from pydantic import BaseModel

from island.database import ASYNC_SESSION
from island.database.schema.user import UserTable
from island.models.avatar import Avatar
from island.models.presence import Presence
from island.models.relationship import Relationship
from island.models.membership import Membership


class BaseUser(BaseModel):
    id: int
    username: str
    nickname: str
    avatar: Avatar
    member: Membership | None
    igloo_id: int | None
    mascot_id: int | None


class User(BaseUser):
    relationship: Relationship | None
    public_stampbook: bool
    presence: Presence | None

    @classmethod
    async def from_table(cls, user: UserTable) -> "User":
        return User(
            id=user.id,
            username=user.username,
            nickname=user.nickname,
            avatar=Avatar.model_validate(user.avatar, from_attributes=True),
            member=None,
            igloo_id=0,
            mascot_id=None,
            relationship=None,
            public_stampbook=False,
            presence=None,
        )


class MyUser(BaseUser):
    igloo_id: int
    is_moderator: bool
    is_stealth: bool

    @classmethod
    async def from_table(cls, user: UserTable) -> "MyUser":
        return MyUser(
            id=user.id,
            username=user.username,
            nickname=user.nickname,
            avatar=Avatar.model_validate(user.avatar, from_attributes=True),
            member=None,
            igloo_id=0,
            mascot_id=None,
            is_moderator=True,
            is_stealth=False,
        )
