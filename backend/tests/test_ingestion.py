from pathlib import Path
import pytest
import pandas as pd

from app.ingestion import (
    load_dataset,
    UnsupportedFormatError,
    DatasetLoadError,
    InvalidDatasetError,
)
from app.core.contracts import DatasetMetadata

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_csv_ingestion():
    csv_path = FIXTURES_DIR / "sample.csv"
    df, metadata = load_dataset(csv_path)

    assert isinstance(df, pd.DataFrame)
    assert isinstance(metadata, DatasetMetadata)
    assert metadata.source_type == "csv"
    assert metadata.rows == 3
    assert metadata.columns == 3
    assert metadata.column_names == ["id", "name", "value"]
    assert metadata.filename == "sample.csv"


def test_json_ingestion():
    json_path = FIXTURES_DIR / "sample.json"
    df, metadata = load_dataset(json_path)

    assert isinstance(df, pd.DataFrame)
    assert isinstance(metadata, DatasetMetadata)
    assert metadata.source_type == "json"
    assert metadata.rows == 3
    assert metadata.columns == 3
    assert metadata.column_names == ["id", "name", "value"]


def test_jsonl_ingestion():
    jsonl_path = FIXTURES_DIR / "sample.jsonl"
    df, metadata = load_dataset(jsonl_path)

    assert isinstance(df, pd.DataFrame)
    assert isinstance(metadata, DatasetMetadata)
    assert metadata.source_type == "jsonl"
    assert metadata.rows == 3
    assert metadata.columns == 3


def test_parquet_ingestion():
    parquet_path = FIXTURES_DIR / "sample.parquet"
    df, metadata = load_dataset(parquet_path)

    assert isinstance(df, pd.DataFrame)
    assert isinstance(metadata, DatasetMetadata)
    assert metadata.source_type == "parquet"
    assert metadata.rows == 3
    assert metadata.columns == 3
    assert metadata.column_names == ["id", "name", "value"]


def test_unsupported_format_error(tmp_path):
    txt_file = tmp_path / "sample.txt"
    txt_file.write_text("dummy text content")

    with pytest.raises(UnsupportedFormatError) as exc_info:
        load_dataset(txt_file)
    assert "Unsupported file format '.txt'" in str(exc_info.value)


def test_missing_file_error():
    with pytest.raises(DatasetLoadError):
        load_dataset("non_existent_file.csv")


def test_empty_csv_error(tmp_path):
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text("")

    with pytest.raises(InvalidDatasetError):
        load_dataset(empty_csv)


def test_malformed_json_error(tmp_path):
    bad_json = tmp_path / "bad.json"
    bad_json.write_text("{this is invalid json")

    with pytest.raises(InvalidDatasetError):
        load_dataset(bad_json)
