from datetime import datetime, timedelta
from typing import Optional, List, Union
from enum import Enum

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Response, HTTPException, Depends
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
    return PASSWORD_CONTEXT.verify(plain_password, hashed_password)

def get_password_hash(password:str):
    return PASSWORD_CONTEXT.hash(password)

def create_access_token(data: dict, expires_delta: Optional[Union[timedelta, None]] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=DEFUALT_TOKEN_EXPIRE)

    to_encode.update({"exp": expire, 'iat': datetime.utcnow(), })
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=JWT_ALGORITHM.value)

    return encoded_jwt

async def get_user_scopes(user: User, *, defualt_scopes: Optional[Union[timedelta, None]] = None) -> List[Scope]:
    user_scopes = await user.scopes

    scopes = [
        Scope(await s.tag)
        for s in user_scopes
    ]

    return scopes if not defualt_scopes else (defualt_scopes + scopes)

async def get_current_user(response: Response, token: str = Depends(OAUTH2_SCHEME)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user