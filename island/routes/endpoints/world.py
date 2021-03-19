from fastapi import Depends, status, APIRouter, Response, Request
from starlette.endpoints import WebSocketEndpoint

router = APIRouter()
@router.websocket_route("/<world_key>")
class WorldEndpoint(WebSocketEndpoint):
    pass