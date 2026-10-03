from pathlib import Path
from typing import Dict, List, Optional, Union
import pandas as pd

from app.core.contracts import (
    AnalysisResponse,
    DatasetProfile,
    DQRule,
    DQResult,
    Relationship,
    PipelineLogEvent,
    RuleType,
    Severity,
)
from app.ingestion import load_dataset
from app.profiling import profile_dataset, detect_relationships
from app.quality import DQEngine, generate_default_rules
from app.pipeline import parse_pipeline_logs
from app.ai import diagnose_pipeline_incident


class AnalysisService:
    """End-to-end data pipeline intelligence orchestrator."""

    def analyze(
        self,
        dataset_paths: List[Union[str, Path]],
        log_path: Optional[Union[str, Path]] = None,
        custom_rules: Optional[List[DQRule]] = None
    ) -> AnalysisResponse:
        """
        Executes end-to-end pipeline analysis:
        Ingestion -> Profiling -> Schema & Relationships -> DQ Execution -> Log Parsing -> Gemma AI Diagnosis.
        """
        loaded_dfs: Dict[str, pd.DataFrame] = {}
        profiles: Dict[str, DatasetProfile] = {}

        # 1. Ingestion & Profiling
        for path_item in dataset_paths:
            p = Path(path_item)
            df, meta = load_dataset(p)
            dataset_name = p.name
            loaded_dfs[dataset_name] = df
            profiles[dataset_name] = profile_dataset(df, dataset_name=dataset_name)

        # 2. Schema & Relationship Detection
        relationships: List[Relationship] = detect_relationships(profiles)

        # 3. Rule Assembly & DQ Execution
        rules_to_run: List[DQRule] = []

        for name, prof in profiles.items():
            rules_to_run.extend(generate_default_rules(prof))

        if custom_rules:
            rules_to_run.extend(custom_rules)

        # Domain-agnostic demo enhancement: If payments and orders datasets are present, add reconciliation rule
        if "payments.csv" in loaded_dfs and "orders.csv" in loaded_dfs:
            rules_to_run.append(
                DQRule(
                    rule_id="DQ-PAY-001",
                    column="payment_total",
                    type=RuleType.RECONCILIATION,
                    severity=Severity.CRITICAL,
                    params={
                        "dataset": "payments.csv",
                        "target_dataset": "orders.csv",
                        "join_column": "order_id",
                        "value_column_1": "payment_total",
                        "value_column_2": "order_amount",
                        "tolerance": 0.01
                    }
                )
            )

        dq_engine = DQEngine(loaded_dfs)
        dq_results: List[DQResult] = dq_engine.execute_rules(rules_to_run)

        # 4. Pipeline Log Parsing
        logs: List[PipelineLogEvent] = []
        if log_path:
            p_log = Path(log_path)
            if p_log.exists():
                logs = parse_pipeline_logs(p_log)

        # 5. Gemma AI Diagnosis
        primary_profile = next(iter(profiles.values())) if profiles else None
        diagnosis = diagnose_pipeline_incident(profiles, dq_results, relationships, logs)

        return AnalysisResponse(
            profile=primary_profile,
            dq_results=dq_results,
            diagnosis=diagnosis
        )


analysis_service = AnalysisService()
