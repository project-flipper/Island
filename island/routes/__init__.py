from typing import Annotated

from fastapi import APIRouter, Depends, Header
from starlette_context import request_cycle_context

from island.routes import endpoints
from island.routes.ws.world import router as world_router


__all__ = ("router", "world_router")


async def language_context_dependency(
    accept_language: Annotated[str | None, Header()] = None
):
    data = {"locale": accept_language}

    with request_cycle_context(data):
        yield


router = APIRouter(dependencies=[Depends(language_context_dependency)])
router.include_router(endpoints.router, tags=["REST Endpoints"])
