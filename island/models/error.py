from pydantic import BaseModel


class Error(BaseModel):
    error_type: str
    error_code: int
    error_description: str


class BanError(Error):
    error_type = "user.banned"
    ban_dur: int
