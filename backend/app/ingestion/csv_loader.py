from pathlib import Path
from typing import Tuple
import pandas as pd
from app.core.contracts import DatasetMetadata
from app.ingestion.base import BaseLoader
from app.ingestion.exceptions import DatasetLoadError, InvalidDatasetError


class CSVLoader(BaseLoader):
    """Loader for CSV files."""

    def load(self, file_path: Path) -> Tuple[pd.DataFrame, DatasetMetadata]:
        path = Path(file_path)
        if not path.exists():
            raise DatasetLoadError(f"File not found: {path}")

        try:
            df = pd.read_csv(path)
        except pd.errors.EmptyDataError:
            raise InvalidDatasetError(f"CSV dataset file is empty: {path.name}")
        except Exception as e:
            raise DatasetLoadError(f"Failed to read CSV file '{path.name}': {str(e)}")

        file_size = path.stat().st_size if path.exists() else 0
        metadata = DatasetMetadata(
            source_type="csv",
            rows=len(df),
            columns=len(df.columns),
            column_names=list(df.columns),
            filename=path.name,
            file_size_bytes=file_size
        )
        return df, metadata
