from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/{config}.json")
async def get_global_config(config: str) -> FileResponse:
    return FileResponse(f"web_service/{config}.json")


@router.get("/{locale}/{config}.json")
async def get_local_config(locale: str, config: str) -> FileResponse:
    return FileResponse(f"web_service/{locale}/{config}.json")

