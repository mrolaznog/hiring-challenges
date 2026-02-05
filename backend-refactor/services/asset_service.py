"""Asset service."""

import logging
from typing import List

from core.exceptions import NotFoundError
from db.asset_db import get_assets
from schemas.asset_schema import AssetResponse
from utils.asset_helper import format_asset_response

logger = logging.getLogger(__name__)


class AssetService:
    """Service for managing assets."""

    def get_all_assets(self) -> List[AssetResponse]:
        """Get all assets with their signals."""
        logger.info("Fetching all assets")
        assets = get_assets()
        if not assets:
            logger.warning("No assets found")
            raise NotFoundError("No assets found")
        response = [AssetResponse(**format_asset_response(asset)) for asset in assets]
        logger.info("Fetched %d assets", len(response))
        return response
