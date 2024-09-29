import asyncio
from typing import Any, Callable
from fastapi import WebSocket

from fastapi.websockets import WebSocketState
from fastapi_events.typing import Event

from island.models.packet import Packet
from island.models.user import MyUser

_default_check = lambda e: True

class Player:
    def __init__(self, ws: WebSocket, *, user: MyUser) -> None:
        self.ws = ws
        self.user = user

    async def wait(self, op: str, *, check: Callable[[Event], bool] = _default_check) -> Event:
        from island.handlers import packet_handlers

        loop = asyncio.get_event_loop()
        future: asyncio.Future[Event] = loop.create_future()

        def func(event: Event):
            try:
                if check(event):
                    future.set_result(event)
                    packet_handlers.unregister(op, func)
            except Exception:
                return

        packet_handlers.register(op, func)
        return await future

    def is_connected(self) -> bool:
        return self.ws.client_state is WebSocketState.CONNECTED

    async def send(self, op: str, d: Any) -> None:
        packet = Packet(op=op, d=d)
        await self.ws.send_json(packet.model_dump())

    async def disconnect(self, code: int, reason: str) -> None:
        await self.ws.close(code, reason)
