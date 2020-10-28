from datetime import  timedelta

from fastapi import Depends, HTTPException, status, APIRouter, Response
from fastapi.security import OAuth2PasswordRequestForm

from island.core.config import config
from island.core.constants.scope import Scope
from island.database.schema.user import User
from island.models.token import TokenResponse, TokenError, Token
from island.utils.auth import verify_password, get_user_scopes, create_access_token

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=15*60) # seconds

@router.post("/auth", response_model=TokenResponse)
async def handle_authenticate_user(response: Response, auth_input: OAuth2PasswordRequestForm=Depends()) -> TokenResponse:
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
            error = TokenError(
                error_type="user.auth.failed",
                error_code=101,
                error_description="User authentication failed. Incorrect username or password."
            ),
            success = False,
            hasError = True
        )

    access_token_expires = timedelta(seconds=ACCESS_TOKEN_EXPIRE_MINUTES)
    user_scopes = await get_user_scopes(user, default_scopes = [Scope.UserLogin])

    access_token = create_access_token(
        data = {
            "sub": user.username,
            "scopes": list(scope.value for scope in user_scopes)
        },
        expires_delta=access_token_expires
    )

    return TokenResponse(
        data=Token(
            access_token=access_token,
            token_type="bearer"
        ),
        success=True
    )
