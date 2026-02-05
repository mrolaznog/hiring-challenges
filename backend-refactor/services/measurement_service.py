"""Measurement service."""

import logging
import statistics
from datetime import datetime
from typing import List

from core.exceptions import ValidationError
from db.measurement_db import get_measurements
from mappers.measurement_mapper import to_measurement_response
from schemas.measurement_schema import (
    MeasurementResponse,
    MeasurementStatsResponse,
)
from utils.date_utils import validate_date_range

logger = logging.getLogger(__name__)


class MeasurementService:
    """Service for managing measurements."""

    def get_measurements(
        self, signal_ids: List[str], from_date: datetime, to_date: datetime
    ) -> List[MeasurementResponse]:
        """Get measurements for signals in date range."""
        logger.info("Fetching measurements for %d signals", len(signal_ids))
        cleaned_signal_ids = [sid.strip() for sid in signal_ids]
        if not cleaned_signal_ids or not all(cleaned_signal_ids):
            logger.warning("Invalid signal IDs provided")
            raise ValidationError("Signal IDs must be non-empty")

        if not validate_date_range(from_date, to_date):
            logger.warning("Invalid date range: %s to %s", from_date, to_date)
            raise ValidationError("Invalid date range: 'from' must be before 'to'")

        measurements = get_measurements(cleaned_signal_ids, from_date, to_date)
        response = [to_measurement_response(m) for m in measurements]
        logger.info("Fetched %d measurements", len(response))
        return response

    def calculate_signal_stats(
        self, signal_id: str, from_date: datetime, to_date: datetime
    ) -> MeasurementStatsResponse:
        """Calculate statistics for a signal over a date range."""
        logger.info("Calculating stats for signal_id=%s", signal_id)
        cleaned_signal_id = signal_id.strip()
        if not cleaned_signal_id:
            logger.warning("Empty signal ID provided")
            raise ValidationError("Signal ID must be non-empty")

        if not validate_date_range(from_date, to_date):
            logger.warning("Invalid date range: %s to %s", from_date, to_date)
            raise ValidationError("Invalid date range: 'from' must be before 'to'")

        measurements = get_measurements([cleaned_signal_id], from_date, to_date)

        if not measurements:
            logger.info("No measurements found for signal_id=%s", cleaned_signal_id)
            return MeasurementStatsResponse(
                signal_id=cleaned_signal_id,
                from_date=from_date,
                to_date=to_date,
                count=0,
                mean=None,
                min=None,
                max=None,
                median=None,
                std_dev=None,
            )

        values = [m["value"] for m in measurements]

        stats = MeasurementStatsResponse(
            signal_id=cleaned_signal_id,
            from_date=from_date,
            to_date=to_date,
            count=len(values),
            mean=round(statistics.mean(values), 2),
            min=round(min(values), 2),
            max=round(max(values), 2),
            median=round(statistics.median(values), 2),
            std_dev=round(statistics.stdev(values), 2) if len(values) > 1 else 0.0,
        )
        logger.info("Calculated stats for signal_id=%s", cleaned_signal_id)
        return stats
