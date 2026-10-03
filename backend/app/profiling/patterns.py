import re
from typing import List
import pandas as pd

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$|^\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$")
UUID_REGEX = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$|^\d{4}/\d{2}/\d{2}$|^\d{2}/\d{2}/\d{4}$|^\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}")


def detect_column_patterns(series: pd.Series, max_samples: int = 100) -> List[str]:
    """Detect common string patterns in a pandas Series."""
    patterns = []
    non_null_s = series.dropna().astype(str)
    if non_null_s.empty:
        return patterns

    sample = non_null_s.iloc[:max_samples]

    # Email check
    if sample.apply(lambda x: bool(EMAIL_REGEX.match(x.strip()))).mean() > 0.7:
        patterns.append("email")

    # Phone check
    if sample.apply(lambda x: bool(PHONE_REGEX.match(x.strip()))).mean() > 0.7:
        patterns.append("phone")

    # UUID check
    if sample.apply(lambda x: bool(UUID_REGEX.match(x.strip()))).mean() > 0.7:
        patterns.append("uuid")

    # Date check
    if sample.apply(lambda x: bool(DATE_REGEX.match(x.strip()))).mean() > 0.7:
        patterns.append("date")

    # ID-like check (column ends with _id or id)
    col_name = str(series.name).lower()
    if col_name == "id" or col_name.endswith("_id") or col_name.endswith("id"):
        patterns.append("id_like")

    return patterns
