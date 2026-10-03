from pathlib import Path
from typing import Tuple, Union
import pandas as pd
from app.core.contracts import DatasetMetadata
from app.ingestion.csv_loader import CSVLoader
from app.ingestion.json_loader import JSONLoader
from app.ingestion.parquet_loader import ParquetLoader
from app.ingestion.exceptions import UnsupportedFormatError, DatasetLoadError


LOADERS = {
    ".csv": CSVLoader(),
    ".json": JSONLoader(),
    ".jsonl": JSONLoader(),
    ".parquet": ParquetLoader(),
}


def load_dataset(file_path: Union[str, Path]) -> Tuple[pd.DataFrame, DatasetMetadata]:
    """
    Main entrypoint for data ingestion.
    Determines file format from extension and delegates to the appropriate loader.
    
    Returns:
        Tuple[pd.DataFrame, DatasetMetadata]
    Raises:
        UnsupportedFormatError: If file extension is not supported.
        DatasetLoadError: If file read/parse fails.
        InvalidDatasetError: If dataset is empty or malformed.
    """
    path = Path(file_path)
    if not path.exists():
        raise DatasetLoadError(f"Dataset file does not exist: {path}")

    ext = path.suffix.lower()
    if ext not in LOADERS:
        raise UnsupportedFormatError(
            f"Unsupported file format '{ext}' for file '{path.name}'. "
            f"Supported formats: {list(LOADERS.keys())}"
        )

    loader = LOADERS[ext]
    return loader.load(path)
