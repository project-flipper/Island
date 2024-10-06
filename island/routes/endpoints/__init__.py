from fastapi import APIRouter

from island.routes.endpoints import auth, avatars, friends, users, web_service, worlds

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(worlds.router, prefix="/worlds", tags=["Worlds"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(avatars.router, prefix="/avatars", tags=["Avatars"])
router.include_router(friends.router, prefix="/friends", tags=["Friends"])
router.include_router(web_service.router, prefix="/web_service", tags=["Web Service"])
