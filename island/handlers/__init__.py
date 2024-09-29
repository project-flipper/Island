from __future__ import annotations

import asyncio
import fnmatch
import functools
import inspect
from contextlib import AsyncExitStack
from contextvars import ContextVar
from typing import Annotated, Any, Callable

from fastapi import Depends, WebSocket, WebSocketException
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import (
    get_dependant,
    get_parameterless_sub_dependant,
    solve_dependencies,
)
from fastapi.params import Depends as ParamDepends
from fastapi_events.dispatcher import dispatch as event_dispatcher
from fastapi_events.handlers.base import BaseEventHandler
from fastapi_events.typing import Event
from loguru import logger
from pydantic import ValidationError

from island.core.config import WORLD_PACKETS_MIDDLEWARE_ID
from island.core.constants.close import CloseCode
from island.database.schema.user import UserTable
from island.models.packet import Packet

_event: ContextVar[Event] = ContextVar("event")


class DelayedInjection:
    def __init__(self, _cb: Callable[[inspect.Parameter], Any]) -> None:
        self._callback = _cb

    def __call__(self, param) -> Any:
        return self._callback(param)

class PacketHandler(BaseEventHandler):
    def __init__(self):
        self._registry: dict[str, list[Callable]] = {}

    def register(
        self,
        op: str = "*",
        func: Callable | None = None,
        *,
        dependencies: list[ParamDepends] | None = None,
    ):
        """Register a packet handler.

        Usage:
            from island.core.world import packet_handlers

            @packet_handlers.register("my:event") # Register a handler as a decorator
            async def handle_my_event(event: Event):
                event_name, payload = event
                print(f"Received event {event_name} with payload {payload}")

        Args:
            :param op: The operation to be associated with the handler. Use "*", the default value, to match all packets.
            :param func: The function to be registered as a handler.  Typically, you would use `register` as a decorator and omit this argument.
        """

        def wrapped(_func):
            self._register_handler(op, _func, dependencies)
            return _func

        if func is None:
            return wrapped

        return wrapped(func)

    def unregister(self, op: str, func: Callable) -> None:
        """Unregisters a packet handler.

        Args:
            :param op: The operation to be associated with the handler. Use "*", the default value, to match all packets.
            :param func: The function to be registered as a handler.  Typically, you would use `register` as a decorator and omit this argument.
        """
        self._unregister_handler(op, func)

    async def handle(self, event: Event) -> None:
        _event.set(event)

        event_name, payload = event
        ws: WebSocket = payload[0]
        packet: Packet = payload[1]

        handlers = self._get_handlers_for_event(event_name=event_name)

        if len(handlers) == 0:
            logger.warning(f"No handlers found for {event_name}")

        for handler in handlers:
            async with AsyncExitStack() as cm:
                # resolve dependencies
                dependant: Dependant = getattr(handler, "__dependant__")

                if not dependant.call:
                    continue

                try:
                    solved = await solve_dependencies(
                        request=ws,
                        dependant=dependant,
                        async_exit_stack=cm,
                        body=packet.d,
                        dependency_overrides_provider=ws.app,
                        embed_body_fields=True,
                    )

                    if inspect.iscoroutinefunction(dependant.call):
                        await dependant.call(**solved.values)
                    else:
                        loop = asyncio.get_event_loop()
                        await loop.run_in_executor(
                            None, functools.partial(dependant.call, **solved.values)
                        )
                except ValidationError:
                    logger.opt(exception=e).error(e)
                    await ws.close(CloseCode.INVALID_DATA, "Invalid data received")
                except WebSocketException as e:
                    await ws.close(e.code, e.reason)
                except Exception as e:
                    logger.opt(exception=e).error("An error occurred when dispatching a packet")

    def _register_handler(
        self,
        event_name: str,
        func: Callable,
        dependencies: list[ParamDepends] | None = None,
    ):
        if not isinstance(event_name, str):
            event_name = str(event_name)

        if event_name not in self._registry:
            self._registry[event_name] = []

        path_format = f"packet:{event_name}"

        self._inject_params(func)

        dependant = get_dependant(path=path_format, call=func)
        dependencies = list(dependencies or [])
        for depends in dependencies[::-1]:
            dependant.dependencies.insert(
                0,
                get_parameterless_sub_dependant(depends=depends, path=path_format),
            )
        setattr(func, "__dependant__", dependant)

        self._registry[event_name].append(func)

    def _get_injection_params(self) -> dict[Any, Any]:
        return {
            Event: EventDep,
            Packet: PacketDep,
            "packet": DelayedInjection(lambda p: Annotated[p.annotation, Depends(get_custom_packet(p.annotation))])
        }

    def _inject_params(self, func: Callable) -> None:
        sig = inspect.signature(func)
        _injections = self._get_injection_params()

        params = []
        for param in sig.parameters.values():
            to_inject = None

            if param.annotation in _injections:
                to_inject = _injections[param.annotation]
            elif param.name in _injections:
                to_inject = _injections[param.name]

            if to_inject is not None:
                if isinstance(to_inject, DelayedInjection):
                    to_inject = to_inject(param)
                param = param.replace(annotation=to_inject)

            params.append(param)

        sig = sig.replace(parameters=params)

        if inspect.ismethod(func):
            func.__func__.__signature__ = sig
        else:
            func.__signature__ = sig

    def _get_handlers_for_event(self, event_name):
        if not isinstance(event_name, str):
            event_name = str(event_name)

        # TODO consider adding a cache
        handlers = []
        for event_name_pattern, registered_handlers in self._registry.items():
            if fnmatch.fnmatch(event_name, event_name_pattern):
                handlers.extend(registered_handlers)

        return handlers

    def _unregister_handler(self, event_name, func):
        if not isinstance(event_name, str):
            event_name = str(event_name)

        if event_name not in self._registry:
            return

        self._registry[event_name].remove(func)


def dispatch(ws: WebSocket, packet: Packet):
    return event_dispatcher(
        str(packet.op), [ws, packet], middleware_id=WORLD_PACKETS_MIDDLEWARE_ID
    )


def get_event() -> Event:
    return _event.get()


EventDep = Annotated[Event, Depends(get_event)]

def get_user_id(ws: WebSocket) -> int:
    return ws.state.user_id

async def get_current_user(user_id: Annotated[int, Depends(get_user_id)]) -> UserTable:
    user = await UserTable.query_by_id(user_id)

    if user is None or user.id != user_id:
        raise WebSocketException(CloseCode.AUTHENTICATION_FAILED, "Authentication failed")

    return user

def get_packet(event=Depends(get_event)) -> Packet:
    return event[1][1]

PacketDep = Annotated[Packet, Depends(get_packet)]

def get_custom_packet(cls = Packet):
    def _wrap(p: PacketDep) -> Packet:
        return cls.model_validate(p.model_dump())
    return _wrap

packet_handlers = PacketHandler()

async def send_packet(ws: WebSocket, op: str, d: Any) -> None:
    await ws.send_text(Packet(op=op, d=d).model_dump_json())
