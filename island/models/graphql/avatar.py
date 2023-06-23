from typing import Optional

import strawberry
from pydantic import BaseModel


class Avatar(BaseModel):
    color: int


@strawberry.experimental.pydantic.type(model=Avatar, all_fields=True)
class AvatarType:
    pass
