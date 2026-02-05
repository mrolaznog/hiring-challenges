"""Database operations for measurements."""

import csv
from datetime import datetime
from functools import lru_cache
from typing import Dict, List

from core.config import get_settings


def _parse_value(raw_value: str) -> float:
    """Parse measurement values that may use comma decimal separators."""
    return float(raw_value.replace(",", "."))


@lru_cache()
def _load_measurements() -> List[Dict]:
    """Load all measurements from CSV and cache in memory."""
    settings = get_settings()
    measurements: List[Dict] = []

    try:
        with open(settings.measurements_path, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter="|")
            for row in reader:
                signal_id = row.get("SignalId")
                timestamp_str = row.get("Ts")
                raw_value = row.get("MeasurementValue")

                if not signal_id or not timestamp_str or raw_value is None:
                    continue

                try:
                    timestamp = datetime.fromisoformat(timestamp_str)
                    value = _parse_value(raw_value)
                except ValueError:
                    continue

                measurements.append(
                    {
                        "signal_id": signal_id,
                        "timestamp": timestamp,
                        "value": value,
                        "unit": None,
                    }
                )
    except FileNotFoundError as exc:
        raise RuntimeError(
            f"Measurements file not found: {settings.measurements_path}"
        ) from exc

    return measurements


def get_measurements(
    signal_ids: List[str], from_date: datetime, to_date: datetime
) -> List[Dict]:
    """Get measurements for given signal IDs and date range."""
    signal_set = set(signal_ids)
    measurements = _load_measurements()

    return [
        m
        for m in measurements
        if m["signal_id"] in signal_set and from_date <= m["timestamp"] <= to_date
    ]
