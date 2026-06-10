from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.config import Settings, get_settings
from app.core.database import get_db
from app.schemas.auth import AuthResponse, SignInRequest, SignUpRequest, UserRead
from app.services.auth import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def signup(
    payload: SignUpRequest,
    response: Response,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> AuthResponse:
    auth_response, token = AuthService(db, settings).signup(payload)
    _set_session_cookie(response, token, settings)
    return auth_response


@router.post("/signin", response_model=AuthResponse)
def signin(
    payload: SignInRequest,
    response: Response,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> AuthResponse:
    auth_response, token = AuthService(db, settings).signin(payload)
    _set_session_cookie(response, token, settings)
    return auth_response


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(settings: Settings = Depends(get_settings)) -> Response:
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie(
        key=settings.session_cookie_name,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        path="/",
    )
    return response


@router.get("/me", response_model=UserRead)
def me(current_user=Depends(get_current_user)) -> UserRead:
    return UserRead.model_validate(current_user)


def _set_session_cookie(response: Response, token: str, settings: Settings) -> None:
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        max_age=settings.access_token_expire_minutes * 60,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        path="/",
    )
