from __future__ import annotations

import argparse
from src.prompt_loader import load_prompt_tests
from src.ollama_client import OllamaClient
from src.models import EvaluationStatus
from src.ollama_client import OllamaClient
from src.prompt_loader import load_prompt_tests
from src.runner import TestRunner
from src.evaluator import evaluate_response
#--------------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="AI Test Lab")

    parser.add_argument(
        "--model",
        default="llama3.1:latest",
        help="Ollama model name",
    )

    parser.add_argument(
        "--prompts",
        default="prompts/prompts.json",
        help="Path to prompt definition file",
    )

    return parser.parse_args()

#-------------------------------
def main() -> int:
    args = parse_args()

    tests = load_prompt_tests(args.prompts)

    client = OllamaClient(model=args.model)

    runner = TestRunner(client, evaluate_response)


    results = runner.run_tests(tests)

    passed = 0
    failed = 0
    errors = 0

    print("\n========== RESULTS ==========\n")

    for result in results:
        print(
            f"{result.test_id:<20}"
            f"{result.status.value:<8}"
            f"{result.reason}\n"
            f"{'':20}Response: {result.actual_response}"
        )

        if result.status == EvaluationStatus.PASS:
            passed += 1
        elif result.status == EvaluationStatus.FAIL:
            failed += 1
        else:
            errors += 1

    print("\n=============================")
    print(f"Passed : {passed}")
    print(f"Failed : {failed}")
    print(f"Errors : {errors}")
    print(f"Total  : {len(results)}")

    return 0 if failed == 0 and errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
