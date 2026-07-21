# `prompt_loader.py`

## Purpose

The `prompt_loader.py` module is responsible for loading AI prompt test definitions from a JSON file, validating them with **Pydantic**, and converting them into strongly typed `PromptTest` objects.

It acts as the **input layer** of the AI Test Lab. Instead of working directly with raw JSON dictionaries, the rest of the framework receives validated Python objects that are guaranteed to follow the expected schema.

Without this module, the AI Test Runner would have no reliable way to load or validate test cases before execution.

---

# Dependencies

```python
import json
from pathlib import Path

from src.models import PromptTest
```

| Module | Purpose |
|---------|----------|
| `json` | Reads JSON files and converts JSON text into Python objects. |
| `Path` | Provides a modern, object-oriented interface for working with files and directories. |
| `PromptTest` | Validates each JSON test case and converts it into a strongly typed Pydantic model. |

---

# Source Code

```python
import json
```

## Explanation

Imports Python's built-in **json** module.

The JSON module allows Python to exchange data using JavaScript Object Notation (JSON), one of the most common formats for configuration files and APIs.

In AI Test Lab, prompt definitions are stored in a JSON file. This module converts that JSON into Python objects.

### Why it is needed

Without the `json` module, Python would treat the file as plain text and could not interpret its structure.

---

```python
from pathlib import Path
```

## Explanation

Imports the `Path` class from Python's `pathlib` module.

`Path` provides an object-oriented approach to handling file system paths.

Instead of writing:

```python
open("prompts/prompts.json")
```

the code creates a `Path` object:

```python
Path("prompts/prompts.json")
```

which exposes many useful methods.

Common examples include:

- `exists()`
- `open()`
- `mkdir()`
- `parent`
- `suffix`

### Why it is used

Using `Path` makes the code:

- easier to read,
- cross-platform,
- less error-prone,
- more maintainable.

---

```python
from src.models import PromptTest
```

## Explanation

Imports the `PromptTest` Pydantic model.

Every JSON object describing a prompt test is converted into one instance of `PromptTest`.

Example JSON:

```json
{
    "id": "greeting-001",
    "prompt": "Say hello",
    "assertions": []
}
```

becomes

```python
PromptTest(...)
```

instead of remaining a plain Python dictionary.

### Why it is used

Using a Pydantic model provides:

- automatic validation,
- type safety,
- autocompletion,
- cleaner code,
- immediate detection of invalid test definitions.

---

```python
def load_prompt_tests(file_path: str | Path) -> list[PromptTest]:
```

# Function Overview

This function loads a JSON file containing prompt test definitions, validates every test case, and returns a list of `PromptTest` objects.

---

## Parameters

```python
file_path
```

Specifies the location of the JSON file.

The type hint

```python
str | Path
```

means the caller may provide either:

```python
"prompts/prompts.json"
```

or

```python
Path("prompts/prompts.json")
```

Both are accepted.

---

## Return Type

```python
list[PromptTest]
```

Returns a list of validated prompt test objects.

Example:

```python
[
    PromptTest(...),
    PromptTest(...),
    PromptTest(...)
]
```

---

```python
path = Path(file_path)
```

## Explanation

Converts the incoming argument into a `Path` object.

Even if the caller passes a string, the code immediately converts it into a `Path`.

Example:

Input:

```python
"prompts/prompts.json"
```

becomes

```python
Path("prompts/prompts.json")
```

### Why this is useful

From this point onward, the function can use all of `Path`'s methods regardless of how the caller supplied the file name.

---

```python
if not path.exists():
```

## Explanation

Checks whether the specified file exists.

If the file cannot be found, the condition evaluates to `True`.

Example:

```
prompts/prompts.json
```

Missing?

Then execution enters the `if` block.

### Why this check matters

Failing early produces a clear and meaningful error instead of allowing the program to fail later while attempting to open a nonexistent file.

---

```python
raise FileNotFoundError(
    f"Prompt file not found: {path}"
)
```

## Explanation

Raises a `FileNotFoundError`.

Example output:

```text
FileNotFoundError:
Prompt file not found:
prompts/prompts.json
```

### Why this is important

This immediately informs the user exactly what went wrong and which file is missing.

Without this explicit exception, debugging would be more difficult.

---

```python
with path.open("r", encoding="utf-8") as file:
```

## Explanation

Opens the JSON file for reading.

Breaking it down:

```python
"r"
```

means

> Open the file in read-only mode.

```python
encoding="utf-8"
```

specifies UTF-8 text encoding, the standard encoding used by JSON.

The `with` statement automatically closes the file after reading, even if an exception occurs.

Equivalent (but discouraged):

```python
file = open(...)

...

file.close()
```

### Why use `with`

Using a context manager prevents resource leaks and guarantees proper cleanup.

---

```python
raw_data = json.load(file)
```

## Explanation

Reads the entire JSON document and converts it into Python objects.

Example JSON:

```json
[
    {
        "id": "1",
        "prompt": "Hello"
    }
]
```

becomes

```python
[
    {
        "id": "1",
        "prompt": "Hello"
    }
]
```

At this point the elements are ordinary Python dictionaries.

### Why this step is necessary

Python cannot validate or manipulate JSON until it has first been converted into native Python objects.

---

```python
return [
    PromptTest.model_validate(item)
    for item in raw_data
]
```

## Explanation

This is a **list comprehension**.

The code iterates over every dictionary stored in `raw_data`.

For each dictionary:

```python
item
```

it executes

```python
PromptTest.model_validate(item)
```

`model_validate()` is a Pydantic method that:

- validates required fields,
- verifies data types,
- creates a `PromptTest` instance,
- raises a `ValidationError` if the data is invalid.

Example:

```python
{
    "id": "1",
    "prompt": "Hello"
}
```

becomes

```python
PromptTest(
    id="1",
    prompt="Hello"
)
```

### Why validation matters

This guarantees that every prompt entering the AI Test Runner follows the expected schema.

If even one prompt contains invalid data, the error is detected immediately rather than during test execution.

---

# Execution Flow

```text
JSON Prompt File
        │
        ▼
Convert to Path object
        │
        ▼
Does the file exist?
        │
   ┌────┴────┐
   │         │
 No         Yes
   │         │
   ▼         ▼
Raise      Open file
FileNotFoundError
             │
             ▼
        json.load()
             │
             ▼
    Python dictionaries
             │
             ▼
PromptTest.model_validate()
             │
             ▼
Validated PromptTest objects
             │
             ▼
Return list[PromptTest]
```

---

# How It Fits into AI Test Lab

```text
prompts.json
      │
      ▼
prompt_loader.py
      │
      ▼
PromptTest objects
      │
      ▼
TestRunner
      │
      ▼
OllamaClient
      │
      ▼
Evaluator
      │
      ▼
JsonReporter
```

The loader serves as the entry point for test definitions. It ensures that only valid prompt specifications continue through the AI testing pipeline.

---

# Key Takeaways

- `prompt_loader.py` is responsible for loading prompt definitions from disk.
- It accepts either a string path or a `Path` object.
- It verifies that the prompt file exists before attempting to read it.
- It parses JSON into Python dictionaries using the built-in `json` module.
- It validates each dictionary with the `PromptTest` Pydantic model.
- Invalid prompt definitions are rejected immediately through Pydantic validation.
- The module returns a list of strongly typed `PromptTest` objects, allowing the rest of the AI Test Lab to operate without handling raw JSON or performing additional validation.

---

# Summary

`prompt_loader.py` is the **data ingestion and validation layer** of the AI Test Lab. Its primary responsibility is to transform external JSON prompt definitions into validated `PromptTest` objects that the rest of the framework can safely consume. By separating file handling and validation from the execution logic, the module improves reliability, maintainability, and readability across the entire testing framework.