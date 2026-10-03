import pandas as pd
from app.quality import DQEngine
from app.core.contracts import DQRule, RuleType, DQStatus, Severity


def test_not_null_rule():
    df = pd.DataFrame({
        "id": [1, 2, None],
        "val": ["a", "b", "c"]
    })
    engine = DQEngine({"test": df})
    rule = DQRule(rule_id="R1", column="id", type=RuleType.NOT_NULL)
    res = engine.execute_rule(rule)

    assert res.status == DQStatus.FAIL
    assert res.failed_rows == 1


def test_reconciliation_rule():
    df1 = pd.DataFrame({"order_id": [1, 2], "payment": [100.0, 200.0]})
    df2 = pd.DataFrame({"order_id": [1, 2], "order_amt": [100.0, 250.0]})

    engine = DQEngine({"pmt": df1, "ord": df2})
    rule = DQRule(
        rule_id="REC1",
        column="payment",
        type=RuleType.RECONCILIATION,
        params={
            "dataset": "pmt",
            "target_dataset": "ord",
            "join_column": "order_id",
            "value_column_1": "payment",
            "value_column_2": "order_amt"
        }
    )
    res = engine.execute_rule(rule)

    assert res.status == DQStatus.FAIL
    assert res.failed_rows == 1
