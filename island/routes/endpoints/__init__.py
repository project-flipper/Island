from fastapi import APIRouter

from island.routes.endpoints import login, world

router = APIRouter()
router.include_router(login.router, prefix="/login", tags=["Login"])
router.include_router(world.router, prefix="/world", tags=["World"])