import sys

import sentry_sdk
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi_events.handlers.local import local_handler
from fastapi_events.middleware import EventHandlerASGIMiddleware
from loguru import logger
from pydantic import ValidationError
from sentry_sdk.integrations.loguru import LoguruIntegration
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette_context.middleware import RawContextMiddleware

from island import events
from island.core.config import (
    ALLOWED_HOSTS,
    API_PREFIX,
    API_VERSION,
    DEBUG,
    FASTAPI_EVENTS_MIDDLEWARE_ID,
    SENTRY_DSN,
)
from island.core.error.http_error import http_error_handler
from island.core.error.validation_error import http422_error_handler
from island.core.lifespan import manage_app_lifespan
from island.middlwares.world import WorldMiddleware
from island.routes import router
from island.utils.routes import get_modules

print(
    r"""


   ,---,              ,--,
,`--.' |            ,--.'|                                 ,---,
|   :  :            |  | :                     ,---,     ,---.'|
:   |  '  .--.--.   :  : '                 ,-+-. /  |    |   | :
|   :  | /  /    '  |  ' |     ,--.--.    ,--.'|'   |    |   | |
'   '  ;|  :  /`./  '  | |    /       \  |   |  ,"' |  ,--.__| |
|   |  ||  :  ;_    |  | :   .--.  .-. | |   | /  | | /   ,'   |
'   :  ; \  \    `. '  : |__  \__\/: . . |   | |  | |.   '  /  |
|   |  '  `----.   \|  | '.'| ," .--.; | |   | |  |/ '   ; |:  |
'   :  | /  /`--'  /;  :    ;/  /  ,.  | |   | |--'  |   | '/  '
;   |.' '--'.     / |  ,   /;  :   .'   \|   |/      |   :    :|
'---'     `--'---'   ---`-' |  ,     .-./'---'        \   \  /
                             `--`---'                  `----'

"""
)


def catch_exceptions():
    sys.excepthook = lambda _type, message, stack: (
        logger.opt(exception=(_type, message, stack)).error("Uncaught Exception")
        if not issubclass(_type, (ValidationError, RequestValidationError))
        else logger.error("Validation error occured")
    )


def initialize_sentry():
    sentry_sdk.init(
        dsn=str(SENTRY_DSN),
        traces_sample_rate=1.0,  # 1.0 => 100% capture rate
        integrations=[LoguruIntegration()],
    )


def get_application() -> FastAPI:
    catch_exceptions()
    initialize_sentry()

    logger.debug("docs_url: {}", f"{API_PREFIX}/docs")
    logger.debug("redoc_url: {}", f"{API_PREFIX}/redocs")
    application = FastAPI(
        debug=DEBUG,
        title="Island Server",
        description="Web API and WS endpoint for ClubPenguin HTML5 client",
        version=API_VERSION,
        docs_url=f"{API_PREFIX}/docs",
        redoc_url=f"{API_PREFIX}/redocs",
        lifespan=manage_app_lifespan
    )

    _prefix = f"{API_PREFIX}"

    logger.info(f"Island version {API_VERSION}")
    logger.info(f"Island API endpoint prefix {_prefix}")
    logger.info(f"Island setting up")

    logger.info("Island adding middlewares")

    logger.debug("Island adding CORS Middleware")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["*"],
    )

    logger.debug("Island adding Event Handler ASGI Middleware")
    application.add_middleware(
        EventHandlerASGIMiddleware,
        handlers=[local_handler],
        middleware_id=FASTAPI_EVENTS_MIDDLEWARE_ID,
    )

    logger.debug("Island adding Starlette Context Middleware")
    application.add_middleware(RawContextMiddleware)

    logger.debug("Island adding World Manager Middleware")
    application.add_middleware(WorldMiddleware)

    logger.info("Island adding startup and shutdown events")

    logger.info("Island adding exception handlers")

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.add_exception_handler(ValidationError, http422_error_handler)

    logger.info("Island adding routers")

    application.include_router(router, prefix=_prefix)

    logger.info("Island adding events")

    get_modules(events, global_namespace="ISLAND_EVENTS_LIST")

    logger.info("Island setup complete")
    logger.info("Island is ready to be started in a ASGI service")

    return application


app = get_application()


@app.get("/sentry-test")
async def trigger_error_error():
    division_by_zero = 1 / 0


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", log_level="debug", reload=True)
