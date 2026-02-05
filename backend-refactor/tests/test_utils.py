from datetime import datetime

from utils.asset_helper import format_asset_response
from utils.date_utils import parse_date, validate_date_range


def test_format_asset_response():
    asset = {"asset_id": "1", "signals": ["a"]}
    result = format_asset_response(asset)
    assert result == {"asset_id": "1", "signals": ["a"]}


def test_format_asset_response_defaults():
    asset = {"asset_id": "1"}
    result = format_asset_response(asset)
    assert result == {"asset_id": "1", "signals": []}


def test_parse_date():
    dt = parse_date("2021-11-07T00:00:00")
    assert isinstance(dt, datetime)


def test_validate_date_range():
    assert validate_date_range(datetime(2021, 1, 1), datetime(2021, 1, 2))
    assert not validate_date_range(datetime(2021, 1, 2), datetime(2021, 1, 1))
