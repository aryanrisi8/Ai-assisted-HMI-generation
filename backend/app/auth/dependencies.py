from uuid import UUID

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.security import decode_access_token, is_token_error
from app.core.config import settings
from app.core.exceptions import AppException
from app.db.session import get_db
from app.models import User
from app.services.user_service import UserService


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_v1_prefix}/auth/token"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")
        if subject is None:
            raise ValueError("Missing token subject.")
        user_id = UUID(subject)
    except Exception as exc:
        if is_token_error(exc) or isinstance(exc, (ValueError, TypeError)):
            raise AppException(
                message="Invalid or expired authentication token.",
                status_code=status.HTTP_401_UNAUTHORIZED,
                error_code="invalid_token",
            ) from exc
        raise

    return UserService(db).get_by_id(user_id)


def get_current_active_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    return UserService(db).ensure_active(current_user)


def require_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if not current_user.is_superuser:
        raise AppException(
            message="Superuser privileges are required.",
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="forbidden",
        )
    return current_user
