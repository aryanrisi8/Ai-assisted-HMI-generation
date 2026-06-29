from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.monitoring import render_prometheus_metrics
from app.core.responses import ApiResponse
from app.db.session import SessionLocal


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


@router.get("/ready", response_model=ApiResponse[dict])
def readiness_check() -> ApiResponse[dict]:
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        return ApiResponse(
            success=False,
            message="Database readiness check failed.",
            data={"ready": False, "error": exc.__class__.__name__},
        )
    return ApiResponse(message="Service is ready.", data={"ready": True})


@router.get("/metrics", response_class=PlainTextResponse)
def metrics() -> str:
    return render_prometheus_metrics()
