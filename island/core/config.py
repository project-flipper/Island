import logging
import sys
from typing import List

from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret, URL

from island.core.logging import InterceptHandler # pylint: disable=import-error

config = Config(".env")

API_PREFIX = config("API_PREFIX", cast=str, default="/api")
API_VERSION = config("API_VERSION", cast=str, default="0.0.1")
API_SUFFIX_VERSION = config("API_SUFFIX_VERSION", cast=bool, default=True)
if API_SUFFIX_VERSION:
    API_PREFIX = f"{API_PREFIX.strip('/')}/{API_VERSION.strip('/')}"
DEBUG = config("DEBUG", cast=bool, default=False)
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret, default="5df9db467ed2c905bcc1")
ALLOWED_HOSTS: List[str] = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=[])
LOGGING_LEVEL = logging.DEBUG if DEBUG else config("LOGGING_LEVEL", cast=lambda x: getattr(logging, x), default="INFO")
WORLD_ACCESS_KEY = config("WORLD_ACCESS_KEY", cast=str, default="earlyDevelopmentTesting01")

logging.getLogger().handlers = [InterceptHandler()]
LOGGERS = ("uvicorn.asgi", "uvicorn.access")
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.setLevel(logging.INFO)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]
