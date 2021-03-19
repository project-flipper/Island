from datetime import datetime, timedelta

from fastapi import Depends, status, APIRouter, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.param_functions import Form
from starlette.responses import JSONResponse

from island.core.config import config
from island.core.constants.scope import Scope
from island.database.schema.user import User
from island.models.token import TokenResponse, TokenError, Token
from island.models.error import BanError
from island.utils.auth import (
    verify_password,
    get_user_scopes,
    create_access_token,
    require_oauth_scopes,
    get_oauth_data,
    oauth_error,
    get_current_user,
    get_user_ban,
)

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=15 * 60
)  # seconds


@router.post("/auth", response_model=TokenResponse)
async def handle_authenticate_user(
    response: Response,
    auth_input: OAuth2PasswordRequestForm = Depends(),
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
    user = await User.query.where(User.username == auth_input.username).gino.first()
    if user is None or not verify_password(auth_input.password, user.password):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return TokenResponse(
            error=TokenError(
                error_type="user.auth.failed",
                error_code=101,
                error_description="User authentication failed. Incorrect username or password.",
            ),
            success=False,
            has_error=True,
        )

    user_ban = await get_user_ban(user)
    if user_ban is not None:
        response.status_code = status.HTTP_403_FORBIDDEN
        ban_dur = user_ban.ban_expire - datetime.now()
        return TokenResponse(
            error=BanError(
                error_code=user_ban.ban_type.value,
                error_description=str(ban_dur),
                ban_dur=round(ban_dur.total_seconds()/60)
            ),
            success=False,
            has_error=True
        )

    access_token_expires = timedelta(seconds=ACCESS_TOKEN_EXPIRE_MINUTES)
    user_scopes = await get_user_scopes(user, default_scopes=[Scope.UserLogin])

    access_token = create_access_token(
        data={
            "sub": f"{user.username}#{user.id}",
            "scopes": list(map(str, user_scopes)),
        },
        expires_delta=access_token_expires,
    )

    token_response = TokenResponse(
        data=Token(access_token=access_token, token_type="bearer"), success=True
    )

    if save_session:
        session_token = create_access_token(
            data={
                "sub": f"{user.username}#{auth_input.password}",
                "scopes": [Scope.UserAuth],
            },
            expires_delta=timedelta(days=180),
        )
        token_response.session_key = session_token

    return token_response


@router.post(
    "/resume",
    response_model=TokenResponse,
    dependencies=[require_oauth_scopes(Scope.UserAuth)],
)
async def handle_authenticate_user(
    response: Response, user: User = Depends(get_current_user)
) -> TokenResponse:

    user_ban = await get_user_ban(user)
    if user_ban is not None:
        response.status_code = status.HTTP_403_FORBIDDEN
        ban_dur = user_ban.ban_expire - datetime.now()
        return TokenResponse(
            error=BanError(
                error_code=user_ban.ban_type.value,
                error_description=str(ban_dur),
                ban_dur=round(ban_dur.total_seconds()/60)
            ),
            success=False,
            has_error=True
        )

    access_token_expires = timedelta(seconds=ACCESS_TOKEN_EXPIRE_MINUTES)
    user_scopes = await get_user_scopes(user, default_scopes=[Scope.UserLogin])

    access_token = create_access_token(
        data={
            "sub": f"{user.username}#{user.id}",
            "scopes": list(map(str, user_scopes)),
        },
        expires_delta=access_token_expires,
    )

    return TokenResponse(
        data=Token(access_token=access_token, token_type="bearer"), success=True
    )


@router.get("/test", dependencies=[require_oauth_scopes(Scope.UserLogin)])
async def test_oauth(request: Request):
    scope = request.scope
    return JSONResponse({"scopes": scope["oauth"]["scopes"]})
