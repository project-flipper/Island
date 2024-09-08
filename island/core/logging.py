import logging
from types import FrameType
from typing import cast

from fastapi.exceptions import RequestValidationError
from loguru import logger
from pydantic import ValidationError


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = cast(FrameType, frame.f_back)
            depth += 1

        exc_info = record.exc_info

        debug = False
        if (
            not debug
            and exc_info is not None
            and exc_info[0] is not None
            and issubclass(
                exc_info[0], (ValidationError, RequestValidationError)
            )
        ):
            logger.error("Validation error occured")
            return

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )
