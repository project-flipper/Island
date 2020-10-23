from fastapi import APIRouter

from island.routes import graphql

router = APIRouter()
router.include_router(
    graphql.router,
    prefix="/data",
    tags=["GraphQL"]
)
