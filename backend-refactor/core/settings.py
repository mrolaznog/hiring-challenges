"""Application settings and environment variables."""

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Application settings loaded from environment."""

    app_name: str = "AssetAPI"
    api_version: str = "v1"
    debug_mode: bool = True
    signals_path: str = "data/signal.json"
    measurements_path: str = "data/measurements.csv"

    model_config = ConfigDict(env_file=".env")
