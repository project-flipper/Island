from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from pydantic import ValidationError
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def http422_error_handler(
    _: Request,
    exc: Exception,
) -> JSONResponse:
    """Intercept any/all ValidationError and return a CP-compatible JSON response.

    Args:
        _ (Request)
        exc (Union[RequestValidationError, ValidationError])

    Returns:
        JSONResponse
    """
    assert isinstance(exc, (RequestValidationError, ValidationError))

    return JSONResponse(
        jsonable_encoder(
            {"has_error": True, "success": False, "data": None, "error": exc.errors()}
        ),
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )


validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": "{0}ValidationError".format(REF_PREFIX)},
    },
}
