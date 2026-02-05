"""Custom exceptions for the API."""


class NotFoundError(Exception):
    """Raised when a requested resource is not found."""

    pass


class ValidationError(Exception):
    """Raised when input validation fails."""

    pass
