from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class Error(BaseModel):
    error_type: str
    error_code: int
    error_description: str


class Response(GenericModel, Generic[T]):
    data: Optional[T] = None
    error: Error = None

    success: bool
    hasError: bool = False
