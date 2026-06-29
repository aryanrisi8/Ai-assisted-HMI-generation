from datetime import datetime, timezone

from fastapi import status
from sqlalchemy.orm import Session

from app.auth.schemas import AuthResponse, RegisterRequest
from app.auth.security import create_access_token, get_password_hash, verify_password
from app.core.exceptions import AppException
from app.models import Role, User, UserStatus
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas import UserRead


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.users = UserRepository(db)
        self.roles = RoleRepository(db)

    def authenticate(self, login: str, password: str) -> AuthResponse:
        user = self.users.get_by_login(login)
        if not user or not verify_password(password, user.hashed_password):
            raise AppException(
                message="Invalid username or password.",
                status_code=status.HTTP_401_UNAUTHORIZED,
                error_code="invalid_credentials",
            )

        if user.status != UserStatus.ACTIVE:
            raise AppException(
                message="User account is not active.",
                status_code=status.HTTP_403_FORBIDDEN,
                error_code="inactive_user",
            )

        user.last_login_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(user)

        token = create_access_token(
            subject=str(user.id),
            extra_claims={"role": user.role.name if user.role else None},
        )
        return AuthResponse(access_token=token, user=UserRead.model_validate(user))

    def register(self, payload: RegisterRequest) -> AuthResponse:
        if self.users.get_by_email(payload.email):
            raise AppException(
                message="Email already exists.",
                status_code=status.HTTP_409_CONFLICT,
                error_code="email_exists",
            )
        if self.users.get_by_username(payload.username):
            raise AppException(
                message="Username already exists.",
                status_code=status.HTTP_409_CONFLICT,
                error_code="username_exists",
            )

        role = self.roles.get_by_name(payload.role_name)
        if role is None:
            role = Role(
                name=payload.role_name,
                description=f"Default {payload.role_name} role",
                permissions={},
            )
            self.roles.add(role)

        user = User(
            role_id=role.id,
            email=str(payload.email),
            username=payload.username,
            full_name=payload.full_name,
            hashed_password=get_password_hash(payload.password),
            status=UserStatus.ACTIVE,
        )
        self.users.add(user)
        self.db.commit()
        self.db.refresh(user)

        token = create_access_token(
            subject=str(user.id),
            extra_claims={"role": role.name},
        )
        return AuthResponse(access_token=token, user=UserRead.model_validate(user))

