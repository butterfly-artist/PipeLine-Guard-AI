import json
from pathlib import Path
from typing import Tuple
import pandas as pd
from app.core.contracts import DatasetMetadata
from app.ingestion.base import BaseLoader
from app.ingestion.exceptions import DatasetLoadError, InvalidDatasetError


class JSONLoader(BaseLoader):
    """Loader for JSON and JSON Lines (JSONL) files."""

    def load(self, file_path: Path) -> Tuple[pd.DataFrame, DatasetMetadata]:
        path = Path(file_path)
        if not path.exists():
            raise DatasetLoadError(f"File not found: {path}")

        df = None
        source_type = "jsonl" if path.suffix.lower() == ".jsonl" else "json"

        try:
            # First try reading as standard JSON array/records
            df = pd.read_json(path)
        except Exception:
            try:
                # Fallback to lines=True for JSON Lines
                df = pd.read_json(path, lines=True)
                source_type = "jsonl"
            except Exception:
                # Fallback using stdlib json to detect invalid structure
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if isinstance(data, list):
                        df = pd.DataFrame(data)
                    elif isinstance(data, dict):
                        df = pd.DataFrame([data])
                    else:
                        raise InvalidDatasetError(f"JSON content in '{path.name}' cannot be converted to tabular format.")
                except json.JSONDecodeError as e:
                    raise InvalidDatasetError(f"Malformed JSON in file '{path.name}': {str(e)}")
                except Exception as e:
                    raise DatasetLoadError(f"Failed to load JSON file '{path.name}': {str(e)}")

        if df is None:
            raise DatasetLoadError(f"Failed to read JSON file '{path.name}'")

        if df.empty and path.stat().st_size == 0:
            raise InvalidDatasetError(f"JSON dataset file is empty: {path.name}")

        file_size = path.stat().st_size if path.exists() else 0
        metadata = DatasetMetadata(
            source_type=source_type,
            rows=len(df),
            columns=len(df.columns),
            column_names=list(df.columns),
            filename=path.name,
            file_size_bytes=file_size
        )
        return df, metadata
