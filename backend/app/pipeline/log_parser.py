import re
from pathlib import Path
from typing import List, Union
from app.core.contracts import PipelineLogEvent

# Common log pattern: [TIMESTAMP] [LEVEL] [COMPONENT] Message...
LOG_PATTERN = re.compile(
    r"^(?:\[(?P<timestamp>[^\]]+)\]\s*)?(?:\[(?P<level>INFO|WARN|WARNING|ERROR|CRITICAL|FATAL)\]\s*)?(?:\[(?P<component>[^\]]+)\]\s*)?(?P<message>.*)$",
    re.IGNORECASE
)


def parse_pipeline_logs(log_source: Union[str, Path]) -> List[PipelineLogEvent]:
    """Parse log file path or raw log text string into PipelineLogEvent items."""
    lines: List[str] = []
    if isinstance(log_source, Path) or (isinstance(log_source, str) and (log_source.endswith(".log") or Path(log_source).exists())):
        p = Path(log_source)
        if p.exists():
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
    elif isinstance(log_source, str):
        lines = log_source.splitlines()

    events: List[PipelineLogEvent] = []
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue

        match = LOG_PATTERN.match(line_str)
        if match:
            gd = match.groupdict()
            level = (gd.get("level") or "INFO").upper()
            ts = gd.get("timestamp")
            comp = gd.get("component") or "pipeline"
            msg = gd.get("message") or line_str

            err_details = msg if level in ("ERROR", "CRITICAL", "FATAL") else None

            events.append(
                PipelineLogEvent(
                    timestamp=ts,
                    log_level=level,
                    component=comp,
                    message=msg,
                    error_details=err_details,
                )
            )
        else:
            events.append(
                PipelineLogEvent(
                    log_level="INFO",
                    component="pipeline",
                    message=line_str,
                )
            )

    return events
