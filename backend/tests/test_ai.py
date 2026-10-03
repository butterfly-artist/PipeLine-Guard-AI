from app.ai.gemma_client import GemmaClient
from app.ai.context_builder import build_ai_context
from app.core.contracts import DiagnosisResult, Severity


def test_context_builder():
    ctx = build_ai_context(
        profiles={},
        dq_results=[],
        relationships=[],
        logs=[]
    )
    assert "datasets" in ctx
    assert "dq_summary" in ctx


def test_gemma_client_fallback():
    client = GemmaClient(api_key="")
    ctx = {"dq_summary": {"failures": []}, "datasets": []}
    res = client.generate_diagnosis(ctx)

    assert isinstance(res, DiagnosisResult)
    assert res.severity in (Severity.LOW, Severity.MEDIUM, Severity.HIGH, Severity.CRITICAL)
