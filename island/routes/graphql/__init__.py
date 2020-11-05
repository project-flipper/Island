from fastapi import APIRouter

from island.routes.graphql import user, world

router = APIRouter()
router.include_router(
    user.router,
    prefix="/user",
    tags=["UserQL", "GraphQL"]
)
router.include_router(
    world.router,
    prefix="/world",
    tags=["WorldQL", "GraphQL"]
)
