import asyncio
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.param_functions import Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload
from fastapi.responses import JSONResponse

from island.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from island.core.constants.scope import Scope
from island.database import ASYNC_SESSION
from island.database.schema.ban import BanTable
from island.database.schema.user import UserTable
from island.models import Error
from island.models.errors.ban import BanError
from island.models.token import Token, TokenResponse
from island.utils.auth import (
    create_access_token,
    get_current_user,
    get_oauth_data,
    get_user_scopes,
    require_oauth_scopes,
    verify_password,
)

router = APIRouter()

DEFAULT_USER_SCOPES = [Scope.UserLogin, Scope.UserRead, Scope.WorldAccess]

@router.post("/login")
async def handle_authenticate_user(
    response: Response,
    auth_input: Annotated[OAuth2PasswordRequestForm, Depends()],
    save_session: bool = Form(
        False,
        description="Returns an access key which can be further used to reauthenticate without need for username and password, if set to True",
    ),
) -> TokenResponse:
    """Authenticate user data and generate OAuth token.

    Args:
        response (Response)
        auth_input (OAuth2PasswordRequestForm, optional): Defaults to Depends().

    Returns:
        TokenResponse
    """
    loop = asyncio.get_event_loop()

    async with ASYNC_SESSION() as session:
        now = datetime.now()
        user_query = (
            select(UserTable)
            .options(joinedload(UserTable.bans.and_(BanTable.ban_expire > now)))
            .where(func.lower(UserTable.username) == auth_input.username.lower())
        )

        user = (await session.execute(user_query)).scalar()

    if user is None or not await loop.run_in_executor(None, verify_password, auth_input.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Error(
                error_type="user.auth.credentials",
                error_code=100,
                error_description="User authentication failed. Incorrect username or password.",
            )
        )

    user_ban = user.bans[0] if user.bans else None
    if user_ban is not None:
        ban_dur = user_ban.ban_expire - datetime.now()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=BanError(
                error_code=user_ban.ban_type,
                error_description=str(ban_dur),
                ban_dur=round(ban_dur.total_seconds() / 60),
            )
        )

    access_token_expires = timedelta(seconds=ACCESS_TOKEN_EXPIRE_MINUTES)
    user_scopes = await get_user_scopes(user, default_scopes=DEFAULT_USER_SCOPES)

    access_token = create_access_token(
        data={
            "sub": f"{user.username}#{user.id}",
            "scopes": list(map(str, user_scopes)),
        },
        expires_delta=access_token_expires,
    )
    
    token = Token(access_token=access_token, token_type="bearer")
    if save_session:
        token.session_key = create_access_token(
            data={
                "sub": f"{user.username}#{user.id}",
                "scopes": [str(Scope.UserAuth)],
            },
            expires_delta=timedelta(days=180),
        )

    return TokenResponse(data=token, access_token=token.access_token, session_key=token.session_key, token_type=token.token_type, success=True)


@router.post(
    "/refresh",
    dependencies=[require_oauth_scopes(Scope.UserAuth)],
)
async def handle_reauthenticate_user(
    response: Response, user: Annotated[UserTable, Depends(get_current_user)]
) -> TokenResponse:
    user_ban = user.bans[0] if user.bans else None
    if user_ban is not None:
        ban_dur = user_ban.ban_expire - datetime.now()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=BanError(
                error_code=user_ban.ban_type,
                error_description=str(ban_dur),
                ban_dur=round(ban_dur.total_seconds() / 60),
            )
        )

    access_token_expires = timedelta(seconds=ACCESS_TOKEN_EXPIRE_MINUTES)
    user_scopes = await get_user_scopes(user, default_scopes=DEFAULT_USER_SCOPES)

    access_token = create_access_token(
        data={
            "sub": f"{user.username}#{user.id}",
            "scopes": list(map(str, user_scopes)),
        },
        expires_delta=access_token_expires,
    )

    token = Token(access_token=access_token, token_type="bearer")
    return TokenResponse(data=token, access_token=token.access_token, session_key=token.session_key, token_type=token.token_type, success=True)

