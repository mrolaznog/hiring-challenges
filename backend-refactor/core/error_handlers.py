"""Centralized exception handlers."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from core.exceptions import NotFoundError, ValidationError

try:
    # Pydantic uses an internal "undefined" sentinel for missing fields; this may move across versions.
    from pydantic_core import PydanticUndefined
except Exception:  # pragma: no cover - fallback for safety
    PydanticUndefined = object()


def _sanitize_errors(value):
    if value is PydanticUndefined or type(value).__name__ == "PydanticUndefinedType":
        return None
    if isinstance(value, dict):
        return {k: _sanitize_errors(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_sanitize_errors(v) for v in value]
    if isinstance(value, tuple):
        return [_sanitize_errors(v) for v in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers for the API."""

    @app.exception_handler(ValueError)
    async def value_error_handler(_: Request, exc: ValueError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(
        _: Request, exc: ValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(NotFoundError)
    async def not_found_handler(_: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": _sanitize_errors(exc.errors())},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, __: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )
