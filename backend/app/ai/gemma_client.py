import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger
from app.core.contracts import (
    DiagnosisResult,
    Severity,
    Evidence,
    ImpactItem,
    RemediationItem,
    QualityRuleSuggestion,
    RuleType,
)

SYSTEM_PROMPT_PATH = Path(__file__).parent.parent.parent.parent / "prompts" / "diagnosis.txt"


def load_system_prompt() -> str:
    if SYSTEM_PROMPT_PATH.exists():
        with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "You are PipeGuard AI's data quality reasoning engine. Return valid JSON diagnosis based strictly on evidence."


class GemmaClient:
    """Gemma Open-Weight AI client wrapper."""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or settings.gemma_api_key
        self.model_name = model_name or os.getenv("GEMMA_MODEL") or settings.gemma_model_name
        self.client = None

        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize google.genai client: {e}")

    def generate_diagnosis(self, context: Dict[str, Any]) -> DiagnosisResult:
        """
        Sends structured evidence context to Gemma and returns a validated DiagnosisResult.
        """
        if not self.api_key or not self.client:
            logger.info("GEMINI_API_KEY not configured. Falling back to deterministic analysis.")
            return self._generate_fallback_diagnosis(context, "GEMINI_API_KEY is not configured. Running in deterministic mode.")

        system_prompt = load_system_prompt()
        prompt_content = f"{system_prompt}\n\nEVIDENCE CONTEXT:\n{json.dumps(context, indent=2)}"

        candidate_models = [self.model_name, "gemini-2.0-flash", "gemini-1.5-flash", "gemma-2-9b-it"]
        last_exception = None

        for model in candidate_models:
            if not model:
                continue
            try:
                from google.genai import types
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt_content,
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                        top_p=0.95,
                        response_mime_type="application/json"
                    )
                )

                raw_text = response.text.strip()
                if raw_text.startswith("```json"):
                    raw_text = raw_text[7:]
                if raw_text.startswith("```"):
                    raw_text = raw_text[3:]
                if raw_text.endswith("```"):
                    raw_text = raw_text[:-3]
                raw_text = raw_text.strip()

                parsed_json = json.loads(raw_text)
                return DiagnosisResult.model_validate(parsed_json)

            except Exception as e:
                last_exception = e
                logger.warning(f"Model '{model}' failed: {e}. Trying fallback model...")

        logger.error(f"All AI model generations failed: {last_exception}")
        return self._generate_fallback_diagnosis(context, f"AI model error: {str(last_exception)}")

    def _generate_fallback_diagnosis(self, context: Dict[str, Any], note: str) -> DiagnosisResult:
        """Deterministic fallback when live Gemma API is not available."""
        dq_summary = context.get("dq_summary", {})
        failures = dq_summary.get("failures", [])
        datasets = context.get("datasets", [])

        affected_entities = [d["name"] for d in datasets]
        affected_cols = []
        evidences = []
        impacts = []
        remediations = []
        rules = []

        if failures:
            sev = Severity.HIGH
            root_cause = f"Detected {len(failures)} data quality rule failures across datasets ({note})."
            for f in failures:
                rule_id = f.get("rule_id", "DQ-UNK")
                failed_cnt = f.get("failed_rows", 0)
                details = f.get("details", "")
                evidences.append(
                    Evidence(
                        source="dq_result",
                        reference=rule_id,
                        observation=f"{failed_cnt} records failed check ({details})"
                    )
                )
                remediations.append(
                    RemediationItem(
                        action=f"Inspect and quarantine records violating rule {rule_id}.",
                        priority=Severity.HIGH
                    )
                )
                rules.append(
                    QualityRuleSuggestion(
                        name=f"auto_{rule_id.lower()}",
                        type=RuleType.NOT_NULL,
                        column="affected_column",
                        severity=Severity.HIGH
                    )
                )
            impacts.append(
                ImpactItem(
                    asset="downstream_pipeline",
                    severity=Severity.HIGH,
                    reason="Data quality failures may propagate inaccurate values to downstream tables."
                )
            )
        else:
            sev = Severity.LOW
            root_cause = f"No critical data quality violations detected ({note})."
            evidences.append(
                Evidence(
                    source="profiler",
                    reference="dataset_profile",
                    observation=f"All {dq_summary.get('passed_rules_count', 0)} quality rules passed cleanly."
                )
            )

        return DiagnosisResult(
            severity=sev,
            root_cause=root_cause,
            affected_entities=affected_entities,
            affected_columns=affected_cols,
            evidence=evidences,
            impact=impacts,
            remediation=remediations,
            quality_rules=rules,
        )
