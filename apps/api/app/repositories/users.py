from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User, UserRole, UserStatus


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: str) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        normalized_email = email.lower()
        statement = select(User).where(User.email == normalized_email)
        return self.db.scalar(statement)

    def create(
        self,
        *,
        name: str,
        email: str,
        password_hash: str,
        daily_request_limit: int,
        monthly_request_limit: int,
        max_tokens_per_request: int,
        role: UserRole = UserRole.USER,
        status: UserStatus = UserStatus.ACTIVE,
    ) -> User:
        user = User(
            name=name,
            email=email.lower(),
            password_hash=password_hash,
            role=role,
            status=status,
            daily_request_limit=daily_request_limit,
            monthly_request_limit=monthly_request_limit,
            max_tokens_per_request=max_tokens_per_request,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

