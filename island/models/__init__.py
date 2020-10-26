from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import TypeVar, Optional, Generic, Any

T = TypeVar("T")

class Response(GenericModel, Generic[T]):
    data: Optional[T] = None
    error: Any = None 

    success: bool 
    hasError: bool = False