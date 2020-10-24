from pydantic import BaseModel, GenericModel
from typing import TypeVar, Optional

T = TypeVar("T")

class Response(GenericModel[T]):
    data: Optional[T] = None
    error: Optional = None 

    success:bool 