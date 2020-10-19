import loguru
from fastapi import APIRouter

from api.core import config # pylint: disable=import-error
from api.database.schema.User import User # pylint: disable=import-error

