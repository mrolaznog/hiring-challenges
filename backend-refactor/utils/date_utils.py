"""Date and time utilities."""

from datetime import datetime


def parse_date(date_str: str) -> datetime:
    """Parse date string to datetime."""
    return datetime.fromisoformat(date_str)


def validate_date_range(from_date: datetime, to_date: datetime) -> bool:
    """Validate that from_date is before to_date."""
    return from_date < to_date
