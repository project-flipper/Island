
from enum import Enum

from pydantic import BaseModel


class RelationshipType(Enum):
    IGNORED = 'ignored'
    PENDING = 'pending'
    FRIEND = 'friend'
    BEST_FRIEND = 'bestfriend'

class Relationship(BaseModel):
    type: RelationshipType
    since: str
