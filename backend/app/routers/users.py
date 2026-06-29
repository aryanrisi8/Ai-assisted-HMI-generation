from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_active_user
from app.core.responses import ApiResponse
from app.models import User
from app.schemas import UserRead


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=ApiResponse[UserRead])
def read_me(current_user: User = Depends(get_current_active_user)) -> ApiResponse[UserRead]:
    return ApiResponse(data=UserRead.model_validate(current_user))

