from island.database.schema.ban import Ban
from pydantic import BaseModel
from island.core.constants.ban import BanType


class Error(BaseModel):
    error_type: str
    error_code: int
    error_description: str


class BanError(Error):
    error_type = "user.banned"
    error_code: BanType
    ban_dur: int
