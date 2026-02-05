from datetime import datetime

from db.measurement_db import get_measurements
from db.signal_db import load_signals


def test_load_signals_returns_normalized_data():
    signals = load_signals()
    assert isinstance(signals, list)
    assert len(signals) > 0
    sample = signals[0]
    assert "signal_id" in sample
    assert "asset_id" in sample


def test_get_measurements_reads_csv_and_filters():
    # Use a broad date range to ensure data is returned
    from_date = datetime(2021, 11, 7, 0, 0, 0)
    to_date = datetime(2021, 11, 7, 23, 59, 59)

    results = get_measurements(["427038"], from_date, to_date)
    assert isinstance(results, list)
    assert len(results) > 0
    for row in results:
        assert row["signal_id"] == "427038"
        assert from_date <= row["timestamp"] <= to_date
