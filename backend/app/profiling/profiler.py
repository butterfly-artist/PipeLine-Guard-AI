from typing import Dict, Optional, List
import pandas as pd
from app.core.contracts import DatasetProfile, ColumnProfile, Relationship
from app.profiling.statistics import calculate_column_profile


def profile_dataset(
    df: pd.DataFrame,
    dataset_name: str = "dataset"
) -> DatasetProfile:
    """
    Computes a complete, deterministic statistical profile of a dataset DataFrame.
    """
    total_rows = len(df)
    total_cols = len(df.columns)
    duplicate_rows = int(df.duplicated().sum())
    memory_usage_bytes = int(df.memory_usage(deep=True).sum())

    columns_profile: Dict[str, ColumnProfile] = {}
    for col in df.columns:
        columns_profile[col] = calculate_column_profile(col, df[col], total_rows)

    return DatasetProfile(
        dataset_name=dataset_name,
        row_count=total_rows,
        column_count=total_cols,
        duplicate_rows=duplicate_rows,
        memory_usage_bytes=memory_usage_bytes,
        columns=columns_profile,
        relationships=[],
    )
