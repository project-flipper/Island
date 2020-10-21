import loguru
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from island.core import config 
from island.database.schema.User import User 
from island.database.utils.user import get_user

login = APIRouter()

@login.post("/auth")
async def handle_authenticate_user():
    pass