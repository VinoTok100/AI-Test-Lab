# prompt_loader.py – Line-by-Line Explanation

## Purpose of this file

`prompt_loader.py` is responsible for loading AI test cases from a JSON file, validating them using Pydantic, and returning them as a list of `PromptTest` objects.

Without this file, the AI Test Lab would have no way to read prompt definitions from disk before executing the tests.

---

## Source Code

```python
import json
```

### Explanation

Imports Python's built-in **json** module.

The `json` module is used to:

* Read JSON files.
* Convert JSON text into Python objects.
* Convert Python objects back into JSON.

In this file it is used to read the prompt definition file.

---

```python
from pathlib import Path
```

### Explanation

Imports the `Path` class from Python's **pathlib** module.

`Path` provides an object-oriented way to work with files and directories.

Instead of writing:

```python
open("prompts/prompts.json")
```

you can write:

```python
Path("prompts/prompts.json")
```

Benefits include:

* Works on Windows, Linux, and macOS.
* Easier to read.
* Provides many helpful methods such as:

  * `exists()`
  * `open()`
  * `mkdir()`
  * `parent`

---

```python
from src.models import PromptTest
```

### Explanation

Imports the **PromptTest** Pydantic model.

Each object in the JSON file will become one `PromptTest`.

Example JSON:

```json
{
    "id": "greeting-001",
    "prompt": "Say hello",
    "assertions": [...]
}
```

becomes

```python
PromptTest(...)
```

instead of a plain dictionary.

Using a model provides:

* type checking
* validation
* autocompletion
* safer code

---

```python
def load_prompt_tests(file_path: str | Path) -> list[PromptTest]:
```

### Explanation

Defines the function that loads prompt tests.

Function name:

```python
load_prompt_tests
```

Meaning:

> Load prompt tests from a file.

### Parameter

```python
file_path
```

The location of the JSON file.

The type hint

```python
str | Path
```

means the function accepts either:

```python
"prompts/prompts.json"
```

or

```python
Path("prompts/prompts.json")
```

### Return type

```python
list[PromptTest]
```

The function returns a list of `PromptTest` objects.

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

### Explanation

Converts the input into a `Path` object.

Even if the caller passes a string,

```python
"prompts/prompts.json"
```

it becomes

```python
Path("prompts/prompts.json")
```

Now the code can use all `Path` methods.

---

```python
if not path.exists():
```

### Explanation

Checks whether the file actually exists.

If the file does not exist:

```python
False
```

the program enters the `if` block.

Example:

```python
prompts/prompts.json
```

Missing?

Then this condition becomes true.

---

```python
raise FileNotFoundError(
    f"Prompt file not found: {path}"
)
```

### Explanation

Stops the program immediately by raising an exception.

Example output:

```
FileNotFoundError:
Prompt file not found:
prompts/prompts.json
```

This prevents confusing errors later when trying to open a file that does not exist.

---

```python
with path.open("r", encoding="utf-8") as file:
```

### Explanation

Opens the JSON file.

Breaking it down:

`"r"`

means:

> Open for reading.

`encoding="utf-8"`

tells Python how to decode the text.

UTF-8 supports virtually every language and is the standard encoding for JSON.

The `with` statement is important because it automatically closes the file when finished, even if an error occurs.

Equivalent (but not recommended):

```python
file = open(...)

...

file.close()
```

---

```python
raw_data = json.load(file)
```

### Explanation

Reads the entire JSON file and converts it into Python objects.

Suppose the JSON contains:

```json
[
  {
    "id":"1",
    "prompt":"Hello"
  }
]
```

After loading:

```python
raw_data
```

contains

```python
[
    {
        "id":"1",
        "prompt":"Hello"
    }
]
```

Notice these are still dictionaries, **not** `PromptTest` objects.

---

```python
return [
    PromptTest.model_validate(item)
    for item in raw_data
]
```

### Explanation

This is a **list comprehension**.

It loops through every dictionary in `raw_data`.

For each dictionary:

```python
item
```

it executes

```python
PromptTest.model_validate(item)
```

`model_validate()` is a Pydantic method that:

* checks every required field
* validates the data types
* creates a real `PromptTest` object
* raises a `ValidationError` if the data is invalid

For example:

```python
{
    "id":"1",
    "prompt":"Hello"
}
```

becomes

```python
PromptTest(
    id="1",
    prompt="Hello"
)
```

Finally, the function returns a list of validated `PromptTest` objects ready for the AI Test Runner.

---

# Execution Flow

```text
JSON file
      │
      ▼
Path(file_path)
      │
      ▼
Does file exist?
      │
      ├── No → FileNotFoundError
      │
      ▼ Yes
Open file
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
PromptTest objects
      │
      ▼
Return list[PromptTest]
```

# Summary

`prompt_loader.py` acts as the **data loading layer** of the AI Test Lab. Its responsibilities are to:

1. Receive the path to a prompt definition file.
2. Verify that the file exists.
3. Open the JSON file safely.
4. Parse the JSON into Python dictionaries.
5. Validate each dictionary with the `PromptTest` Pydantic model.
6. Return a list of validated `PromptTest` objects that the test runner can execute.

This separation of responsibilities keeps the rest of the framework simple: other modules can assume they always receive valid `PromptTest` objects instead of dealing with raw JSON.
