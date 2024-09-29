"""

CLIENT -> Authorization Header  [Verify, //Login//]
       -> event system
           -> Scopes
           -> Priority


scope => single string/Scope, list or tuple or iterable of string/Scope, or callable

@island_event.on(Event(type='PING', scopes=_or(['user:world:auth', 'user:world:init'])))
@has_scope()
@allow_once
@disable
async def handle_ping(ctx, *args, **kwargs):
    pass 

"""

import asyncio
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, WebSocketException
from pydantic import BaseModel, ValidationError
from sqlalchemy import select

from island.core.constants.close import CloseCode
from island.core.constants.events import EventEnum
from island.core.world.player import Player
from island.handlers import dispatch as dispatch_packet
from island.database import ASYNC_SESSION
from island.database.schema.user import UserTable
from island.events import _force_fastapi_events_dispatch_as_task, dispatch as global_dispatch
from island.models.packet import Packet
from island.models.user import MyUser
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
        raise WebSocketException(CloseCode.AUTHENTICATION_TIMEOUT, 'Client did not respond within the required time')

    try:
        token = packet.d.token
        oauth = await get_oauth_data(token)
        return await get_current_user_id(oauth)
    except HTTPException:
        raise WebSocketException(CloseCode.AUTHENTICATION_FAILED, 'Authentication failed')


@router.websocket("/world")
async def world_connection(ws: WebSocket):
    await ws.accept()

    player = None

    try:
        user_id = await handle_authentication(ws)

        if user_id is None:
            return

        async with ASYNC_SESSION() as session:
            user_query = select(UserTable).where(UserTable.id == user_id)

            user = (await session.execute(user_query)).scalar()

            assert user is not None

            my_user = await MyUser.from_table(user)

        player = Player(ws, user=my_user)
        # TODO: Validate connection while invalidating others

        global_dispatch(EventEnum.WORLD_PLAYER_JOIN, player)

        while True:
            packet = await receive_packet(ws)
            with _force_fastapi_events_dispatch_as_task():
                dispatch_packet(player, packet)
    except ValidationError:
        raise WebSocketException(CloseCode.INVALID_DATA, 'Invalid data received')
    except WebSocketDisconnect:
        pass
    except Exception:
        pass

    if player is not None:
        global_dispatch(EventEnum.WORLD_PLAYER_LEAVE, player)
