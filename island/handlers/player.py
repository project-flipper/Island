from typing import Annotated
from fastapi import Depends, WebSocket
from island.handlers import get_user_id, packet_handlers, send_packet
from island.models.action import Action
from island.models.packet import Packet


@packet_handlers.register("player:action")
async def handle_player_action(
    ws: WebSocket, packet: Packet[Action], user_id: Annotated[int, Depends(get_user_id)]
):
    await send_packet(
        ws,
        "player:action",
        Action(
            player_id=user_id,
            frame=packet.d.frame,
            x=packet.d.x,
            y=packet.d.y,
        ),
    )
