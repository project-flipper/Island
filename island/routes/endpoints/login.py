from fastapi import Depends, HTTPException, status, APIRouter, Response
from fastapi.security import OAuth2PasswordRequestForm

from island.core import config 
from island.core.constants.scope import Scope
from island.database.schema.User import User 
from island.database.utils.user import get_user
from island.models.token import TokenResponse, TokenError, Token
from island.utils.auth import verify_password, get_user_scopes

login = APIRouter()

@login.post("/auth")
async def handle_authenticate_user(response: Response, auth_input: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    user = await User.query.where(User.username == auth_input.username).gino.first()
    if user is None or not verify_password(auth_input.password, user.password):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return TokenResponse(
            error = TokenError(
                    error_type = "user.auth.failed",
                    error_code = 101,
                    error_description = "User authentication failed. Incorrect username or password."
            ),
            success = False
        )
    

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    user_scopes = get_user_scopes(user, [Scope.UserLogin])

    access_token = create_access_token(
        data = {
            "sub": user.username, 
            "scopes": list(scope.value for scope in user_scopes)
        }, 
        expires_delta=access_token_expires
    )

    return TokenResponse(
        data = Token(
            access_token = access_token,
            token_type = "bearer"
        ),
        success = True
    )