from typing import Annotated
from fastapi import APIRouter, Depends, Header
from starlette_context import request_cycle_context

from island.routes import auth, avatars, friends, users, web_service, worlds

__all__ = ('router',)

async def language_context_dependency(
    accept_language: Annotated[str | None, Header()] = None
):
    data = {"locale": accept_language}

    with request_cycle_context(data):
        yield


router = APIRouter(dependencies=[Depends(language_context_dependency)])
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(worlds.router, prefix="/worlds", tags=["Worlds"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(avatars.router, prefix="/avatars", tags=["Avatars"])
router.include_router(friends.router, prefix="/friends", tags=["Friends"])
router.include_router(web_service.router, prefix="/web_service", tags=["Web Service"])
