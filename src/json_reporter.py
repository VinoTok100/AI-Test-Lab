import json
from pathlib import Path

from src.models import EvaluationStatus, TestResult


class JsonReporter:
    """Writes AI test results to a JSON report file."""

    def __init__(self, report_path: Path) -> None:
        self.report_path = report_path

    def write(self, results: list[TestResult]) -> None:
        self.report_path.parent.mkdir(parents=True, exist_ok=True)

        report = {
            "summary": {
                "passed": sum(r.status == EvaluationStatus.PASS for r in results),
                "failed": sum(r.status == EvaluationStatus.FAIL for r in results),
                "errors": sum(r.status == EvaluationStatus.ERROR for r in results),
                "total": len(results),
            },
            "results": [r.model_dump(mode="json") for r in results],
        }

        self.report_path.write_text(
            json.dumps(report, indent=2),
            encoding="utf-8",
        )
