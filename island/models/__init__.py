from typing import Any, Generic, Optional, TypeVar, Union

from pydantic import BaseModel
from pydantic.generics import GenericModel

from island.core.constants.error import ErrorEnum

T = TypeVar("T")


class Error(BaseModel):
    error_type: str
    error_code: Union[int, ErrorEnum]
    error_description: str


class Response(GenericModel, Generic[T]):
    data: Optional[T] = None
    error: Error = None

    success: bool
    hasError: bool = False
