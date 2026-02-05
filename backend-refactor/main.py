"""Main entry point for the application."""

import uvicorn
from app import create_app
from core.config import get_settings
from helpers.startup import startup

app = create_app()
startup(app)

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug_mode,
    )
