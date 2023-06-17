from typing import Optional
from pydantic import BaseModel
import strawberry


class User(BaseModel):
    id: int
    username: Optional[str]
    nickname: str


@strawberry.experimental.pydantic.type(model=User, all_fields=True)
class UserType:
    pass
