import pytest
from core.exceptions import NotFoundError
from services.asset_service import AssetService


def test_get_all_assets_raises_when_empty(monkeypatch):
    def _empty_assets():
        return []

    monkeypatch.setattr("services.asset_service.get_assets", _empty_assets)

    service = AssetService()
    with pytest.raises(NotFoundError):
        service.get_all_assets()


def test_get_all_assets_returns_formatted_assets(monkeypatch):
    def _assets():
        return [
            {
                "asset_id": "1",
                "signals": [
                    {
                        "signal_gid": "gid",
                        "signal_id": "sid",
                        "signal_name": "name",
                        "asset_id": "1",
                        "unit": "kV",
                    }
                ],
            }
        ]

    monkeypatch.setattr("services.asset_service.get_assets", _assets)

    service = AssetService()
    result = service.get_all_assets()

    assert len(result) == 1
    assert result[0].asset_id == "1"
    assert result[0].signals[0].signal_id == "sid"
