from typing import Dict, List, Optional
from app.core.contracts import (
    DatasetProfile,
    Relationship,
    DQResult,
    PipelineLogEvent,
    DiagnosisResult,
)
from app.ai.context_builder import build_ai_context
from app.ai.gemma_client import GemmaClient


def diagnose_pipeline_incident(
    profiles: Dict[str, DatasetProfile],
    dq_results: List[DQResult],
    relationships: List[Relationship],
    logs: List[PipelineLogEvent],
    gemma_client: Optional[GemmaClient] = None
) -> DiagnosisResult:
    """
    Builds context, invokes Gemma reasoning engine, and returns a validated DiagnosisResult.
    """
    context = build_ai_context(profiles, dq_results, relationships, logs)
    client = gemma_client or GemmaClient()
    return client.generate_diagnosis(context)
