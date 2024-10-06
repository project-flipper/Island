import random
from typing import Annotated, Any
from fastapi import Depends, WebSocket
from pydantic import BaseModel
from island.database.schema.user import UserTable
from island.handlers import packet_handlers, send_packet, get_current_user
from island.models.action import Action
from island.models.packet import Packet
from island.models.player import Player
from island.models.user import User


class RoomJoinData(BaseModel):
    room_id: int
    x: float | None = None
    y: float | None = None


class RoomJoinResponse(BaseModel):
    room_id: int
    players: list


DEFAULT_ACTION = Action(frame=0)
SPAWN_ROOMS = [
    100,  # town
    200,  # village
    230,  # mtn
    300,  # plaza
    400,  # beach
    800,  # dock
    801,  # forts
    802,  # rink
    805,  # berg
    807,  # shack
    809,  # forest
    810,  # cove
]  # TODO: get from crumbs instead and verify if full


async def send_packet_to_room(room_id: int, op: str, d: Any):
    pass

def get_safe_coordinates(room_id: int) -> tuple[float, float]:
    return 800, 800


@packet_handlers.register("room:join")
async def handle_room_join(
    ws: WebSocket,
    packet: Packet[RoomJoinData],
    user: Annotated[UserTable, Depends(get_current_user)],
):
    safe = get_safe_coordinates(packet.d.room_id)
    x = packet.d.x or safe[0]
    y = packet.d.y or safe[1]

    await send_packet(
        ws,
        "room:join",
        RoomJoinResponse(
            room_id=packet.d.room_id,
            players=[
                Player(
                    user=await User.from_table(user),
                    x=x,
                    y=y,
                    action=DEFAULT_ACTION,
                )
            ],
        ),
    )


@packet_handlers.register("room:spawn")
async def handle_room_spawn(
    ws: WebSocket, packet: Packet, user: Annotated[UserTable, Depends(get_current_user)]
):
    room_id = random.choice(SPAWN_ROOMS)
    # TODO: get available rooms and dispatch a room:join with a safe x, y from crumbs
    safe = get_safe_coordinates(room_id)

    await send_packet(
        ws,
        "room:join",
        RoomJoinResponse(
            room_id=room_id,
            players=[
                Player(
                    user=await User.from_table(user),
                    x=safe[0],
                    y=safe[1],
                    action=DEFAULT_ACTION,
                )
            ],
        ),
    )