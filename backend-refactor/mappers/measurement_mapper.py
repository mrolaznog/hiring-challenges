"""Measurement mapping utilities."""
from typing import Dict

from schemas.measurement_schema import MeasurementResponse


def to_measurement_response(measurement: Dict) -> MeasurementResponse:
    """Map a raw measurement dict to a response model."""
    return MeasurementResponse(
        signal_id=measurement.get("signal_id"),
        timestamp=measurement.get("timestamp"),
        value=measurement.get("value"),
        unit="W",
    )
