from fastapi import APIRouter

from island.routes.endpoints import login

router = APIRouter()
router.include_router(
    login.router,
    prefix="/login",
    tags=["Login"]
)
