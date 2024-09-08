from pydantic import BaseModel

from island.core.constants.error import ErrorEnum



class Error(BaseModel):
    error_type: str
    error_code: int | ErrorEnum
    error_description: str


class Response[T](BaseModel):
    data: T | None = None
    error: Error | None = None

    success: bool
    has_error: bool = False
