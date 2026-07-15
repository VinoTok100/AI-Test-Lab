import json

from src.json_reporter import JsonReporter
from src.models import (
    AssertionType,
    EvaluationStatus,
    TestResult as ResultModel,
)


def test_json_reporter_creates_report(tmp_path):
    results = [
        ResultModel(
            test_id="greeting-001",
            name="Basic greeting test",
            category="functional",
            prompt="Say hello.",
            model="llama3.1",
            actual_response="Hello!",
            passed=True,
            status=EvaluationStatus.PASS,
            assertion_type=AssertionType.CONTAINS,
            expected="Hello",
            reason="The response contains the expected text.",
            response_time_seconds=0.25,
        )
    ]

    report_path = tmp_path / "results.json"
    reporter = JsonReporter(report_path)

    reporter.write(results)

    assert report_path.exists()

    report_data = json.loads(
        report_path.read_text(encoding="utf-8")
    )

    assert report_data["summary"] == {
        "passed": 1,
        "failed": 0,
        "errors": 0,
        "total": 1,
    }

    result = report_data["results"][0]

    assert result["test_id"] == "greeting-001"
    assert result["status"] == "PASS"
    assert result["actual_response"] == "Hello!"
    assert result["passed"] is True