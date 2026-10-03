from app.pipeline.log_parser import parse_pipeline_logs


def test_log_parser():
    raw_log = """
    [2026-10-03 10:00:00] [INFO] [pipeline] Pipeline started.
    [2026-10-03 10:01:00] [ERROR] [reconciler] 17 records failed payment reconciliation.
    """
    events = parse_pipeline_logs(raw_log)

    assert len(events) == 2
    assert events[1].log_level == "ERROR"
    assert "17 records failed" in events[1].message
