from fastapi import APIRouter

from island.routes.graphql import user

router = APIRouter()
router.include_router(
    user.router,
    prefix="/user",
    tags=["UserQL"]
)
