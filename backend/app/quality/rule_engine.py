from typing import Dict, List, Optional, Union
import pandas as pd
from app.core.contracts import DQRule, DQResult, DQStatus, RuleType, Severity
from app.quality.validators import (
    validate_not_null,
    validate_unique,
    validate_range,
    validate_format,
    validate_referential_integrity,
    validate_reconciliation,
)


class DQEngine:
    """Deterministic Data Quality Engine."""

    def __init__(self, datasets: Optional[Dict[str, pd.DataFrame]] = None):
        self.datasets: Dict[str, pd.DataFrame] = datasets or {}

    def add_dataset(self, name: str, df: pd.DataFrame) -> None:
        self.datasets[name] = df

    def execute_rule(self, rule: DQRule, primary_dataset_name: Optional[str] = None) -> DQResult:
        """Execute a single DQ rule against registered dataset(s)."""
        ds_name = rule.params.get("dataset", primary_dataset_name)
        if ds_name not in self.datasets and self.datasets:
            ds_name = next(iter(self.datasets.keys()))

        df = self.datasets.get(ds_name)
        if df is None:
            return DQResult(
                rule_id=rule.rule_id,
                status=DQStatus.FAIL,
                checked_rows=0,
                failed_rows=0,
                failure_rate=0.0,
                details=f"Dataset '{ds_name}' not available for rule execution."
            )

        if rule.type == RuleType.NOT_NULL:
            return validate_not_null(df, rule)
        elif rule.type == RuleType.UNIQUE:
            return validate_unique(df, rule)
        elif rule.type == RuleType.RANGE:
            return validate_range(df, rule)
        elif rule.type == RuleType.FORMAT:
            return validate_format(df, rule)
        elif rule.type == RuleType.REFERENTIAL_INTEGRITY:
            target_ds_name = rule.params.get("target_dataset")
            target_df = self.datasets.get(target_ds_name)
            if target_df is None:
                return DQResult(
                    rule_id=rule.rule_id,
                    status=DQStatus.FAIL,
                    checked_rows=len(df),
                    failed_rows=len(df),
                    failure_rate=100.0,
                    details=f"Target dataset '{target_ds_name}' not found for referential integrity check."
                )
            return validate_referential_integrity(df, target_df, rule)
        elif rule.type == RuleType.RECONCILIATION:
            target_ds_name = rule.params.get("target_dataset")
            target_df = self.datasets.get(target_ds_name)
            if target_df is None:
                return DQResult(
                    rule_id=rule.rule_id,
                    status=DQStatus.FAIL,
                    checked_rows=len(df),
                    failed_rows=len(df),
                    failure_rate=100.0,
                    details=f"Target dataset '{target_ds_name}' not found for reconciliation check."
                )
            return validate_reconciliation(df, target_df, rule)

        return DQResult(
            rule_id=rule.rule_id,
            status=DQStatus.WARNING,
            checked_rows=len(df),
            failed_rows=0,
            failure_rate=0.0,
            details=f"Unsupported rule type '{rule.type}'."
        )

    def execute_rules(self, rules: List[DQRule], primary_dataset_name: Optional[str] = None) -> List[DQResult]:
        """Execute a list of DQ rules."""
        results = []
        for r in rules:
            results.append(self.execute_rule(r, primary_dataset_name))
        return results
