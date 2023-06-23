from enum import Enum
from typing import Any, Optional, Union

from fastapi_events.dispatcher import dispatch as event_dispatcher

from island.core.config import FASTAPI_EVENTS_MIDDLEWARE_ID


def dispatch(
    event_name: Union[str, Enum],
    payload: Optional[Any] = None,
    middleware_id: Optional[int] = None,
):
    return event_dispatcher(
        event_name, payload, middleware_id=FASTAPI_EVENTS_MIDDLEWARE_ID
    )
