"""Asset schema definitions."""

from typing import List, Optional

from pydantic import BaseModel, field_validator


class AssetResponse(BaseModel):
    """Schema for asset API response."""

    asset_id: str

    signals: List["SignalResponse"]

    @field_validator("asset_id")
    @classmethod
    def _non_empty_asset_id(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("asset_id must be non-empty")
        return value

    model_config = {
        "json_schema_extra": {
            "example": {
                "asset_id": "1",
                "signals": [
                    {
                        "signal_gid": "045ad75f-d8c7-4c92-b252-05f515e4006f",
                        "signal_id": "427038",
                        "signal_name": "BEZOBF110BIRMENU_L12",
                        "asset_id": "1",
                        "unit": "kV",
                    }
                ],
            }
        }
    }


class SignalResponse(BaseModel):
    """Schema for signal data in asset responses."""

    signal_gid: Optional[str]
    signal_id: Optional[str]
    signal_name: Optional[str]
    asset_id: Optional[str]
    unit: Optional[str]

    @field_validator("signal_id")
    @classmethod
    def _non_empty_signal_id(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("signal_id must be non-empty when provided")
        return value

    model_config = {
        "json_schema_extra": {
            "example": {
                "signal_gid": "045ad75f-d8c7-4c92-b252-05f515e4006f",
                "signal_id": "427038",
                "signal_name": "BEZOBF110BIRMENU_L12",
                "asset_id": "1",
                "unit": "kV",
            }
        }
    }


# Resolve forward reference for SignalResponse in AssetResponse.
AssetResponse.model_rebuild()
