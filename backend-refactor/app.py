"""Application factory and configuration."""

import logging

from api.v1.endpoints import assets as assets_v1
from api.v1.endpoints import health as health_v1
from api.v1.endpoints import measurements as measurements_v1
from core.config import get_settings
from core.error_handlers import register_exception_handlers
from core.logging_config import configure_logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    configure_logging()
    logger = logging.getLogger(__name__)
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.api_version)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    # Register v1 routes
    app.include_router(assets_v1.router, prefix="/api/v1")
    app.include_router(measurements_v1.router, prefix="/api/v1")
    app.include_router(health_v1.router, prefix="/api/v1")

    @app.on_event("startup")
    async def _on_startup() -> None:
        logger.info("Application startup")

    @app.on_event("shutdown")
    async def _on_shutdown() -> None:
        logger.info("Application shutdown")

    return app
