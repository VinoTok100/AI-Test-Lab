import json
from pathlib import Path

from src.models import TestResult, EvaluationStatus #TestStatus


class JsonReporter:
    """Writes AI test results to a JSON report file."""

    def __init__(self, report_path: Path) -> None:
        self.report_path = report_path

    def write(self, results: list[TestResult]) -> None:
        self.report_path.parent.mkdir(parents=True, exist_ok=True)

        report = {
            "summary": {
                "passed": self._count_status(results, EvaluationStatus.PASS),
                "failed": self._count_status(results, EvaluationStatus.FAIL),
                "errors": self._count_status(results, EvaluationStatus.ERROR),
                "total": len(results),
            },
            "results": [
                result.model_dump(mode="json")
                for result in results
            ],
        }

        self.report_path.write_text(
            json.dumps(report, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def _count_status(
        results: list[TestResult],
        status: EvaluationStatus,
    ) -> int:
        return sum(result.status == status for result in results)