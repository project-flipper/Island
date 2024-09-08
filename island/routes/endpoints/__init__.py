from fastapi import APIRouter

from island.routes.endpoints import auth, users, worlds

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(worlds.router, prefix="/worlds", tags=["Worlds"])
