from fastapi import APIRouter, Depends, Request, Response, status
from starlette.endpoints import WebSocketEndpoint

router = APIRouter()


@router.websocket_route("/<world_key>")
class WorldEndpoint(WebSocketEndpoint):
    pass
