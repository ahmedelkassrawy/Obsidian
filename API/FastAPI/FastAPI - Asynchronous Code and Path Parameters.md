# FastAPI: Asynchronous Code and Path Parameters

## Asynchronous Code in FastAPI

Asynchronous code allows a program to handle tasks that require waiting for I/O operations (e.g., network requests, file operations) without blocking execution. The program can perform other tasks while waiting for "slow" operations to complete, improving efficiency. This concept is referred to as **concurrency**, distinct from **parallelism**.

### Key I/O Operations

Asynchronous code is typically used for "slow" I/O operations, such as:
- Sending/receiving data over a network.
- Reading/writing files to disk.
- Interacting with remote APIs or databases.
- Waiting for database query results.
### Example: Basic Async Route

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}
```

### HTTP Methods

FastAPI uses standard HTTP methods for different operations:

- `POST`: Create data.
- `GET`: Read data.
- `PUT`: Update data.
- `DELETE`: Delete data.

The `@app.get("/")` decorator indicates that the function handles `GET` requests to the root path (`/`).

Available decorators:
- `@app.get()`
- `@app.post()`
- `@app.put()`
- `@app.delete()`
## Path Parameters
Path parameters are defined in the URL path (e.g., `/items/{item_id}`) and are passed to the function as arguments.
### Basic Path Parameter Example
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

### Order Matters

Path operations are evaluated in order. Specific paths (e.g., `/users/me`) must be declared before generic ones (e.g., `/users/{user_id}`) to avoid conflicts.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```

### Predefined Values with Enum

You can restrict path parameters to predefined values using an `Enum` class.

```python
from enum import Enum
from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}
```

### Multiple Path and Query Parameters

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: int):
    item = {"item_id": item_id, "user_id": user_id}
    return JSONResponse(content=item)
```

## Request Body

A **request body** is data sent by the client to the API, while a **response body** is data sent back by the API. Use Pydantic models to define the structure of the request body.

### Example: Request Body with Pydantic

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    desc: str
    price: float
    tax: float | None = None

@app.post("/items")
async def create_item(item: Item):
    return item
```

### Example: Modifying Request Body Data

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    desc: str
    price: float
    tax: float | None = None

@app.post("/items")
async def create_item(item: Item):
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item.price = price_with_tax
    return item
```

## Advanced Path Parameters

### Importing Path

Use `Path` and `Annotated` for validations and metadata.

```python
from typing import Annotated
from fastapi import FastAPI, Path, Query
```

### Basic Path Parameter with Metadata

```python
app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

**Note**: Path parameters are always required as they are part of the URL.

### FastAPI Version Requirement

- `Annotated` support requires FastAPI **0.95.1** or higher.

### Declaring Metadata

Add metadata like `title` to path parameters.

```python
item_id: Annotated[int, Path(title="The ID of the item to get")]
```

### Parameter Order

Without `Annotated`, Python requires parameters with defaults to follow those without. FastAPI identifies parameters by name and type, so order is flexible.

#### Non-Annotated Example (Python 3.8+)

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

#### Using `*` for Keyword Arguments

Use `*` to enforce keyword arguments, allowing required parameters after optional ones.

```python
@app.get("/items/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

#### Annotated Example (Python 3.9+)

```python
from typing import Annotated
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")], q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

### Numeric Validations

Add numeric constraints using `Path`.

#### Greater Than or Equal (`ge`)

```python
item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)]
```

- Ensures `item_id` ≥ 1.

#### Greater Than (`gt`) and Less Than or Equal (`le`)

```python
item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)]
```

- Ensures `item_id` > 0 and ≤ 1000.

#### Float Validations

```python
@app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str,
    size: Annotated[float, Query(gt=0, lt=10.5)],
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results
```

- `size` must be a float > 0 and < 10.5.

### Validation Keywords

- `gt`: Greater than
- `ge`: Greater than or equal
- `lt`: Less than
- `le`: Less than or equal

### Technical Details

- `Path` and `Query` are functions returning class instances, inheriting from a `Param` class.
- Using functions avoids type errors in editors.

## Recap

- Asynchronous code handles I/O efficiently via concurrency.
- Path parameters are defined in the URL and are always required.
- Use `Path` and `Annotated` for validations and metadata.
- Order matters for path operations; specific paths come before generic ones.
- Pydantic models define request bodies.
- Numeric validations (`gt`, `ge`, `lt`, `le`) work for integers and floats.