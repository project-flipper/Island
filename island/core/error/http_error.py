from typing import Any
from starlette.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi import Request
from fastapi.responses import JSONResponse

def maybe_encode_model(model: Any) -> Any:
    return jsonable_encoder(model) if isinstance(model, BaseModel) else str(model)

async def http_error_handler(_: Request, exc: Exception) -> JSONResponse:
    """Intercept any/all HTTPExceptions from FastAPI, and return a CP compatible JSON response.

    Args:
        _ (Request)
        exc (Exception)

    Returns:
        JSONResponse
    """
    assert isinstance(exc, HTTPException)

    if isinstance(exc.detail, list):
        return JSONResponse(
            {
                "has_error": True,
                "success": False,
                "data": None,
                "error": [maybe_encode_model(exc) for exc in exc.detail],
            },
            status_code=exc.status_code,
        )

    return JSONResponse(
        {"has_error": True, "success": False, "data": None, "error": maybe_encode_model(exc.detail)},
        status_code=exc.status_code,
    )
