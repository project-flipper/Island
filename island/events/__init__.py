from enum import Enum
from typing import Any

from fastapi_events.dispatcher import dispatch as event_dispatcher

from island.core.config import FASTAPI_EVENTS_MIDDLEWARE_ID


def dispatch(
    event_name: str | Enum,
    payload: Any | None = None,
    middleware_id: int | None = None,
):
    return event_dispatcher(
        str(event_name), payload, middleware_id=FASTAPI_EVENTS_MIDDLEWARE_ID
    )
