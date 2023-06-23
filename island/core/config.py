import logging
from typing import List

from sqlalchemy.engine.url import URL, make_url
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

from island.core.logging import InterceptHandler

config = Config(".env")

# API config
API_PREFIX = config("API_PREFIX", cast=str, default="")
API_VERSION = config("API_VERSION", cast=str, default="0.0.1")
API_SUFFIX_VERSION = config("API_SUFFIX_VERSION", cast=bool, default=True)
if API_SUFFIX_VERSION:
    API_PREFIX = f"{API_PREFIX.strip('/')}/{API_VERSION.strip('/')}"
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=[]
)

# Logging config
DEBUG = config("DEBUG", cast=bool, default=False)
LOGGING_LEVEL = (
    logging.DEBUG
    if DEBUG
    else config("LOGGING_LEVEL", cast=lambda x: getattr(logging, x), default="INFO")
)

# Security config
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret, default="5df9db467ed2c905bcc1")
WORLD_ACCESS_KEY = config(
    "WORLD_ACCESS_KEY", cast=str, default="earlyDevelopmentTesting01"
)
DATABASE_SECRET_KEY = config(
    "DATABASE_SECRET_KEY", cast=Secret, default="change_me1234"
)

# Database config
DB_DRIVER = config("DB_DRIVER", default="postgresql+asyncpg")
DB_HOST = config("DB_HOST", default="localhost")
DB_PORT = config("DB_PORT", cast=int, default=None)
DB_USER = config("DB_USER", default="postgres")
DB_PASSWORD = config("DB_PASSWORD", cast=Secret, default="password")
DB_DATABASE = config("DB_DATABASE", default="island")
DB_DSN = config(
    "DB_DSN",
    cast=make_url,
    default=URL.create(
        drivername=DB_DRIVER,
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_DATABASE,
    ),
)


# Sentry config
SENTRY_DSN = config("SENTRY_DSN", cast=Secret, default="")

# Redis config
REDIS_HOST = config("REDIS_HOST", cast=str, default="127.0.0.1")
REDIS_PORT = config("REDIS_PORT", cast=int, default=6379)
REDIS_PASSWORD = config("REDIS_PASSWORD", cast=Secret, default=None)
REDIS_SSL_REQUIRED = config("REDIS_SSL_REQUIRED", cast=bool, default=True)

# General
I18N_DEFAULT_LOCALE = config("I18N_DEFAULT_LOCALE", cast=str, default="en")
I18N_DIR = config("I18N_DIR", cast=str, default="./config/locale")
FASTAPI_EVENTS_MIDDLEWARE_ID = config(
    "FASTAPI_EVENTS_MIDDLEWARE_ID", cast=int, default=id("fastapi-events")
)

logging.getLogger().handlers = [InterceptHandler()]
LOGGERS = ("uvicorn.asgi", "uvicorn.access")
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.setLevel(logging.INFO)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]
