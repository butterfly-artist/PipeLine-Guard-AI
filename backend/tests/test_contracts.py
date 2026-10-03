from app.core.contracts import (
    DiagnosisResult,
    Evidence,
    ImpactItem,
    RemediationItem,
    QualityRuleSuggestion,
    Severity,
    RuleType,
    DQStatus,
    DQResult,
)


def test_diagnosis_result_contract():
    diagnosis = DiagnosisResult(
        severity=Severity.HIGH,
        root_cause="Mismatched payment totals across transactions.",
        affected_entities=["sample_payments.csv"],
        affected_columns=["payment_total"],
        evidence=[
            Evidence(
                source="dq_result",
                reference="DQ-PAY-001",
                observation="17 payment records failed reconciliation"
            )
        ],
        impact=[
            ImpactItem(
                asset="gold_revenue_dashboard",
                severity=Severity.HIGH,
                reason="Inconsistent transaction data propagates to revenue reporting."
            )
        ],
        remediation=[
            RemediationItem(
                action="Quarantine un-reconciled payment records.",
                priority=Severity.HIGH
            )
        ],
        quality_rules=[
            QualityRuleSuggestion(
                name="payment_reconciliation",
                type=RuleType.RECONCILIATION,
                column="payment_total",
                severity=Severity.HIGH
            )
        ]
    )

    assert diagnosis.severity == Severity.HIGH
    assert len(diagnosis.evidence) == 1
    assert diagnosis.evidence[0].reference == "DQ-PAY-001"
    assert diagnosis.quality_rules[0].type == RuleType.RECONCILIATION


def test_dq_result_contract():
    dq = DQResult(
        rule_id="DQ-001",
        status=DQStatus.FAIL,
        checked_rows=100,
        failed_rows=5,
        failure_rate=5.0
    )

    assert dq.status == DQStatus.FAIL
    assert dq.failure_rate == 5.0
