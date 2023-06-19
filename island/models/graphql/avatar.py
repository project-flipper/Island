from typing import Optional
from pydantic import BaseModel
import strawberry


class Avatar(BaseModel):
    color: int


@strawberry.experimental.pydantic.type(model=Avatar, all_fields=True)
class AvatarType:
    pass
