"""Health check endpoint (v1)."""

from datetime import datetime, timezone

from fastapi import APIRouter
from schemas.health_schema import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def get_health() -> HealthResponse:
    """Return service health status."""
    return HealthResponse(status="ok", timestamp=datetime.now(timezone.utc))
