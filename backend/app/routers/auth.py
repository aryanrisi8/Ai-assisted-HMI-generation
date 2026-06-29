from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.auth.schemas import AuthResponse, LoginRequest, RegisterRequest, TokenResponse
from app.core.responses import ApiResponse
from app.db.session import get_db
from app.models import User
from app.schemas import UserRead
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=ApiResponse[AuthResponse])
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
) -> ApiResponse[AuthResponse]:
    auth_response = AuthService(db).register(payload)
    return ApiResponse(message="User registered.", data=auth_response)


@router.post("/login", response_model=ApiResponse[AuthResponse])
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
) -> ApiResponse[AuthResponse]:
    auth_response = AuthService(db).authenticate(payload.username, payload.password)
    return ApiResponse(message="Login successful.", data=auth_response)


@router.post("/token", response_model=TokenResponse)
def oauth_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:
    auth_response = AuthService(db).authenticate(
        form_data.username,
        form_data.password,
    )
    return TokenResponse(access_token=auth_response.access_token)


@router.get("/me", response_model=ApiResponse[UserRead])
def read_current_user(
    current_user: User = Depends(get_current_active_user),
) -> ApiResponse[UserRead]:
    return ApiResponse(data=UserRead.model_validate(current_user))

