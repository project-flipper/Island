from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request

class WorldMiddleware:
    def __init__(self, app: ASGIApp):
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        req = Request(scope, receive)
        print("url:", req.url.path, "scope", scope)
        await self._app(scope, receive, send)