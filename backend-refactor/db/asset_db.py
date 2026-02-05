"""Database operations for assets."""

from typing import Dict, List

from db.signal_db import load_signals


def get_assets() -> List[Dict]:
    """Get all assets grouped by asset_id."""
    signals = load_signals()
    assets_dict = {}

    for signal in signals:
        asset_id = signal.get("asset_id")
        if asset_id not in assets_dict:
            assets_dict[asset_id] = {"asset_id": asset_id, "signals": []}
        assets_dict[asset_id]["signals"].append(signal)

    return list(assets_dict.values())
