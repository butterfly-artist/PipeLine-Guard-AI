from typing import List
import pandas as pd
from app.core.contracts import DQRule, RuleType, Severity, DatasetProfile


def generate_default_rules(profile: DatasetProfile) -> List[DQRule]:
    """Generate generic executable DQ rules based on dataset profile facts."""
    rules: List[DQRule] = []
    idx = 1

    for col_name, col_prof in profile.columns.items():
        # Add NOT_NULL rule for non-nullable candidate columns or ID columns
        if col_prof.null_count == 0 or col_name.lower().endswith("_id") or col_name.lower() == "id":
            rules.append(
                DQRule(
                    rule_id=f"DQ-GEN-{idx:03d}",
                    column=col_name,
                    type=RuleType.NOT_NULL,
                    severity=Severity.HIGH,
                )
            )
            idx += 1

        # Add UNIQUE rule for candidate keys
        if col_prof.unique_count == profile.row_count and profile.row_count > 0:
            rules.append(
                DQRule(
                    rule_id=f"DQ-GEN-{idx:03d}",
                    column=col_name,
                    type=RuleType.UNIQUE,
                    severity=Severity.HIGH,
                )
            )
            idx += 1

        # Add RANGE rule for non-negative numerical values
        if col_prof.min_value is not None and isinstance(col_prof.min_value, (int, float)) and col_prof.min_value >= 0:
            rules.append(
                DQRule(
                    rule_id=f"DQ-GEN-{idx:03d}",
                    column=col_name,
                    type=RuleType.RANGE,
                    severity=Severity.MEDIUM,
                    params={"min": 0.0}
                )
            )
            idx += 1

    return rules
