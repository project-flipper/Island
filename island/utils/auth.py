from datetime import datetime, timedelta, UTC
from typing import Annotated, Any

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
import jwt
import bcrypt
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from island.core.config import DATABASE_SECRET_KEY, DEFAULT_TOKEN_EXPIRE, JWT_ALGORITHM, SECRET_KEY
from island.core.constants.scope import Scope as ScopeEnum
from island.database import ASYNC_SESSION
from island.database.schema.ban import BanTable
from island.database.schema.user import UserTable
from island.models import Error

from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine


class IslandOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> str | None:
        try:
            return await super().__call__(request)
        except HTTPException:
            raise oauth_error


OAUTH2_SCHEME = IslandOAuth2PasswordBearer(tokenUrl="/auth/login")

oauth_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=Error(
        error_type="user.token.invalid",
        error_code=101,
        error_description="OAuth token invalid or expired.",
    ),
)

scope_error = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail=Error(
        error_type="user.token.scope",
        error_code=103,
        error_description="OAuth does not meet the required scopes.",
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
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def get_password_hash(password: str) -> str:
    """Generate bcrypt hash for given plain text password.

    Args:
        password (str)

    Returns:
        str
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def encrypt_email(email: str) -> str:
    """Encrypts an email using AES.
    
    """
    engine = AesEngine()
    engine._update_key(str(DATABASE_SECRET_KEY))
    engine._set_padding_mechanism("pkcs5")
    return engine.encrypt(email)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Generate OAuth2 token with given data, and expiry

    Args:
        data (dict)
        expires_delta (Optional[Union[timedelta, None]], optional): Defaults to None.

    Returns:
        str: OAuth2 encoded token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(seconds=DEFAULT_TOKEN_EXPIRE)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=JWT_ALGORITHM.value)

    return encoded_jwt


async def get_user_scopes(
    user: UserTable, *, default_scopes: list[ScopeEnum] | None = None
) -> list[ScopeEnum]:
    """Get list of user scopes from database, along with default_scopes if any given. `default_scopes` is added to beginning of the result.

    Args:
        user (User)
        default_scopes (Optional[Union[timedelta, None]], optional): Defaults to None.

    Returns:
        List[Scope]
    """

    return user.scopes if not default_scopes else default_scopes + user.scopes

async def get_oauth_data(oauth: Annotated[str, Depends(OAUTH2_SCHEME)]) -> dict[str, Any]:
    try:
        data = jwt.decode(oauth, str(SECRET_KEY), algorithms=[JWT_ALGORITHM.value])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        raise oauth_error

    return data

async def get_current_user_id(oauth_data: Annotated[dict[str, Any], Depends(get_oauth_data)]) -> int:
    _, user_id = oauth_data["sub"].split("#")
    return int(user_id)

async def get_current_user(user_id: Annotated[int, Depends(get_current_user_id)]) -> UserTable:
    async with ASYNC_SESSION() as session:
        user_query = (
            select(UserTable)
            .options(
                joinedload(UserTable.bans.and_(BanTable.ban_expire > datetime.now()))
            )
            .where(UserTable.id == user_id)
        )

        user = (await session.execute(user_query)).scalar()

    if user is None or user.id != user_id:
        raise oauth_error

    return user

def require_oauth_scopes(*scopes: ScopeEnum):
    """Checks if user has required scope/permission.

    Raises:
        scope_error: If user doesn't have sufficient scope/perms.

    Returns:
        Depends: FastAPI dependency
    """
    scopes_req = set(map(str, scopes))

    def __check_oauth_scope(oauth_data: Annotated[dict[str, Any], Depends(get_oauth_data)]):
        available_scopes = set(oauth_data["scopes"])

        if not scopes_req.issubset(available_scopes):
            raise scope_error

    return Depends(__check_oauth_scope)
