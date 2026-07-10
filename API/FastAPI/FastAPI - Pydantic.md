# FastAPI and Pydantic 

This Obsidian Markdown file provides a structured overview of FastAPI and Pydantic concepts, focusing on model declarations, validations, and handling of request parameters like cookies and headers. It is designed for studying and quick reference.

---

## Table of Contents
- [Introduction](#introduction)
- [Pydantic Models](#pydantic-models)
  - [Field Validations and Metadata](#field-validations-and-metadata)
  - [BaseModel](#basemodel)
  - [Set Types](#set-types)
  - [Nested Models](#nested-models)
  - [Attributes with Lists of Submodels](#attributes-with-lists-of-submodels)
  - [Special Types and Validation](#special-types-and-validation)
  - [Adding Examples in Field](#adding-examples-in-field)
  - [Body with Examples](#body-with-examples)
  - [Body with Multiple Examples](#body-with-multiple-examples)
  - [OpenAPI Examples](#openapi-examples)
  - [Other Data Types](#other-data-types)
- [Cookie Parameters](#cookie-parameters)
  - [Cookie Parameter Models](#cookie-parameter-models)
  - [Forbid Extra Cookies](#forbid-extra-cookies)
- [Header Parameters](#header-parameters)
  - [Automatic Conversion](#automatic-conversion)
  - [Duplicate Headers](#duplicate-headers)
  - [Header Parameter Models](#header-parameter-models)
  - [Forbid Extra Headers](#forbid-extra-headers)
- [Comparison: Headers vs. Cookies](#comparison-headers-vs-cookies)

---

## Introduction
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. It integrates with **Pydantic** for data validation and serialization, providing automatic generation of OpenAPI documentation and robust type checking.

Pydantic is used to define data models with type annotations and validations, ensuring data integrity and simplifying request/response handling in FastAPI.

---

## Pydantic Models

### Field Validations and Metadata
Use Pydantic's `Field` to add validations and metadata to model attributes.

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None,
        title="The description of the item",
        max_length=300
    )
    price: float = Field(
        gt=0,
        description="The price must be greater than zero"
    )
    tax: float | None = Field(
        default=None,
        title="The tax of the item"
    )
```

- **Key Features**:
  - `default`: Set default value (e.g., `None`).
  - `title`: Descriptive title for OpenAPI documentation.
  - `max_length`: Restrict string length.
  - `gt`: Ensure value is greater than a specified number (e.g., `price > 0`).
  - `description`: Add metadata for documentation.

---

### BaseModel
Pydantic's `BaseModel` is the foundation for creating data models. It supports type hints and optional fields.

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    tags: list[str] = []
```

- **Key Points**:
  - Fields are defined with type hints.
  - Default values (e.g., `None`, `[]`) make fields optional.
  - FastAPI uses these models to validate request bodies and generate responses.

---

### Set Types
To ensure unique values, use Python's `set` type instead of `list`.

```python
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    tags: set[str] = set()
```

- **Why Use `set`**?
  - Ensures unique values (e.g., no duplicate tags).
  - In requests, a list is converted to a `set`, removing duplicates.
  - In responses, the `set` is converted back to a `list` for JSON compatibility.

---

### Nested Models
Models can include other models as fields for complex data structures.

```python
from pydantic import BaseModel

class Image(BaseModel):
    url: str
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None
```

- **Example JSON**:
```json
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
```

- **Key Points**:
  - Submodels (e.g., `Image`) are defined as types.
  - Nested models can be optional (`None` by default).

---

### Attributes with Lists of Submodels
Models can include lists of submodels for handling multiple related objects.

```python
from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None
```

- **Example JSON**:
```json
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}
```

- **Key Points**:
  - Use `list[Model]` for lists of submodels.
  - `HttpUrl` ensures valid URLs (Pydantic validation).
  - FastAPI endpoint to handle lists:
    ```python
    @app.post("/images/multiple/")
    async def create_multiple_images(images: list[Image]):
        return images
    ```

---

### Special Types and Validation
Pydantic supports special types for advanced validation, such as `HttpUrl`.

```python
from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
    url: HttpUrl
    name: str
```

- **Key Points**:
  - `HttpUrl`: Validates that the string is a valid URL.
  - Other special types include `EmailStr`, `PositiveInt`, etc.
  - Ensures data conforms to expected formats before processing.

---

### Adding Examples in Field
Add example values to fields for better OpenAPI documentation.

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])
```

- **Key Points**:
  - `examples` provides sample values in OpenAPI docs.
  - Improves API usability by showing expected input formats.

---

### Body with Examples
Add examples to the request body using FastAPI's `Body` function.

```python
from typing import Annotated
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2
                }
            ]
        )
    ]
):
    results = {"item_id": item_id, "item": item}
    return results
```

- **Key Points**:
  - `Body(examples=...)` adds example payloads to OpenAPI docs.
  - `Annotated` combines type hints with metadata.

---

### Body with Multiple Examples
Provide multiple example payloads for a single endpoint.

```python
from typing import Annotated
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2
                },
                {
                    "name": "Bar",
                    "price": "35.4"
                },
                {
                    "name": "Baz",
                    "price": "thirty five point four"
                }
            ]
        )
    ]
):
    results = {"item_id": item_id, "item": item}
    return results
```

- **Key Points**:
  - Multiple examples show different valid/invalid cases.
  - FastAPI validates and converts data (e.g., string `"35.4"` to `float`).

---

### OpenAPI Examples
Use `openapi_examples` for richer example documentation with summaries and descriptions.

```python
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2
                    }
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4"
                    }
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four"
                    }
                }
            }
        )
    ]
):
    results = {"item_id": item_id, "item": item}
    return results
```

- **Key Points**:
  - `openapi_examples` provides structured examples with metadata.
  - `summary` and `description` enhance OpenAPI UI documentation.
  - Shows valid, converted, and invalid cases.

---

### Other Data Types
Pydantic supports additional data types for flexible validation:
- `UUID`: Universally Unique Identifier, represented as a `str`.
- `datetime.datetime`: ISO 8601 format (e.g., `2008-09-15T15:53:00+05:00`).
- `datetime.date`: ISO 8601 date (e.g., `2008-09-15`).
- `datetime.time`: ISO 8601 time (e.g., `14:23:55.003`).
- `datetime.timedelta`: Represented as `float` (total seconds) or ISO 8601 time diff.
- `frozenset`: Like `set`, ensures unique values; treated as a list in JSON.
- `bytes`: Treated as `str` with `binary` format in schema.
- `Decimal`: Handled like `float` in requests/responses.

```python
from datetime import datetime, time, timedelta
from typing import Annotated
from uuid import UUID
from fastapi import Body, FastAPI

app = FastAPI()

@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat: Annotated[time, Body()]
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat": repeat,
        "start_process": start_process,
        "duration": duration
    }
```

- **Key Points**:
  - Use `Annotated` to combine type hints with FastAPI metadata.
  - Pydantic handles serialization/deserialization for these types.
  - See [Pydantic documentation](https://docs.pydantic.dev/latest/usage/types/types/) for more types.

---

## Cookie Parameters
Cookies are used for client-side state management, stored in the browser.

```python
from typing import Annotated
from fastapi import Cookie, FastAPI

app = FastAPI()

@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}
```

- **Key Points**:
  - `Cookie()` extracts values from the `Cookie` header.
  - Cookies are optional (`None` by default).
  - Browsers restrict JavaScript access to cookies, impacting API docs UI testing.

---

### Cookie Parameter Models
Group related cookies into a Pydantic model for reusability and validation.

```python
from typing import Annotated
from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None

@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies
```

- **Key Points**:
  - Define cookies as fields in a Pydantic model.
  - Reusable across multiple endpoints.
  - Validates cookie data before processing.

---

### Forbid Extra Cookies
Restrict cookies to only those defined in the model.

```python
from typing import Annotated, Union
from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Cookies(BaseModel):
    model_config = {"extra": "forbid"}
    session_id: str
    fatebook_tracker: Union[str, None] = None
    googall_tracker: Union[str, None] = None

@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies
```

- **Key Points**:
  - `model_config = {"extra": "forbid"}` rejects undefined cookies.
  - Returns error for extra cookies (e.g., `santa_tracker`).
  - Enhances API security by controlling cookie input.

---

## Header Parameters
Headers provide metadata about the request (e.g., authentication, client info).

```python
from typing import Annotated
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
```

- **Key Points**:
  - `Header()` extracts values from request headers.
  - Optional by default (`None`).

---

### Automatic Conversion
FastAPI converts header names (e.g., underscores to hyphens) unless disabled.

```python
from typing import Annotated
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(
    strange_header: Annotated[str | None, Header(convert_underscores=False)] = None
):
    return {"strange_header": strange_header}
```

- **Key Points**:
  - `convert_underscores=False` preserves underscores in header names.
  - Be cautious, as some proxies/servers disallow headers with underscores.

---

### Duplicate Headers
Handle headers with multiple values using a `list`.

```python
from typing import Annotated
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}
```

- **Example Request**:
```
X-Token: foo
X-Token: bar
```

- **Example Response**:
```json
{
    "X-Token values": ["bar", "foo"]
}
```

- **Key Points**:
  - Use `list[str]` to capture multiple header values.
  - FastAPI collects all values into a Python list.

---

### Header Parameter Models
Group related headers into a Pydantic model for reusability.

```python
from typing import Annotated
from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers
```

- **Key Points**:
  - Define headers as fields in a Pydantic model.
  - Supports complex types (e.g., `bool`, `list[str]`).
  - Validates header data before processing.

---

### Forbid Extra Headers
Restrict headers to only those defined in the model.

```python
from typing import Annotated
from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class CommonHeaders(BaseModel):
    model_config = {"extra": "forbid"}
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers
```

- **Key Points**:
  - `model_config = {"extra": "forbid"}` rejects undefined headers.
  - Returns error for extra headers, enhancing security.

---

## Comparison: Headers vs. Cookies

| Feature             | Header                                  | Cookie                                  |
|---------------------|-----------------------------------------|-----------------------------------------|
| **Purpose**         | General request metadata                | Client-side state management            |
| **HTTP Location**   | Individual headers (e.g., `User-Agent`) | `Cookie` header (key-value pairs)       |
| **Storage**         | Not stored on client                    | Stored on client (browser)              |
| **Persistence**     | Per request, no persistence             | Can be persistent or session-based      |
| **FastAPI Utility** | `fastapi.Header`                        | `fastapi.Cookie`                        |
| **Security**        | HTTPS recommended                       | HTTPS, `HttpOnly`, `Secure`, `SameSite` |
| **Use Case**        | Authentication, client info             | Sessions, tracking, preferences         |
| **Example**         | `User-Agent: Mozilla/5.0 ...`           | `Cookie: ads_id=xyz789`                 |

### When to Use
- **Headers**: For metadata like authentication tokens, client type, or custom API metadata.
- **Cookies**: For client-side state management (e.g., sessions, tracking, preferences).

---
