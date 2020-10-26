from loguru import logger

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from island.core.error.http_error import http_error_handler
from island.core.error.validation_error import http422_error_handler
from island.routes import router
from island.core.config import ALLOWED_HOSTS, API_PREFIX, DEBUG, SECRET_KEY, API_VERSION
from island.core.events import create_start_app_handler, create_stop_app_handler

print ("""
                                                                 
                                                                 
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
                                                                 
       """)

def get_application() -> FastAPI:
   application = FastAPI(
      debug = DEBUG,
      title = "Island Server",
      description = "Web API and WS endpoint for ClubPenguin HTML5 client",
      version = API_VERSION,
      docs_url = f"/{API_PREFIX.strip('/')}/docs",
      redoc_url = f"/{API_PREFIX.strip('/')}/redocs",
   )

   logger.info(f"Island version {API_VERSION}")
   logger.info(f"Island API endpoint prefix /{API_PREFIX}/")
   logger.info(f"Island setting up")

   logger.info("Island adding middlewares")

   logger.debug("Island adding CORSMiddleware")
   application.add_middleware(
      CORSMiddleware,
      allow_origins=ALLOWED_HOSTS or ["*"],
      allow_credentials=True,
      allow_methods=["GET", "POST"],
      allow_headers=["*"],
   )

   logger.info("Island adding startup and shutdown events")

   application.add_event_handler("startup", create_start_app_handler(application))
   application.add_event_handler("shutdown", create_stop_app_handler(application))

   logger.info("Island adding exception handlers")

   application.add_exception_handler(HTTPException, http_error_handler)
   application.add_exception_handler(RequestValidationError, http422_error_handler)

   logger.info("Island adding routers")

   application.include_router(router, prefix=f"/{API_PREFIX.strip('/')}")

   logger.info("Island setup complete")

   return application


app = get_application()
