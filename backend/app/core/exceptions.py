import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.responses import ErrorResponse


logger = logging.getLogger(__name__)


class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: str = "application_error",
        details: dict | list | str | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details


def _error_response(
    status_code: int,
    message: str,
    error_code: str,
    details: dict | list | str | None = None,
) -> JSONResponse:
    payload = ErrorResponse(
        message=message,
        error_code=error_code,
        details=details,
    )
    return JSONResponse(status_code=status_code, content=payload.model_dump())


async def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
    return _error_response(
        status_code=exc.status_code,
        message=exc.message,
        error_code=exc.error_code,
        details=exc.details,
    )


async def validation_exception_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    return _error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Request validation failed.",
        error_code="validation_error",
        details=exc.errors(),
    )


async def integrity_error_handler(_: Request, exc: IntegrityError) -> JSONResponse:
    logger.warning("Database integrity error", exc_info=exc)
    return _error_response(
        status_code=status.HTTP_409_CONFLICT,
        message="Database constraint violation.",
        error_code="integrity_error",
    )


async def sqlalchemy_error_handler(_: Request, exc: SQLAlchemyError) -> JSONResponse:
    logger.exception("Database error", exc_info=exc)
    return _error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Database operation failed.",
        error_code="database_error",
    )


async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error", exc_info=exc)
    return _error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Internal server error.",
        error_code="internal_server_error",
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

