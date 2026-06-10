from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import UserStatus
from app.repositories.users import UserRepository
from app.schemas.auth import AuthResponse, SignInRequest, SignUpRequest, UserRead


class AuthService:
    def __init__(self, db: Session, settings: Settings) -> None:
        self.users = UserRepository(db)
        self.settings = settings

    def signup(self, payload: SignUpRequest) -> tuple[AuthResponse, str]:
        existing_user = self.users.get_by_email(payload.email)
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

        user = self.users.create(
            name=payload.name.strip(),
            email=payload.email,
            password_hash=hash_password(payload.password),
            daily_request_limit=self.settings.default_daily_request_limit,
            monthly_request_limit=self.settings.default_monthly_request_limit,
            max_tokens_per_request=self.settings.default_max_tokens_per_request,
        )
        token = create_access_token(user.id, self.settings)
        return AuthResponse(user=UserRead.model_validate(user)), token

    def signin(self, payload: SignInRequest) -> tuple[AuthResponse, str]:
        user = self.users.get_by_email(payload.email)
        if user is None or not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email or password is incorrect.",
            )

        if user.status != UserStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This account is disabled.",
            )

        token = create_access_token(user.id, self.settings)
        return AuthResponse(user=UserRead.model_validate(user)), token

