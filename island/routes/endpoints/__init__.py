from fastapi import APIRouter

from island.routes.endpoints import auth, world

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(world.router, prefix="/world", tags=["World"])
