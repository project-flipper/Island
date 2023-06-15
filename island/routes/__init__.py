from fastapi import APIRouter

from island.routes import endpoints

router = APIRouter()
# router.include_router(graphql.router, prefix="/data", tags=["GraphQL"])
router.include_router(endpoints.router, tags=["Endpoints"])
