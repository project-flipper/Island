from fastapi.security.utils import get_authorization_scheme_param
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request
from typing import Dict, Optional, Tuple
from jose import jwt
from island.utils.auth import SECRET_KEY, JWT_ALGORITHM


class WorldMiddleware:

    def __init__(self, app: ASGIApp):
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] in ("http", "websocket"):
            req: Request = Request(scope, receive)
            oauth_data = await self.retrieve_oauth_token(req)
            #TODO: Check if current app is world app, and if so check if the oauth token is for the world app.
            scope["oauth"] = oauth_data

        await self._app(scope, receive, send)

    async def retrieve_oauth_token(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            return None

        return param
