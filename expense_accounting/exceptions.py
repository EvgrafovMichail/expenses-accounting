class ApplicationBaseError(Exception):
    """Base exception of expense accounting application."""


class DataLoaderError(ApplicationBaseError):
    """Exception caused by data loading errors."""
