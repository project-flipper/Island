from fastapi import APIRouter
from island.utils.routes import get_graphql_routers
from island.routes import graphql


router = APIRouter()
router.include_router(get_graphql_routers(graphql))
