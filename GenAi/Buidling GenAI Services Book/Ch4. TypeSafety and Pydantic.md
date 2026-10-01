---
tags: [genai, python, fastapi, pydantic, type-safety]
---

## Introduction to type safety

Types tell you what values a variable can hold and what operations you can run on it. Python's common built-in types are `int`, `float`, `str`, and `bool`.

> [!definition] Type safety
> The practice of making sure variables only ever hold values that match their declared types.

Python is dynamically typed. Types are checked only when the code runs, not beforehand, and you don't have to declare them because Python infers them from the values you assign.

> [!definition] Dynamic typing
> Type checks happen at runtime. A mismatch only shows up as an error when that line of code actually executes.

Adding types lets you catch errors much earlier. You enforce type constraints by fully typing your variables and functions:

![[Pasted image 20260929141426.png]]

A type checker then warns you about mismatches while you're still developing. That saves time, because you find problems early instead of chasing obscure runtime errors later. You can go one step further and run type checks automatically in your deployment pipeline, so breaking changes never reach production.

> [!warning] The trade-off
> Type safety feels like a burden at first. You have to type every function you write, which slows you down early in a project.
>
> Skipping types costs more later. If another developer changes a database table or an API schema your service depends on, nothing warns you, and the bug surfaces at runtime.

## Type annotations

> [!definition] Type annotation
> The syntax for declaring a type on a variable, parameter, or return value, e.g. `text: str` or `-> int`.

In Python applications, type annotations give you:

- Auto-complete support in your code editor
- Static type checks with tools like `mypy`

FastAPI also uses type hints to:

- Define handler requirements: path and query parameters, bodies, headers, dependencies, and so on
- Convert data when needed
- Validate data from incoming requests, databases, and external services
- Keep the OpenAPI specification (which powers the generated docs page) up to date automatically

### Example: a typed cost calculator

```python
# utils.py
from typing import Literal, TypeAlias

import tiktoken
from loguru import logger

SupportedModels: TypeAlias = Literal["gpt-3.5", "gpt-4"]
PriceTable: TypeAlias = dict[SupportedModels, float]

price_table: PriceTable = {
    "gpt-3.5": 0.002,
    "gpt-4": 0.06,
}


def count_tokens(text: str | None) -> int:
    if text is None:
        logger.warning("Response is None")
        return 0

    enc = tiktoken.encoding_for_model("gpt-3.5")
    return len(enc.encode(text))


def calculate_usage_costs(
    prompt: str,
    response: str | None,
    model: SupportedModels,
) -> tuple[float, float, float]:
    if model not in price_table:
        raise ValueError(
            f"Model {model} is not supported. "
            f"Supported models are: {list(price_table.keys())}"
        )

    price = price_table[model]
    req_costs = price * count_tokens(prompt) / 1000
    res_costs = price * count_tokens(response) / 1000
    total_costs = req_costs + res_costs

    return req_costs, res_costs, total_costs
```

> [!definition] TypeAlias
> Marks an assignment as a **type alias** (a new name for a type) instead of an ordinary variable. `PriceTable` above is a type you can annotate with, not a dictionary.

> [!definition] Literal
> Restricts a variable to a fixed set of exact values. `Literal["gpt-3.5", "gpt-4"]` accepts only those two strings.

### Annotated

The note's takeaway is to use `Annotated` instead of `TypeAlias`. `Annotated` still lets you reuse types, and it also lets you attach metadata to them.

> [!definition] Annotated
> `Annotated[BaseType, Metadata]` pairs a type with extra information. Type checkers ignore the metadata, but it documents the code, and libraries like Pydantic can read it to enforce rules at runtime.

> [!warning]
> `Annotated` needs at least two arguments: the type and at least one piece of metadata.

```python
from typing import Annotated, Literal

SupportedModels = Annotated[Literal["gpt-3.5", "gpt-4o"], "Supported models"]
PriceTable = Annotated[dict[SupportedModels, float], "Price per model"]

price: PriceTable = {
    "gpt-3.5": 0.00638,
    "gpt-4o": 0.000638,
}
```

---

## Dataclasses and Pydantic

When you need a custom data structure, a dataclass lets you organize, store, and pass data around the application. You group related data from different places into one structure and hand it to a function as a single item.

> [!definition] Dataclass
> A Python class decorated with `@dataclass` that generates `__init__`, `__repr__`, and similar methods for you. It removes boilerplate but does **no validation**.

> [!definition] Pydantic model
> A class that inherits from `BaseModel`. When you create one, Pydantic runs initialization hooks that add data validation, serialization, and JSON schema generation, none of which plain dataclasses have.

| Tool | What it gives you |
| --- | --- |
| `dataclass` | Less boilerplate, no validation |
| Pydantic `BaseModel` | Strict validation, serialization, JSON schema |

With Pydantic, `Annotated` becomes more than documentation. Pydantic reads the metadata and enforces it as a runtime constraint:

```python
Annotated[BaseType, Metadata]
```

> [!definition] default_factory
> Instead of a fixed default value, you pass a function. Pydantic calls it every time a new instance is created. The book uses this to give every response its own unique UUID string.

## Special constraint types

Pydantic ships ready-made types for common checks.

IP address:

```python
ip: Annotated[str, IPvAnyAddress] | None
```

Positive integers:

```python
ImageSize = Annotated[
    tuple[PositiveInt, PositiveInt],
    "Width and height of an image in pixels",
]
```

URL:

```python
url: Annotated[str, HttpUrl] | None = None
```

## Custom field and model validators

Custom validators let you write your own validation rules.

### Field validator with AfterValidator

```python
from typing import Annotated

from pydantic import AfterValidator, Field, PositiveInt

ImageSize = Annotated[
    tuple[PositiveInt, PositiveInt],
    Field(description="Width and height of an image in pixels"),
]


def validate_square_dimensions(value: tuple[int, int]) -> tuple[int, int]:
    width, height = value
    if width != height:
        raise ValueError("Only square images are supported (width must equal height)")
    if width not in {512, 1024}:
        raise ValueError(f"Invalid output size: {value} — expected (512, 512) or (1024, 1024)")
    return value


OutputSize = Annotated[ImageSize, AfterValidator(validate_square_dimensions)]
```

> [!definition] AfterValidator
> A validator that runs **after** Pydantic's own parser has confirmed the value matches the base type. Your function gets a value that's already the right type and only has to check your custom rule.

### Model validator

```python
from typing import Annotated

from pydantic import Field, model_validator


class ImageModelRequest(ModelRequest):
    model: SupportedModels
    output_size: OutputSize
    num_inference_steps: Annotated[int, Field(ge=1, le=2000, default=200)]

    # 3. Cross-field / Multi-field validator (Model-level)
    @model_validator(mode="after")
    def validate_model_inference_steps(self) -> "ImageModelRequest":
        if self.model == "tinysd" and self.num_inference_steps > 1000:
            raise ValueError("TinySD model cannot exceed 1000 inference steps")
        return self
```

> [!definition] model_validator
> A method on the model that validates the whole object at once. With `mode="after"`, it runs once every field has been parsed, so it can compare fields against each other.

### Which one to use

| | `AfterValidator` | `@model_validator` |
| --- | --- | --- |
| Scope | One field | The whole model |
| Where it lives | Inside `Annotated[...]` | A method on the `BaseModel` class |
| Can see other fields | No | Yes |
| When it runs | Right after that single field is parsed | After the model's fields are parsed (`mode="after"`) |

> [!tip] Rule of thumb
> - The rule looks at **one value** (is this a valid postal code? is this integer in my custom set?): use `AfterValidator`. You can then reuse it as a type alias.
> - The rule **compares field A with field B** (`start_date < end_date`, or "if `status == "FAILED"`, `error_code` is required"): use `@model_validator(mode="after")`.

## Computed fields

> [!definition] Computed field
> A value derived from other fields in the model at the moment you read it, instead of one you pass in.

Before this feature, you'd use Python's `@property` for a dynamic value. Pydantic ignores properties during serialization, so they don't appear in `model_dump()` or `model_dump_json()` output. `@computed_field` fixes that: it behaves like a normal property in your code, and Pydantic treats it as a real field.

```python
from typing import Annotated

from pydantic import Field, computed_field


class TextModelResponse(ModelResponse):
    model: SupportedModels
    price: Annotated[float, Field(ge=0, default=0.01)]
    temperature: Annotated[float, Field(ge=0.0, le=1.0, default=0.0)]

    @computed_field  # Note: @property is often combined or @computed_field handles it directly
    @property
    def tokens(self) -> int:
        return count_tokens(self.content)

    @computed_field
    @property
    def cost(self) -> float:
        return self.price * self.tokens
```

- `tokens` reads `self.content` and calls `count_tokens` to count the generated tokens.
- `cost` multiplies `self.price` by that token count.

In Python code, you access them like any ordinary property:

```python
response = TextModelResponse(
    content="Hello, how can I help you?",
    model="gpt-4o",
    price=0.002,
)

# Accessed via dot notation:
print(response.tokens)  # Output: 8
print(response.cost)    # Output: 0.016
```

## Exporting and serializing models

> [!definition] Serialization
> Converting an object into a format you can store or send, such as a Python `dict` or a JSON string.

### `.model_dump()`

Converts the model instance into a Python `dict`.

```python
from datetime import datetime

from pydantic import BaseModel, HttpUrl


class UserProfile(BaseModel):
    id: int
    name: str
    website: HttpUrl
    created_at: datetime


profile = UserProfile(
    id=1,
    name="Alice",
    website="https://example.com",
    created_at=datetime.now(),
)

data = profile.model_dump()
print(type(data))          # <class 'dict'>
print(data["created_at"])  # datetime.datetime(...) object (Python-native)
```

By default the dictionary holds native Python objects, like `datetime` and `UUID` instances. To get JSON-safe primitives instead (dates as ISO strings, for example), pass `mode="json"`:

```python
json_friendly_dict = profile.model_dump(mode="json")
print(json_friendly_dict["created_at"])  # "2026-09-29T16:52:00..." (string)
```

### `.model_dump_json()`

Converts the model instance straight into a JSON-encoded string.

```python
json_str = profile.model_dump_json(indent=2)
print(type(json_str))  # <class 'str'>
```

> [!note] Performance
> `.model_dump_json()` doesn't call `.model_dump()` and then `json.dumps()`. Pydantic's Rust core serializes directly to raw JSON, which the note puts at about 5x faster.

| Method | Returns | Values inside |
| --- | --- | --- |
| `model_dump()` | Python `dict` | Native Python objects (`datetime`, `UUID`, ...) |
| `model_dump(mode="json")` | Python `dict` | JSON-safe primitives (str, int, float, bool, list, dict, `None`) |
| `model_dump_json()` | `str` | Valid JSON text, ready to send over the wire |

%% related:start (auto-generated, regenerate with related_links.py) %%
## Related
- [[Pydantic]]
%% related:end %%
