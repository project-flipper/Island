from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from island.core.config import config, SECRET_KEY
from island.database.schema.user import User
from island.core.constants.scope import Scope

class JWTTokenType(Enum):
    HS256 = "HS256"
    RS256 = "RS256"

DEFUALT_TOKEN_EXPIRE = config("DEFUALT_TOKEN_EXPIRE", cast=int, default=15*60)
JWT_ALGORITHM = config("DEFUALT_TOKEN_EXPIRE", cast=JWTTokenType, default="HS256")

PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="auth")

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password:str):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=DEFUALT_TOKEN_EXPIRE)

    to_encode.update({"exp": expire, 'iat': datetime.utcnow(), })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM.value)

    return encoded_jwt

def get_user_scopes(user: User, *, defualt_scopes: List[Scope] = None) -> List[Scope]:
    pass
