class IngestionError(Exception):
    """Base exception for all dataset ingestion failures."""
    pass


class UnsupportedFormatError(IngestionError):
    """Raised when an unsupported file extension or format is provided."""
    pass


class DatasetLoadError(IngestionError):
    """Raised when a dataset cannot be read or parsed."""
    pass


class InvalidDatasetError(IngestionError):
    """Raised when a loaded dataset is empty or invalid."""
    pass
