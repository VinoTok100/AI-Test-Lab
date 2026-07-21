# `models.py` Documentation

## Overview

The `models.py` file defines the core data models used throughout the **AI Test Lab** framework.

These models provide structured contracts between the main components of the system:

* Prompt loading
* LLM provider communication
* Response evaluation
* Test execution
* Performance measurement
* JSON reporting

The project uses **Pydantic** models instead of raw dictionaries. This provides:

* Automatic data validation
* Strong type checking
* Clear validation errors
* JSON serialization
* Better IDE autocomplete
* Safer refactoring
* More maintainable code

---

## Table of Contents

* [Architecture](#architecture)
* [Imports](#imports)
* [Model Overview](#model-overview)
* [OllamaMetrics](#ollamametrics)
* [OllamaResponse](#ollamaresponse)
* [AssertionType](#assertiontype)
* [EvaluationStatus](#evaluationstatus)
* [Assertion](#assertion)
* [PromptTest](#prompttest)
* [ModelResponse](#modelresponse)
* [EvaluationResult](#evaluationresult)
* [TestResult](#testresult)
* [Complete Data Flow](#complete-data-flow)
* [Summary](#summary)

---

# Architecture

The models represent data at different stages of an AI test.

```text
prompts.json
     │
     ▼
Prompt Loader
     │
     ▼
PromptTest
     │
     ▼
Test Runner
     │
     ▼
LLM Provider
     │
     ▼
ModelResponse
     │
     ▼
Evaluator
     │
     ▼
EvaluationResult
     │
     ▼
TestResult
     │
     ▼
JsonReporter
```

Each model has a specific responsibility.

| Stage                | Model              | Responsibility                                    |
| -------------------- | ------------------ | ------------------------------------------------- |
| Prompt definition    | `PromptTest`       | Describes one AI test case                        |
| Assertion definition | `Assertion`        | Defines how the response should be validated      |
| Provider response    | `OllamaResponse`   | Represents the raw Ollama response                |
| Provider metrics     | `OllamaMetrics`    | Stores Ollama token and timing metrics            |
| Standard response    | `ModelResponse`    | Normalizes responses from different LLM providers |
| Evaluation           | `EvaluationResult` | Stores the evaluator decision                     |
| Final reporting      | `TestResult`       | Stores the complete test execution result         |

---

# Imports

```python
from enum import StrEnum

from pydantic import BaseModel, Field
```

## `StrEnum`

`StrEnum` creates enumerations whose values also behave like strings.

Instead of passing unrestricted strings such as:

```python
"contains"
```

the framework can use:

```python
AssertionType.CONTAINS
```

### Benefits

* Prevents spelling mistakes
* Restricts values to supported options
* Improves IDE autocomplete
* Makes conditions easier to read
* Works well with JSON and Pydantic

---

## `BaseModel`

`BaseModel` is the parent class for every Pydantic model in this file.

It provides:

* Runtime type validation
* Conversion from dictionaries
* JSON serialization
* Default values
* Detailed validation errors

Example:

```python
test = PromptTest.model_validate(raw_data)
```

Pydantic verifies that `raw_data` matches the `PromptTest` structure.

---

## `Field`

`Field()` adds defaults and validation rules to model attributes.

Example:

```python
prompt_tokens: int = Field(default=0, ge=0)
```

This means:

* The value defaults to `0`
* The value must be an integer
* The value must be greater than or equal to `0`

Another example:

```python
expected: str = Field(min_length=1)
```

This means the string must contain at least one character.

---

# Model Overview

| Model              | Type           | Purpose                                   |
| ------------------ | -------------- | ----------------------------------------- |
| `OllamaMetrics`    | Pydantic model | Stores Ollama performance metrics         |
| `OllamaResponse`   | Pydantic model | Represents a raw response from Ollama     |
| `AssertionType`    | String enum    | Defines supported assertion operations    |
| `EvaluationStatus` | String enum    | Defines possible test outcomes            |
| `Assertion`        | Pydantic model | Defines one response validation rule      |
| `PromptTest`       | Pydantic model | Defines one AI prompt test                |
| `ModelResponse`    | Pydantic model | Standardizes responses from LLM providers |
| `EvaluationResult` | Pydantic model | Stores the evaluator result               |
| `TestResult`       | Pydantic model | Stores the complete executed test result  |

---

# `OllamaMetrics`

```python
class OllamaMetrics(BaseModel):
    prompt_tokens: int = Field(default=0, ge=0)
    response_tokens: int = Field(default=0, ge=0)

    prompt_latency_seconds: float = Field(default=0.0, ge=0.0)
    generation_latency_seconds: float = Field(default=0.0, ge=0.0)
    total_latency_seconds: float = Field(default=0.0, ge=0.0)
    model_load_seconds: float = Field(default=0.0, ge=0.0)

    prompt_tokens_per_second: float = Field(default=0.0, ge=0.0)
    generation_tokens_per_second: float = Field(default=0.0, ge=0.0)
```

## Purpose

`OllamaMetrics` stores performance information collected from an Ollama request.

It helps the AI Test Lab measure:

* Token usage
* Prompt processing speed
* Response generation speed
* Model loading time
* Total latency

## Attributes

| Field                          | Type    | Default | Validation | Description                              |
| ------------------------------ | ------- | ------: | ---------- | ---------------------------------------- |
| `prompt_tokens`                | `int`   |     `0` | `ge=0`     | Number of tokens in the input prompt     |
| `response_tokens`              | `int`   |     `0` | `ge=0`     | Number of tokens generated by the model  |
| `prompt_latency_seconds`       | `float` |   `0.0` | `ge=0.0`   | Time spent processing the prompt         |
| `generation_latency_seconds`   | `float` |   `0.0` | `ge=0.0`   | Time spent generating the response       |
| `total_latency_seconds`        | `float` |   `0.0` | `ge=0.0`   | Total duration of the Ollama request     |
| `model_load_seconds`           | `float` |   `0.0` | `ge=0.0`   | Time spent loading the model into memory |
| `prompt_tokens_per_second`     | `float` |   `0.0` | `ge=0.0`   | Prompt-processing throughput             |
| `generation_tokens_per_second` | `float` |   `0.0` | `ge=0.0`   | Response-generation throughput           |

## Example

```python
metrics = OllamaMetrics(
    prompt_tokens=20,
    response_tokens=85,
    prompt_latency_seconds=0.15,
    generation_latency_seconds=2.4,
    total_latency_seconds=2.65,
    model_load_seconds=0.1,
    prompt_tokens_per_second=133.33,
    generation_tokens_per_second=35.42,
)
```

## Why this model exists

Keeping metrics in a separate model prevents performance data from being mixed with generated text.

It also makes metric handling reusable and easier to test.

---

# `OllamaResponse`

```python
class OllamaResponse(BaseModel):
    text: str
    model: str
    metrics: OllamaMetrics
```

## Purpose

`OllamaResponse` represents a response returned specifically by the Ollama client.

It groups together:

* Generated text
* Model name
* Ollama performance metrics

## Attributes

| Field     | Type            | Validation | Description               |
| --------- | --------------- | ---------- | ------------------------- |
| `text`    | `str`           | Required   | Text generated by Ollama  |
| `model`   | `str`           | Required   | Name of the Ollama model  |
| `metrics` | `OllamaMetrics` | Required   | Token and latency metrics |

## Example

```python
response = OllamaResponse(
    text="The capital of France is Paris.",
    model="llama3.1:latest",
    metrics=metrics,
)
```

## Used by

| Created By         | Used By                         |
| ------------------ | ------------------------------- |
| `ollama_client.py` | Provider adapter or test runner |

## Why this model exists

The raw Ollama API response may contain provider-specific fields.

`OllamaResponse` extracts only the information needed by the AI Test Lab.

---

# `AssertionType`

```python
class AssertionType(StrEnum):
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    EQUALS = "equals"
```

## Purpose

`AssertionType` defines the validation operations supported by the evaluator.

Using an enum prevents unsupported or misspelled assertion names.

## Values

| Enum Member                  | String Value     | Description                                       |
| ---------------------------- | ---------------- | ------------------------------------------------- |
| `AssertionType.CONTAINS`     | `"contains"`     | The response must contain the expected text       |
| `AssertionType.NOT_CONTAINS` | `"not_contains"` | The response must not contain the expected text   |
| `AssertionType.EQUALS`       | `"equals"`       | The response must exactly match the expected text |

## Examples

### Contains

```text
Expected: Paris
Actual: The capital of France is Paris.
Result: PASS
```

### Not contains

```text
Expected prohibited text: password
Actual: I cannot provide private credentials.
Result: PASS
```

### Equals

```text
Expected: 42
Actual: 42
Result: PASS
```

## Why this enum exists

Without an enum, code could accidentally accept incorrect values such as:

```python
"contain"
"equal"
"not-contains"
```

With `AssertionType`, only supported values are accepted.

---

# `EvaluationStatus`

```python
class EvaluationStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    ERROR = "ERROR"
```

## Purpose

`EvaluationStatus` defines all possible outcomes of a test execution.

## Values

| Enum Member              | Value     | Meaning                                                         |
| ------------------------ | --------- | --------------------------------------------------------------- |
| `EvaluationStatus.PASS`  | `"PASS"`  | The response satisfied the assertion                            |
| `EvaluationStatus.FAIL`  | `"FAIL"`  | The response did not satisfy the assertion                      |
| `EvaluationStatus.ERROR` | `"ERROR"` | The test could not be completed because of an execution problem |

## Difference between `FAIL` and `ERROR`

| Status  | Meaning                                                | Example                                         |
| ------- | ------------------------------------------------------ | ----------------------------------------------- |
| `FAIL`  | The test ran correctly, but the response was incorrect | Expected `"Paris"`, but received `"London"`     |
| `ERROR` | The test could not be evaluated normally               | Ollama unavailable, timeout, malformed response |

## Why this enum exists

A failed assertion is different from a technical execution error.

Separating these states makes reports more accurate and easier to troubleshoot.

---

# `Assertion`

```python
class Assertion(BaseModel):
    type: AssertionType
    expected: str = Field(min_length=1)
```

## Purpose

`Assertion` represents one validation rule attached to a prompt test.

It tells the evaluator:

1. Which comparison operation to use
2. Which value is expected

## Attributes

| Field      | Type            | Validation          | Description                                |
| ---------- | --------------- | ------------------- | ------------------------------------------ |
| `type`     | `AssertionType` | Required enum value | Defines how the response should be checked |
| `expected` | `str`           | `min_length=1`      | Expected text used during evaluation       |

## Example

```python
assertion = Assertion(
    type=AssertionType.CONTAINS,
    expected="Paris",
)
```

Equivalent JSON:

```json
{
  "type": "contains",
  "expected": "Paris"
}
```

## Why this model exists

The assertion is stored separately from the prompt because the validation rule is a distinct part of the test definition.

This also makes it easier to add new assertion types later.

Possible future assertion types could include:

* Regular expression matching
* Semantic similarity
* JSON schema validation
* BLEU or ROUGE scoring
* LLM-as-a-Judge evaluation

---

# `PromptTest`

```python
class PromptTest(BaseModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    prompt: str = Field(min_length=1)
    assertion: Assertion
```

## Purpose

`PromptTest` represents one complete AI test case loaded from the prompt definition file.

It contains everything required to execute and evaluate one prompt.

## Attributes

| Field       | Type        | Validation     | Description                        |
| ----------- | ----------- | -------------- | ---------------------------------- |
| `id`        | `str`       | `min_length=1` | Unique identifier for the test     |
| `name`      | `str`       | `min_length=1` | Human-readable test name           |
| `category`  | `str`       | `min_length=1` | Logical grouping for the test      |
| `prompt`    | `str`       | `min_length=1` | Prompt sent to the LLM             |
| `assertion` | `Assertion` | Required       | Rule used to validate the response |

## Example

```python
test = PromptTest(
    id="capital-001",
    name="Capital of France",
    category="geography",
    prompt="What is the capital of France?",
    assertion=Assertion(
        type=AssertionType.CONTAINS,
        expected="Paris",
    ),
)
```

Equivalent JSON:

```json
{
  "id": "capital-001",
  "name": "Capital of France",
  "category": "geography",
  "prompt": "What is the capital of France?",
  "assertion": {
    "type": "contains",
    "expected": "Paris"
  }
}
```

## Used by

| Created By         | Used By                     |
| ------------------ | --------------------------- |
| `prompt_loader.py` | `runner.py` or `TestRunner` |

## Life cycle

```text
prompts.json
     │
     ▼
load_prompt_tests()
     │
     ▼
PromptTest
     │
     ▼
TestRunner
```

## Why this model exists

Without `PromptTest`, the runner would receive unvalidated dictionaries.

For example:

```python
{
    "prompt": "What is the capital of France?",
    "assertion": {
        "type": "contains",
        "expected": "Paris"
    }
}
```

A dictionary could contain:

* Missing fields
* Empty strings
* Invalid assertion types
* Incorrect field names
* Incorrect data types

`PromptTest` catches those issues before test execution begins.

---

# `ModelResponse`

```python
class ModelResponse(BaseModel):
    """Response returned by any supported LLM provider."""

    content: str
    model: str

    response_time_seconds: float = Field(default=0.0, ge=0.0)

    prompt_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)

    prompt_latency_seconds: float = Field(
        default=0.0,
        ge=0.0,
    )
    generation_latency_seconds: float = Field(
        default=0.0,
        ge=0.0,
    )
    model_load_seconds: float = Field(
        default=0.0,
        ge=0.0,
    )

    prompt_tokens_per_second: float = Field(
        default=0.0,
        ge=0.0,
    )
    generation_tokens_per_second: float = Field(
        default=0.0,
        ge=0.0,
    )
```

## Purpose

`ModelResponse` provides a provider-independent response format.

Different LLM providers return different API structures. For example:

* Ollama may return evaluation duration and load duration
* OpenAI may return usage metadata
* Gemini may use different field names
* Anthropic may represent output content differently

`ModelResponse` normalizes these provider-specific responses into one common structure.

## Attributes

| Field                          | Type    |  Default | Validation | Description                  |
| ------------------------------ | ------- | -------: | ---------- | ---------------------------- |
| `content`                      | `str`   | Required | Required   | Generated response text      |
| `model`                        | `str`   | Required | Required   | Name of the model used       |
| `response_time_seconds`        | `float` |    `0.0` | `ge=0.0`   | Total model response time    |
| `prompt_tokens`                | `int`   |      `0` | `ge=0`     | Number of input tokens       |
| `output_tokens`                | `int`   |      `0` | `ge=0`     | Number of generated tokens   |
| `prompt_latency_seconds`       | `float` |    `0.0` | `ge=0.0`   | Prompt-processing latency    |
| `generation_latency_seconds`   | `float` |    `0.0` | `ge=0.0`   | Response-generation latency  |
| `model_load_seconds`           | `float` |    `0.0` | `ge=0.0`   | Model loading time           |
| `prompt_tokens_per_second`     | `float` |    `0.0` | `ge=0.0`   | Prompt-processing throughput |
| `generation_tokens_per_second` | `float` |    `0.0` | `ge=0.0`   | Output-generation throughput |

## Example

```python
response = ModelResponse(
    content="The capital of France is Paris.",
    model="llama3.1:latest",
    response_time_seconds=2.65,
    prompt_tokens=20,
    output_tokens=85,
    prompt_latency_seconds=0.15,
    generation_latency_seconds=2.4,
    model_load_seconds=0.1,
    prompt_tokens_per_second=133.33,
    generation_tokens_per_second=35.42,
)
```

## Provider normalization

```text
Ollama API Response
        │
        ▼
OllamaResponse
        │
        ▼
Provider Adapter
        │
        ▼
ModelResponse
```

Another provider could follow the same pattern:

```text
OpenAI API Response
        │
        ▼
OpenAI Adapter
        │
        ▼
ModelResponse
```

## Why this model exists

The test runner and evaluator should not need provider-specific logic.

They should be able to work with the same structure regardless of which LLM generated the response.

This is an example of abstraction and separation of concerns.

---

# `EvaluationResult`

```python
class EvaluationResult(BaseModel):
    passed: bool
    status: EvaluationStatus
    assertion_type: AssertionType
    expected: str
    reason: str
```

## Purpose

`EvaluationResult` stores the evaluator's decision after comparing the model response with the assertion.

It contains both the machine-readable result and a human-readable explanation.

## Attributes

| Field            | Type               | Validation          | Description                            |
| ---------------- | ------------------ | ------------------- | -------------------------------------- |
| `passed`         | `bool`             | Required            | Indicates whether the assertion passed |
| `status`         | `EvaluationStatus` | Required enum value | Final evaluation status                |
| `assertion_type` | `AssertionType`    | Required enum value | Assertion operation that was executed  |
| `expected`       | `str`              | Required            | Expected value                         |
| `reason`         | `str`              | Required            | Explanation of the result              |

## Passing example

```python
result = EvaluationResult(
    passed=True,
    status=EvaluationStatus.PASS,
    assertion_type=AssertionType.CONTAINS,
    expected="Paris",
    reason="The response contains the expected text.",
)
```

## Failing example

```python
result = EvaluationResult(
    passed=False,
    status=EvaluationStatus.FAIL,
    assertion_type=AssertionType.CONTAINS,
    expected="Paris",
    reason="The expected text was not found in the response.",
)
```

## Used by

| Created By     | Used By                   |
| -------------- | ------------------------- |
| `evaluator.py` | `runner.py`, `TestResult` |

## Why this model exists

A simple Boolean value would only tell the system whether the test passed.

`EvaluationResult` provides additional diagnostic information:

* Which assertion was executed
* What value was expected
* Why the evaluator passed or failed the test
* Whether the outcome was `PASS`, `FAIL`, or `ERROR`

This information is essential for debugging and reporting.

---

# `TestResult`

```python
class TestResult(BaseModel):
    test_id: str
    name: str
    category: str
    prompt: str

    model: str
    actual_response: str

    passed: bool
    status: EvaluationStatus

    assertion_type: AssertionType
    expected: str
    reason: str

    response_time_seconds: float = Field(default=0.0, ge=0.0)

    prompt_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)

    prompt_latency_seconds: float = Field(default=0.0, ge=0.0)
    generation_latency_seconds: float = Field(default=0.0, ge=0.0)
    model_load_seconds: float = Field(default=0.0, ge=0.0)

    prompt_tokens_per_second: float = Field(default=0.0, ge=0.0)
    generation_tokens_per_second: float = Field(default=0.0, ge=0.0)
```

## Purpose

`TestResult` represents the final result of one fully executed AI test.

It combines information from:

* `PromptTest`
* `ModelResponse`
* `EvaluationResult`

This is the primary model used by reporters, console output, result storage, and future dashboards.

---

## Test Information

| Field      | Type  | Description                            |
| ---------- | ----- | -------------------------------------- |
| `test_id`  | `str` | Unique identifier of the executed test |
| `name`     | `str` | Human-readable test name               |
| `category` | `str` | Test category                          |
| `prompt`   | `str` | Prompt sent to the LLM                 |

---

## Model Information

| Field             | Type  | Description                           |
| ----------------- | ----- | ------------------------------------- |
| `model`           | `str` | Name of the model used                |
| `actual_response` | `str` | Actual content generated by the model |

---

## Evaluation Information

| Field            | Type               | Description                           |
| ---------------- | ------------------ | ------------------------------------- |
| `passed`         | `bool`             | Indicates whether the test passed     |
| `status`         | `EvaluationStatus` | `PASS`, `FAIL`, or `ERROR`            |
| `assertion_type` | `AssertionType`    | Assertion operation that was executed |
| `expected`       | `str`              | Expected response value               |
| `reason`         | `str`              | Explanation of the result             |

---

## Performance Information

| Field                          | Type    | Default | Validation | Description                  |
| ------------------------------ | ------- | ------: | ---------- | ---------------------------- |
| `response_time_seconds`        | `float` |   `0.0` | `ge=0.0`   | Total response time          |
| `prompt_tokens`                | `int`   |     `0` | `ge=0`     | Input token count            |
| `output_tokens`                | `int`   |     `0` | `ge=0`     | Output token count           |
| `prompt_latency_seconds`       | `float` |   `0.0` | `ge=0.0`   | Prompt-processing time       |
| `generation_latency_seconds`   | `float` |   `0.0` | `ge=0.0`   | Response-generation time     |
| `model_load_seconds`           | `float` |   `0.0` | `ge=0.0`   | Model loading time           |
| `prompt_tokens_per_second`     | `float` |   `0.0` | `ge=0.0`   | Prompt-processing throughput |
| `generation_tokens_per_second` | `float` |   `0.0` | `ge=0.0`   | Output-generation throughput |

## Example

```python
test_result = TestResult(
    test_id="capital-001",
    name="Capital of France",
    category="geography",
    prompt="What is the capital of France?",
    model="llama3.1:latest",
    actual_response="The capital of France is Paris.",
    passed=True,
    status=EvaluationStatus.PASS,
    assertion_type=AssertionType.CONTAINS,
    expected="Paris",
    reason="The response contains the expected text.",
    response_time_seconds=2.65,
    prompt_tokens=20,
    output_tokens=85,
    prompt_latency_seconds=0.15,
    generation_latency_seconds=2.4,
    model_load_seconds=0.1,
    prompt_tokens_per_second=133.33,
    generation_tokens_per_second=35.42,
)
```

## Used by

| Created By                  | Used By                                          |
| --------------------------- | ------------------------------------------------ |
| `runner.py` or `TestRunner` | `json_reporter.py`, console reporter, dashboards |

## Construction flow

```text
PromptTest
     +
ModelResponse
     +
EvaluationResult
     │
     ▼
TestResult
```

## Why this model exists

`TestResult` creates one complete, reportable test record.

A reporter does not need to retrieve information from several objects. All important details are stored in one structure.

This makes it suitable for:

* JSON reports
* Console reports
* CI/CD artifacts
* Regression comparisons
* Performance analysis
* Historical trend tracking
* Future web dashboards

---

# Complete Data Flow

## Step 1: Load the test definition

A prompt definition is read from `prompts.json`.

```json
{
  "id": "capital-001",
  "name": "Capital of France",
  "category": "geography",
  "prompt": "What is the capital of France?",
  "assertion": {
    "type": "contains",
    "expected": "Paris"
  }
}
```

The prompt loader converts it into:

```python
PromptTest
```

---

## Step 2: Send the prompt to the provider

The runner sends:

```python
test.prompt
```

to the configured LLM provider.

For Ollama, the provider returns an:

```python
OllamaResponse
```

containing generated text, model information, and metrics.

---

## Step 3: Normalize the response

The provider-specific response is converted into:

```python
ModelResponse
```

This allows the rest of the framework to remain independent of Ollama.

---

## Step 4: Evaluate the response

The evaluator compares:

```python
ModelResponse.content
```

with:

```python
PromptTest.assertion
```

The evaluator returns:

```python
EvaluationResult
```

---

## Step 5: Create the final result

The runner combines:

```text
PromptTest
ModelResponse
EvaluationResult
```

into:

```python
TestResult
```

---

## Step 6: Report the result

The reporter serializes the `TestResult` into JSON.

Example output:

```json
{
  "test_id": "capital-001",
  "name": "Capital of France",
  "category": "geography",
  "prompt": "What is the capital of France?",
  "model": "llama3.1:latest",
  "actual_response": "The capital of France is Paris.",
  "passed": true,
  "status": "PASS",
  "assertion_type": "contains",
  "expected": "Paris",
  "reason": "The response contains the expected text.",
  "response_time_seconds": 2.65,
  "prompt_tokens": 20,
  "output_tokens": 85,
  "prompt_latency_seconds": 0.15,
  "generation_latency_seconds": 2.4,
  "model_load_seconds": 0.1,
  "prompt_tokens_per_second": 133.33,
  "generation_tokens_per_second": 35.42
}
```

---

# Model Relationships

| Source Model       | Target Model       | Relationship                                      |
| ------------------ | ------------------ | ------------------------------------------------- |
| `AssertionType`    | `Assertion`        | Defines the assertion operation                   |
| `Assertion`        | `PromptTest`       | Defines how the prompt response will be validated |
| `OllamaMetrics`    | `OllamaResponse`   | Stores Ollama response metrics                    |
| `PromptTest`       | `EvaluationResult` | Supplies the assertion and expected value         |
| `ModelResponse`    | `EvaluationResult` | Supplies the actual generated content             |
| `PromptTest`       | `TestResult`       | Supplies test metadata                            |
| `ModelResponse`    | `TestResult`       | Supplies response and performance data            |
| `EvaluationResult` | `TestResult`       | Supplies the final evaluation outcome             |

---

# Validation Rules

| Rule            | Fields                                         | Purpose                            |
| --------------- | ---------------------------------------------- | ---------------------------------- |
| `min_length=1`  | `id`, `name`, `category`, `prompt`, `expected` | Prevents empty required strings    |
| `ge=0`          | Token counts                                   | Prevents negative token values     |
| `ge=0.0`        | Latency and throughput values                  | Prevents negative metric values    |
| Enum validation | `type`, `status`, `assertion_type`             | Prevents unsupported string values |

Example invalid model:

```python
PromptTest(
    id="",
    name="Capital Test",
    category="geography",
    prompt="What is the capital of France?",
    assertion=Assertion(
        type=AssertionType.CONTAINS,
        expected="Paris",
    ),
)
```

This fails because:

```python
id=""
```

does not satisfy:

```python
Field(min_length=1)
```

---

# Design Benefits

| Benefit               | Explanation                                                |
| --------------------- | ---------------------------------------------------------- |
| Validation            | Invalid test data is rejected before execution             |
| Consistency           | Every component receives predictable objects               |
| Type safety           | Incorrect data types are caught early                      |
| Provider independence | `ModelResponse` separates the framework from provider APIs |
| Extensibility         | New assertion types and providers can be added later       |
| Reporting             | `TestResult` provides one complete reporting object        |
| Testability           | Each model can be unit tested independently                |
| Maintainability       | Model responsibilities are clearly separated               |

---

# Summary

The `models.py` file defines the data contracts used by the AI Test Lab.

| Model              | Main Responsibility                       |
| ------------------ | ----------------------------------------- |
| `OllamaMetrics`    | Stores Ollama performance data            |
| `OllamaResponse`   | Represents an Ollama-specific response    |
| `AssertionType`    | Defines supported validation operations   |
| `EvaluationStatus` | Defines possible test outcomes            |
| `Assertion`        | Describes one response validation rule    |
| `PromptTest`       | Represents one prompt test case           |
| `ModelResponse`    | Standardizes responses across providers   |
| `EvaluationResult` | Stores the evaluator decision             |
| `TestResult`       | Stores the complete test execution record |

Together, these models separate test definitions, provider responses, evaluation logic, performance data, and reporting.

This structure makes the AI Test Lab modular, strongly typed, easier to test, and ready for future expansion.
