"""Measurement schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class MeasurementResponse(BaseModel):
    """Response schema for measurements."""

    signal_id: str
    timestamp: datetime
    value: float
    unit: Optional[str] = None

    @field_validator("signal_id")
    @classmethod
    def _non_empty_signal_id(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("signal_id must be non-empty")
        return value

    model_config = {
        "json_schema_extra": {
            "example": {
                "signal_id": "427038",
                "timestamp": "2021-11-07T23:59:03.762",
                "value": 116.129,
                "unit": None,
            }
        }
    }


class MeasurementStatsResponse(BaseModel):
    """Statistics response for a signal over a date range."""

    signal_id: str
    from_date: datetime
    to_date: datetime
    count: int
    mean: Optional[float]
    min: Optional[float]
    max: Optional[float]
    median: Optional[float]
    std_dev: Optional[float]

    @field_validator("signal_id")
    @classmethod
    def _non_empty_stats_signal_id(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("signal_id must be non-empty")
        return value

    model_config = {
        "json_schema_extra": {
            "example": {
                "signal_id": "427038",
                "from_date": "2021-11-07T00:00:00",
                "to_date": "2021-11-07T23:59:59",
                "count": 5,
                "mean": 116.12,
                "min": 115.36,
                "max": 116.13,
                "median": 115.96,
                "std_dev": 0.31,
            }
        }
    }
