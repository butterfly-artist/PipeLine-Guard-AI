from typing import Dict, List, Optional, Any
from app.core.contracts import (
    DatasetProfile,
    SchemaDefinition,
    Relationship,
    DQResult,
    PipelineLogEvent,
    DQStatus,
)


def build_ai_context(
    profiles: Dict[str, DatasetProfile],
    dq_results: List[DQResult],
    relationships: List[Relationship],
    logs: List[PipelineLogEvent],
    schemas: Optional[Dict[str, SchemaDefinition]] = None
) -> Dict[str, Any]:
    """
    Compiles deterministic profiling, DQ results, schema, and log events
    into a compact, structured AI evidence context dictionary.
    """
    datasets_summary = []
    for name, prof in profiles.items():
        col_summaries = []
        for col_name, c_prof in prof.columns.items():
            col_summaries.append({
                "column": col_name,
                "type": c_prof.data_type,
                "null_pct": c_prof.null_percentage,
                "unique_pct": c_prof.unique_percentage,
                "min": c_prof.min_value,
                "max": c_prof.max_value,
                "patterns": c_prof.detected_patterns
            })

        datasets_summary.append({
            "name": name,
            "row_count": prof.row_count,
            "column_count": prof.column_count,
            "duplicate_rows": prof.duplicate_rows,
            "columns": col_summaries
        })

    # Filter DQ failures & warnings
    failures = []
    passes_count = 0
    for r in dq_results:
        if r.status in (DQStatus.FAIL, DQStatus.WARNING):
            failures.append({
                "rule_id": r.rule_id,
                "status": r.status.value,
                "checked_rows": r.checked_rows,
                "failed_rows": r.failed_rows,
                "failure_rate_pct": r.failure_rate,
                "details": r.details
            })
        else:
            passes_count += 1

    # Filter log errors
    log_errors = []
    for l in logs:
        if l.log_level in ("ERROR", "CRITICAL", "WARN", "WARNING", "FATAL"):
            log_errors.append({
                "level": l.log_level,
                "component": l.component,
                "message": l.message
            })

    rel_summary = [
        f"{r.source_column} -> {r.target_dataset}.{r.target_column} ({r.relationship_type})"
        for r in relationships
    ]

    return {
        "datasets": datasets_summary,
        "dq_summary": {
            "passed_rules_count": passes_count,
            "failed_rules_count": len(failures),
            "failures": failures
        },
        "relationships": rel_summary,
        "pipeline_log_errors": log_errors
    }
