from typing import Any, Dict, Optional

from pydantic import BaseModel

from island.models.error import Error


class Action(BaseModel):
    """Generic Action-model for incoming and outgoing event(s).

    Usage:
        Can be used either directly, as raw-action class/object,
        or the class can be extended to give more information
        about the data being received/sent.

        Example:

        class ExampleData(BaseModel):
            example_string_data: str
            example_optional_data: int = 100
            example_optional_list: Optional[List[int]]

        class ExampleAction(Action): # <-- inherit from [Action] class
            d: ExampleData # <-- giving more information on data structure for [d].

    Args:
        BaseModel ([type]): [description]
    """

    op: str  # action [category:event]
    d: Optional[Dict[str, Any]]  # event data
    e: Optional[
        Error
    ]  # event error data, almost only used on replies to action-request
