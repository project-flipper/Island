from datetime import datetime, timedelta
from typing import Optional, List, Union
from enum import Enum

from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status, Request
from jose import jwt
from passlib.context import CryptContext

from island.core.config import config, SECRET_KEY
from island.database.schema.user import User
from island.database.schema.ban import Ban
from island.core.constants.scope import Scope as ScopeEnum
from island.models.error import Error


class JWTTokenType(Enum):
    HS256 = "HS256"
    RS256 = "RS256"


class IslandOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        try:
            return await super().__call__(request)
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=Error(
                    error_type="oauth.failed",
                    error_code=103,
                    error_description="Unable to verify OAuth. OAuth invalid or expired.",
                ),
            )


DEFAULT_TOKEN_EXPIRE = config(
    "DEFAULT_TOKEN_EXPIRE", cast=int, default=15 * 60)
JWT_ALGORITHM = config("DEFAULT_TOKEN_EXPIRE",
                       cast=JWTTokenType, default="HS256")

PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAUTH2_SCHEME = IslandOAuth2PasswordBearer(tokenUrl="auth")

oauth_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=Error(
        error_type="user.token.failed",
        error_code=102,
        error_description="OAuth token doesn't have required scope or expired.",
    ),
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain_text against hashed bcrypt hash_password

    Args:
        plain_password (str)
        hashed_password (str)

    Returns:
        bool
    """
    return PASSWORD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate bcrypt hash for given plain text password.

    Args:
        password (str)

    Returns:
        str
    """
    return PASSWORD_CONTEXT.hash(password)


def create_access_token(
    data: dict, expires_delta: Optional[Union[timedelta, None]] = None
) -> str:
    """Generate OAuth2 token with given data, and expiry

    Args:
        data (dict)
        expires_delta (Optional[Union[timedelta, None]], optional): Defaults to None.

    Returns:
        str: OAuth2 encoded token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=DEFAULT_TOKEN_EXPIRE)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, str(
        SECRET_KEY), algorithm=JWT_ALGORITHM.value)

    return encoded_jwt


async def get_user_scopes(
    user: User, *, default_scopes: Optional[List[ScopeEnum]] = None
) -> List[ScopeEnum]:
    """Get list of user scopes from database, along with default_scopes if any given. `default_scopes` is added to beginning of the result.

    Args:
        user (User)
        default_scopes (Optional[Union[timedelta, None]], optional): Defaults to None.

    Returns:
        List[Scope]
    """

    return user.scopes if not default_scopes else default_scopes + user.scopes


async def get_oauth_data(request: Request) -> dict:
    oauth_data = request.scope["oauth"]

    if oauth_data is None:
        raise oauth_error

    return oauth_data


async def get_current_user(oauth_data: dict = Depends(get_oauth_data)) -> User:
    username, user_id = oauth_data["data"]["sub"].split("#")
    user = await User.query.where(User.username == username).gino.first()

    if user is None or str(user.id) != user_id:
        raise oauth_error

    return user


async def get_user_ban(user: User = Depends(get_current_user)) -> Union[Ban, None]:
    """Get user active `Ban` object, `None` otherwise

    Args:
        user (User, optional): [`User` object]. Defaults to Depends(get_current_user).

    Returns:
        Union[Ban, None]: User' active ban
    """
    user_ban: Ban = await Ban.load(user=user).order_by(Ban.ban_expire).limit(1).first()
    if user_ban is None:
        return

    now = datetime.now()
    if user_ban.ban_expire > now:
        return user_ban


def require_oauth_scopes(*scopes: List[ScopeEnum]):
    """Checks if user has required scope/permission.

    Raises:
        oauth_error: If user doesn't have sufficient scope/perms.

    Returns:
        Depends: FastAPI dependency
    """
    scopes_req = set(map(str, scopes))

    def __check_oauth_scope(oauth_data: dict = Depends(get_oauth_data)):
        available_scopes = set(oauth_data["scopes"])

        if not scopes_req.issubset(available_scopes):
            raise oauth_error

    return Depends(__check_oauth_scope)
