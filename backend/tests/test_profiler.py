import pandas as pd
from app.profiling import profile_dataset, detect_schema, detect_candidate_keys


def test_profiler_statistics():
    df = pd.DataFrame({
        "id": [1, 2, 3, 4],
        "name": ["Alice", "Bob", None, "Dave"],
        "amount": [10.0, 20.0, 30.0, 40.0]
    })
    prof = profile_dataset(df, "test_df")

    assert prof.row_count == 4
    assert prof.column_count == 3
    assert prof.columns["name"].null_count == 1
    assert prof.columns["amount"].min_value == 10.0
    assert prof.columns["amount"].max_value == 40.0
    assert prof.columns["amount"].mean == 25.0


def test_candidate_keys():
    df = pd.DataFrame({
        "order_id": ["ORD-1", "ORD-2", "ORD-3"],
        "status": ["PAID", "PAID", "PENDING"]
    })
    prof = profile_dataset(df, "orders")
    keys = detect_candidate_keys(prof)

    assert "order_id" in keys
    assert "status" not in keys
