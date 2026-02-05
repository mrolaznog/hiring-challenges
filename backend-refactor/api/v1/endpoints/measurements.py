"""Measurements endpoints (v1)."""

from typing import List

from fastapi import APIRouter, Path, Query
from schemas.measurement_schema import MeasurementResponse, MeasurementStatsResponse
from services.measurement_service import MeasurementService
from utils.date_utils import parse_date

router = APIRouter(tags=["measurements"])
measurement_service = MeasurementService()


@router.get("/measurements", response_model=List[MeasurementResponse])
async def get_measurements(
    signal_ids: List[str] = Query(..., min_items=1, description="Signal IDs"),
    from_date: str = Query(..., alias="from", description="Start date (ISO format)"),
    to_date: str = Query(..., alias="to", description="End date (ISO format)"),
):
    """Get measurements for specified signals and date range."""
    from_dt = parse_date(from_date)
    to_dt = parse_date(to_date)

    return measurement_service.get_measurements(signal_ids, from_dt, to_dt)


@router.get("/measurements/stats/{signal_id}", response_model=MeasurementStatsResponse)
async def get_signal_stats(
    signal_id: str = Path(..., min_length=1, description="Signal ID"),
    from_date: str = Query(..., alias="from", description="Start date (ISO format)"),
    to_date: str = Query(..., alias="to", description="End date (ISO format)"),
):
    """Calculate statistics for a signal over a date range."""
    from_dt = parse_date(from_date)
    to_dt = parse_date(to_date)

    return measurement_service.calculate_signal_stats(signal_id, from_dt, to_dt)
