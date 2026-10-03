from typing import Any, Dict, Optional
import numpy as np
import pandas as pd
from app.core.contracts import ColumnProfile
from app.profiling.patterns import detect_column_patterns


def calculate_column_profile(col_name: str, series: pd.Series, total_rows: int) -> ColumnProfile:
    """Calculate detailed column statistical profile."""
    null_count = int(series.isnull().sum())
    null_percentage = round((null_count / total_rows * 100.0), 2) if total_rows > 0 else 0.0

    unique_count = int(series.nunique(dropna=True))
    unique_percentage = round((unique_count / total_rows * 100.0), 2) if total_rows > 0 else 0.0

    data_type = str(series.dtype)

    min_val: Optional[Any] = None
    max_val: Optional[Any] = None
    mean_val: Optional[float] = None
    median_val: Optional[float] = None

    if pd.api.types.is_numeric_dtype(series) and not pd.api.types.is_bool_dtype(series):
        non_null = series.dropna()
        if not non_null.empty:
            min_val = float(non_null.min()) if not np.isnan(non_null.min()) else None
            max_val = float(non_null.max()) if not np.isnan(non_null.max()) else None
            mean_val = round(float(non_null.mean()), 4) if not np.isnan(non_null.mean()) else None
            median_val = round(float(non_null.median()), 4) if not np.isnan(non_null.median()) else None
    else:
        non_null = series.dropna()
        if not non_null.empty:
            min_val = str(non_null.min())
            max_val = str(non_null.max())

    patterns = detect_column_patterns(series)

    return ColumnProfile(
        column_name=col_name,
        data_type=data_type,
        null_count=null_count,
        null_percentage=null_percentage,
        unique_count=unique_count,
        unique_percentage=unique_percentage,
        min_value=min_val,
        max_value=max_val,
        mean=mean_val,
        median=median_val,
        detected_patterns=patterns,
    )
