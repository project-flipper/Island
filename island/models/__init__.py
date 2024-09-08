from pydantic import BaseModel
from pydantic.generics import GenericModel

from island.core.constants.error import ErrorEnum



class Error(BaseModel):
    error_type: str
    error_code: int | ErrorEnum
    error_description: str


class Response[T](GenericModel):
    data: T | None = None
    error: Error | None = None

    success: bool
    hasError: bool = False
