from fastapi.security.utils import get_authorization_scheme_param
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request
from typing import Dict, Optional
from jose import jwt

from island.core.world import WorldBase
from island.utils.auth import SECRET_KEY, JWT_ALGORITHM

class WorldMiddleware:

    worlds: Dict[str, WorldBase] = dict()

    def __init__(self, app: ASGIApp):
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] in ("http", "websocket"):
            req: Request = Request(scope, receive)
            world = self.world_from_token(await self.retrieve_oauth_token(req))

            if world is not None:
                scope["world"] = world

        await self._app(scope, receive, send)

    def world_from_token(self, token) -> Optional[WorldBase]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            world_id = payload.get("world_id", None)
            
            return self.worlds.get(world_id, None)
        except:
            return None
    
    async def retrieve_oauth_token(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            return None  

        return param