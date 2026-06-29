from fastapi import APIRouter

from app.core.config import settings
from app.core.responses import ApiResponse


router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=ApiResponse[dict])
def health_check() -> ApiResponse[dict]:
    return ApiResponse(
        message="Service is healthy.",
        data={
            "app_name": settings.app_name,
            "environment": settings.app_env,
        },
    )

