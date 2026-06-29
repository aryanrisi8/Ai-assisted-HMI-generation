from uuid import UUID

from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models import User, UserStatus
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.users = UserRepository(db)

    def get_by_id(self, user_id: UUID) -> User:
        user = self.users.get(user_id)
        if user is None:
            raise AppException(
                message="User not found.",
                status_code=status.HTTP_404_NOT_FOUND,
                error_code="user_not_found",
            )
        return user

    def ensure_active(self, user: User) -> User:
        if user.status != UserStatus.ACTIVE:
            raise AppException(
                message="User account is not active.",
                status_code=status.HTTP_403_FORBIDDEN,
                error_code="inactive_user",
            )
        return user

