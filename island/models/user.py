from pydantic import BaseModel

from island.database import ASYNC_SESSION
from island.database.schema.user import UserTable
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

    @classmethod
    async def from_user_table(cls, user: UserTable) -> "User":
        async with ASYNC_SESSION() as session:
            user = await session.merge(user)

            return User(
                id=str(user.id),
                username=user.username,
                nickname=user.nickname,
                avatar=Avatar.model_validate(user.avatar, from_attributes=True),
                member=None,
                iglooId=0,
                mascotId=None,
                relationship=None,
                publicStampbook=False,
                presence=None
            )

class MyUser(BaseUser):
    moderator: bool
    iglooId: int
    stealth: bool

    @classmethod
    async def from_user_table(cls, user: UserTable) -> "MyUser":
        async with ASYNC_SESSION() as session:
            user = await session.merge(user)

            return MyUser(
                id=str(user.id),
                username=user.username,
                nickname=user.nickname,
                avatar=Avatar.model_validate(user.avatar, from_attributes=True),
                member=None,
                iglooId=0,
                mascotId=None,
                moderator=True,
                stealth=False
            )
