from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import BaseModel


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:

    if isinstance(exc.detail, BaseModel):
        return JSONResponse(
            {
                "hasError": True,
                "success": False,
                "data": None,
                "error": jsonable_encoder(exc.detail)
            }, 
            status_code=exc.status_code
        )

    return JSONResponse(
        {
            "hasError": True,
            "success": False,
            "data": None,
            "error": str(exc.detail)
        }, 
        status_code=exc.status_code
    )