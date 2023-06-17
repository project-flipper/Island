from pydantic.generics import GenericModel
from pydantic import BaseModel
from typing import TypeVar, Optional, Generic, Any

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
