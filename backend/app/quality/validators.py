from typing import Dict, Any, Tuple
import re
import pandas as pd
from app.core.contracts import DQRule, DQResult, DQStatus, RuleType, Severity


def validate_not_null(df: pd.DataFrame, rule: DQRule) -> DQResult:
    col = rule.column
    checked_rows = len(df)
    if col not in df.columns:
        return DQResult(
            rule_id=rule.rule_id,
            status=DQStatus.FAIL,
            checked_rows=checked_rows,
            failed_rows=checked_rows,
            failure_rate=100.0,
            details=f"Column '{col}' does not exist in dataset."
        )

    failed_rows = int(df[col].isnull().sum())
    failure_rate = round((failed_rows / checked_rows * 100.0), 4) if checked_rows > 0 else 0.0
    status = DQStatus.PASS if failed_rows == 0 else DQStatus.FAIL

    return DQResult(
        rule_id=rule.rule_id,
        status=status,
        checked_rows=checked_rows,
        failed_rows=failed_rows,
        failure_rate=failure_rate,
        details=f"{failed_rows} null records found in column '{col}'." if failed_rows > 0 else "Passed."
    )


def validate_unique(df: pd.DataFrame, rule: DQRule) -> DQResult:
    col = rule.column
    checked_rows = len(df)
    if col not in df.columns:
        return DQResult(
            rule_id=rule.rule_id,
            status=DQStatus.FAIL,
            checked_rows=checked_rows,
            failed_rows=checked_rows,
            failure_rate=100.0,
            details=f"Column '{col}' does not exist in dataset."
        )

    non_null_s = df[col].dropna()
    duplicated_mask = non_null_s.duplicated(keep=False)
    failed_rows = int(duplicated_mask.sum())
    failure_rate = round((failed_rows / checked_rows * 100.0), 4) if checked_rows > 0 else 0.0
    status = DQStatus.PASS if failed_rows == 0 else DQStatus.FAIL

    return DQResult(
        rule_id=rule.rule_id,
        status=status,
        checked_rows=checked_rows,
        failed_rows=failed_rows,
        failure_rate=failure_rate,
        details=f"{failed_rows} duplicate records found in column '{col}'." if failed_rows > 0 else "Passed."
    )


def validate_range(df: pd.DataFrame, rule: DQRule) -> DQResult:
    col = rule.column
    checked_rows = len(df)
    if col not in df.columns:
        return DQResult(
            rule_id=rule.rule_id,
            status=DQStatus.FAIL,
            checked_rows=checked_rows,
            failed_rows=checked_rows,
            failure_rate=100.0,
            details=f"Column '{col}' does not exist."
        )

    min_val = rule.params.get("min")
    max_val = rule.params.get("max")

    series = pd.to_numeric(df[col], errors="coerce")
    mask = pd.Series(False, index=df.index)

    if min_val is not None:
        mask = mask | (series < min_val)
    if max_val is not None:
        mask = mask | (series > max_val)

    failed_rows = int(mask.sum())
    failure_rate = round((failed_rows / checked_rows * 100.0), 4) if checked_rows > 0 else 0.0
    status = DQStatus.PASS if failed_rows == 0 else DQStatus.FAIL

    return DQResult(
        rule_id=rule.rule_id,
        status=status,
        checked_rows=checked_rows,
        failed_rows=failed_rows,
        failure_rate=failure_rate,
        details=f"{failed_rows} records out of range [{min_val}, {max_val}] in column '{col}'." if failed_rows > 0 else "Passed."
    )


def validate_format(df: pd.DataFrame, rule: DQRule) -> DQResult:
    col = rule.column
    pattern = rule.params.get("pattern", "")
    checked_rows = len(df)

    if col not in df.columns or not pattern:
        return DQResult(
            rule_id=rule.rule_id,
            status=DQStatus.WARNING,
            checked_rows=checked_rows,
            failed_rows=0,
            failure_rate=0.0,
            details="Invalid format rule parameter or missing column."
        )

    regex = re.compile(pattern)
    series = df[col].dropna().astype(str)
    failed_rows = int(series.apply(lambda x: not bool(regex.search(x))).sum())
    failure_rate = round((failed_rows / checked_rows * 100.0), 4) if checked_rows > 0 else 0.0
    status = DQStatus.PASS if failed_rows == 0 else DQStatus.FAIL

    return DQResult(
        rule_id=rule.rule_id,
        status=status,
        checked_rows=checked_rows,
        failed_rows=failed_rows,
        failure_rate=failure_rate,
        details=f"{failed_rows} records failed format regex match in column '{col}'." if failed_rows > 0 else "Passed."
    )


def validate_referential_integrity(
    source_df: pd.DataFrame,
    target_df: pd.DataFrame,
    rule: DQRule
) -> DQResult:
    col = rule.column
    target_col = rule.params.get("target_column", col)
    checked_rows = len(source_df)

    if col not in source_df.columns or target_col not in target_df.columns:
        return DQResult(
            rule_id=rule.rule_id,
            status=DQStatus.FAIL,
            checked_rows=checked_rows,
            failed_rows=checked_rows,
            failure_rate=100.0,
            details="Referential integrity column missing in source or target."
        )

    source_values = source_df[col].dropna().unique()
    target_values = set(target_df[target_col].dropna().unique())

    unmatched = set(source_values) - target_values
    failed_mask = source_df[col].isin(unmatched)
    failed_rows = int(failed_mask.sum())
    failure_rate = round((failed_rows / checked_rows * 100.0), 4) if checked_rows > 0 else 0.0
    status = DQStatus.PASS if failed_rows == 0 else DQStatus.FAIL

    return DQResult(
        rule_id=rule.rule_id,
        status=status,
        checked_rows=checked_rows,
        failed_rows=failed_rows,
        failure_rate=failure_rate,
        details=f"{failed_rows} records in source column '{col}' reference missing key in target column '{target_col}'." if failed_rows > 0 else "Passed."
    )


def validate_reconciliation(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    rule: DQRule
) -> DQResult:
    """Reconcile values across linked datasets (e.g., payments vs orders)."""
    join_col = rule.params.get("join_column", rule.column)
    val_col1 = rule.params.get("value_column_1", rule.column)
    val_col2 = rule.params.get("value_column_2", rule.column)
    tolerance = rule.params.get("tolerance", 0.01)

    checked_rows = len(df1)
    if join_col not in df1.columns or join_col not in df2.columns or val_col1 not in df1.columns or val_col2 not in df2.columns:
        return DQResult(
            rule_id=rule.rule_id,
            status=DQStatus.FAIL,
            checked_rows=checked_rows,
            failed_rows=checked_rows,
            failure_rate=100.0,
            details="Required join or value columns missing for reconciliation check."
        )

    sub1 = df1[[join_col, val_col1]].rename(columns={val_col1: "val_src"})
    sub2 = df2[[join_col, val_col2]].rename(columns={val_col2: "val_tgt"})

    merged = pd.merge(sub1, sub2, on=join_col, how="inner")
    v1 = pd.to_numeric(merged["val_src"], errors="coerce")
    v2 = pd.to_numeric(merged["val_tgt"], errors="coerce")

    diff = (v1 - v2).abs()
    failed_mask = diff > tolerance
    failed_rows = int(failed_mask.sum())
    failure_rate = round((failed_rows / len(merged) * 100.0), 4) if len(merged) > 0 else 0.0
    status = DQStatus.PASS if failed_rows == 0 else DQStatus.FAIL

    return DQResult(
        rule_id=rule.rule_id,
        status=status,
        checked_rows=len(merged),
        failed_rows=failed_rows,
        failure_rate=failure_rate,
        details=f"{failed_rows} records failed monetary/numeric reconciliation check between '{val_col1}' and '{val_col2}'." if failed_rows > 0 else "Passed."
    )
