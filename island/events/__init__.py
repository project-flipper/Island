from contextlib import contextmanager
from enum import Enum
from typing import Any, Generator

from fastapi_events import in_req_res_cycle
from fastapi_events.dispatcher import dispatch as event_dispatcher

from island.core.config import FASTAPI_EVENTS_MIDDLEWARE_ID

__all__ = ("_force_fastapi_events_dispatch_as_task", "dispatch")


@contextmanager
def _force_fastapi_events_dispatch_as_task() -> Generator:
    token = in_req_res_cycle.set(False)
    yield
    in_req_res_cycle.reset(token)


def dispatch(
    event_name: str | Enum,
    payload: Any | None = None,
    middleware_id: int | None = None,
):
    return event_dispatcher(
        str(event_name), payload, middleware_id=FASTAPI_EVENTS_MIDDLEWARE_ID
    )
