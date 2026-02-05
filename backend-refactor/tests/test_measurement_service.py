from datetime import datetime

import pytest
from core.exceptions import ValidationError
from services.measurement_service import MeasurementService


def test_get_measurements_invalid_signal_ids():
    service = MeasurementService()
    with pytest.raises(ValidationError):
        service.get_measurements(["", "  "], datetime(2021, 1, 1), datetime(2021, 1, 2))


def test_get_measurements_invalid_date_range():
    service = MeasurementService()
    with pytest.raises(ValidationError):
        service.get_measurements(["1"], datetime(2021, 1, 2), datetime(2021, 1, 1))


def test_get_measurements_returns_models(monkeypatch):
    def _fake_get_measurements(signal_ids, from_date, to_date):
        return [
            {
                "signal_id": signal_ids[0],
                "timestamp": datetime(2021, 1, 1, 0, 0, 0).isoformat(),
                "value": 123.4,
                "unit": "kV",
            }
        ]

    monkeypatch.setattr(
        "services.measurement_service.get_measurements", _fake_get_measurements
    )

    service = MeasurementService()
    result = service.get_measurements(["1"], datetime(2021, 1, 1), datetime(2021, 1, 2))

    assert len(result) == 1
    assert result[0].signal_id == "1"


def test_calculate_signal_stats_no_measurements(monkeypatch):
    def _fake_get_measurements(signal_ids, from_date, to_date):
        return []

    monkeypatch.setattr(
        "services.measurement_service.get_measurements", _fake_get_measurements
    )

    service = MeasurementService()
    stats = service.calculate_signal_stats(
        "1", datetime(2021, 1, 1), datetime(2021, 1, 2)
    )

    assert stats.count == 0
    assert stats.signal_id == "1"


def test_calculate_signal_stats_with_measurements(monkeypatch):
    def _fake_get_measurements(signal_ids, from_date, to_date):
        return [
            {"value": 1.0},
            {"value": 2.0},
            {"value": 3.0},
        ]

    monkeypatch.setattr(
        "services.measurement_service.get_measurements", _fake_get_measurements
    )

    service = MeasurementService()
    stats = service.calculate_signal_stats(
        "1", datetime(2021, 1, 1), datetime(2021, 1, 2)
    )

    assert stats.count == 3
    assert stats.mean == 2.0
