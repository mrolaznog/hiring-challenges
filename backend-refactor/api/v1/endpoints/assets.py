"""Assets endpoint (v1)."""

from typing import List

from fastapi import APIRouter
from schemas.asset_schema import AssetResponse
from services.asset_service import AssetService

router = APIRouter(tags=["assets"])

# Instance-based approach
asset_service = AssetService()


@router.get("/assets", response_model=List[AssetResponse])
async def get_assets():
    """Get all assets with their signals."""
    assets = asset_service.get_all_assets()
    return assets
