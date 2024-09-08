from starlette.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi import Request
from fastapi.responses import JSONResponse


async def http_error_handler(_: Request, exc: Exception) -> JSONResponse:
    """Intercept any/all HTTPExceptions from FastAPI, and return a CP compatible JSON response.

    Args:
        _ (Request)
        exc (Exception)

    Returns:
        JSONResponse
    """
    assert isinstance(exc, HTTPException)

    if isinstance(exc.detail, BaseModel):
        return JSONResponse(
            {
                "has_error": True,
                "success": False,
                "data": None,
                "error": jsonable_encoder(exc.detail),
            },
            status_code=exc.status_code,
        )

    return JSONResponse(
        {"has_error": True, "success": False, "data": None, "error": str(exc.detail)},
        status_code=exc.status_code,
    )
