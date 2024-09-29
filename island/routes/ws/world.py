"""

CLIENT -> Authorization Header  [Verify, //Login//]
       -> event system
           -> Scopes
           -> Priority


scope => single string/Scope, list or tuple or iterable of string/Scope, or callable

@island_event.on(Event(type="PING", scopes=_or(["user:world:auth", "user:world:init"])))
@has_scope()
@allow_once
@disable
async def handle_ping(ctx, *args, **kwargs):
    pass 

"""

import asyncio
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, WebSocketException
from loguru import logger
from pydantic import BaseModel, ValidationError

from island.core.constants.close import CloseCode
from island.core.constants.events import EventEnum
from island.handlers import dispatch as dispatch_packet
from island.events import _force_fastapi_events_dispatch_as_task, dispatch as global_dispatch
from island.models.packet import Packet
from island.utils.auth import get_current_user_id, get_oauth_data

router = APIRouter()

class AuthData(BaseModel):
    token: str

async def receive_packet[P: Packet](ws: WebSocket, *, cls: type[P] = Packet) -> P:
    return cls.model_validate(await ws.receive_json())

async def handle_authentication(ws: WebSocket) -> int | None:
    try:
        async with asyncio.timeout(15):
            packet = await receive_packet(ws, cls=Packet[AuthData])
    except asyncio.TimeoutError:
        raise WebSocketException(CloseCode.AUTHENTICATION_TIMEOUT, "Client did not respond within the required time")

    try:
        token = packet.d.token
        oauth = get_oauth_data(token)
        return get_current_user_id(oauth)
    except HTTPException:
        raise WebSocketException(CloseCode.AUTHENTICATION_FAILED, "Authentication failed")


@router.websocket("/world")
async def world_connection(ws: WebSocket):
    await ws.accept()

    global_dispatch(EventEnum.WORLD_CLIENT_CONNECT, ws)

    try:
        user_id = await handle_authentication(ws)

        if user_id is None:
            return

        # TODO: Validate connection while invalidating others

        ws.state.user_id = user_id

        global_dispatch(EventEnum.WORLD_CLIENT_AUTH, ws)

        while True:
            packet = await receive_packet(ws)
            with _force_fastapi_events_dispatch_as_task():
                dispatch_packet(ws, packet)
    except ValidationError:
        raise WebSocketException(CloseCode.INVALID_DATA, "Invalid data received")
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.opt(exception=e).error("An error has occurred inside a WebSocket connection")

    global_dispatch(EventEnum.WORLD_CLIENT_DISCONNECT, ws)
