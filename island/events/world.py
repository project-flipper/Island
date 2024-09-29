from fastapi_events.handlers.local import local_handler
from fastapi_events.typing import Event

from island.core.constants.events import EventEnum


@local_handler.register(event_name=str(EventEnum.WORLD_CLIENT_CONNECT))
async def on_world_connection(event: Event) -> None:
    pass


@local_handler.register(event_name=str(EventEnum.WORLD_CLIENT_AUTH))
async def on_world_auth(event: Event) -> None:
    pass


@local_handler.register(event_name=str(EventEnum.WORLD_CLIENT_DISCONNECT))
async def on_world_disconnection(event: Event) -> None:
    pass
