from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.core.monitoring import register_monitoring
from app.routers.api import api_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    configure_logging()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="0.1.0",
        lifespan=lifespan,
    )

    if settings.backend_cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.backend_cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    register_exception_handlers(app)
    register_monitoring(app)
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
