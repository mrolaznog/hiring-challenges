"""Utility helpers for assets."""

from typing import Dict


def format_asset_response(asset_data: Dict) -> Dict:
    """Format asset data for response."""
    return {
        "asset_id": asset_data.get("asset_id"),
        "signals": asset_data.get("signals", []),
    }
