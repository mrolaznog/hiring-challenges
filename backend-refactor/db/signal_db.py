"""Database operations for signals."""

import json
from functools import lru_cache
from typing import Dict, List

from core.config import get_settings


def _normalize_signal(raw: Dict) -> Dict:
    """Normalize signal keys to snake_case."""
    return {
        "signal_gid": raw.get("SignalGId"),
        "signal_id": raw.get("SignalId"),
        "signal_name": raw.get("SignalName"),
        "asset_id": raw.get("AssetId"),
        "unit": raw.get("Unit"),
    }


@lru_cache()
def load_signals() -> List[Dict]:
    """Load signals from JSON file."""
    settings = get_settings()
    try:
        with open(settings.signals_path, "r") as f:
            data = json.load(f)
            return [_normalize_signal(item) for item in data]
    except FileNotFoundError as exc:
        raise RuntimeError(f"Signals file not found: {settings.signals_path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Invalid JSON in signals file: {settings.signals_path}"
        ) from exc
