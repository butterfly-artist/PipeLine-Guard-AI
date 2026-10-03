from typing import Dict, List, Optional
import pandas as pd
from app.core.contracts import (
    SchemaDefinition,
    SchemaField,
    DatasetProfile,
    Relationship,
)


def detect_schema(df: pd.DataFrame, schema_name: str = "default_schema") -> SchemaDefinition:
    """Infer candidate schema definition from a pandas DataFrame."""
    fields: List[SchemaField] = []
    total_rows = len(df)

    for col in df.columns:
        series = df[col]
        dtype = str(series.dtype)
        nullable = series.isnull().any()
        unique = bool(total_rows > 0 and series.nunique(dropna=True) == total_rows and not nullable)

        min_val = None
        max_val = None

        if pd.api.types.is_numeric_dtype(series) and not pd.api.types.is_bool_dtype(series):
            non_null = series.dropna()
            if not non_null.empty:
                min_val = float(non_null.min())
                max_val = float(non_null.max())

        fields.append(
            SchemaField(
                column_name=col,
                data_type=dtype,
                nullable=nullable,
                unique=unique,
                minimum=min_val,
                maximum=max_val,
            )
        )

    return SchemaDefinition(name=schema_name, fields=fields)


def detect_candidate_keys(profile: DatasetProfile) -> List[str]:
    """Identify candidate keys from a DatasetProfile."""
    candidate_keys = []
    for col_name, col_prof in profile.columns.items():
        if col_prof.null_count == 0 and col_prof.unique_count == profile.row_count and profile.row_count > 0:
            candidate_keys.append(col_name)
    return candidate_keys


def detect_relationships(profiles: Dict[str, DatasetProfile]) -> List[Relationship]:
    """
    Detect candidate cross-dataset relationships (e.g. FK relationships)
    based on column naming conventions and matching candidate keys.
    """
    relationships: List[Relationship] = []

    # Map candidate keys across all datasets
    dataset_keys: Dict[str, List[str]] = {}
    for name, prof in profiles.items():
        dataset_keys[name] = detect_candidate_keys(prof)

    for source_name, source_prof in profiles.items():
        for col_name in source_prof.columns.keys():
            # Check if this column matches a candidate key in another table
            for target_name, keys in dataset_keys.items():
                if source_name == target_name:
                    continue
                if col_name in keys:
                    relationships.append(
                        Relationship(
                            source_column=col_name,
                            target_dataset=target_name,
                            target_column=col_name,
                            relationship_type="INFERRED_FOREIGN_KEY"
                        )
                    )

    return relationships
