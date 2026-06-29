from fastapi import APIRouter

from app.routers import alarm_intelligence, auth, health, metadata, templates, users
from app.routers.dashboards import router as dashboards_router


api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(metadata.router)
api_router.include_router(templates.router)
api_router.include_router(templates.category_router)
api_router.include_router(dashboards_router)
api_router.include_router(alarm_intelligence.router)
