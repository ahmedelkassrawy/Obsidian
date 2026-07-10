# FastAPI Response Models and Status Codes Study Notes

This Obsidian Markdown file provides a structured overview of FastAPI's response models, return types, and HTTP status codes, with a focus on using Pydantic for data validation and serialization. It is designed for studying and quick reference.

---

## Table of Contents
- [Introduction](#introduction)
- [Response Model - Return Type](#response-model---return-type)
  - [Single Model Response](#single-model-response)
  - [List of Models Response](#list-of-models-response)
- [Add an Output Model](#add-an-output-model)
- [Extra Models](#extra-models)
  - [Multiple Models for Different Purposes](#multiple-models-for-different-purposes)
- [Pydantic Dict and Unpacking](#pydantic-dict-and-unpacking)
  - [Dict Method](#dict-method)
  - [Unpacking](#unpacking)
- [Union or AnyOf](#union-or-anyof)
- [List of Models](#list-of-models)
- [Response Status Codes](#response-status-codes)
  - [Status Code Ranges](#status-code-ranges)
  - [Using Status Codes in FastAPI](#using-status-codes-in-fastapi)
- [Study Tips](#study-tips)

---

## Introduction
FastAPI leverages **Pydantic** models to define request and response structures, ensuring type safety and automatic OpenAPI documentation. The `response_model` parameter in FastAPI endpoints specifies the expected return type, which is validated and serialized using Pydantic. HTTP status codes communicate the outcome of a request, with FastAPI providing flexible ways to set them.

This guide covers how to define response models, handle multiple model types, and use status codes effectively.

---

## Response Model - Return Type
The `response_model` parameter in FastAPI defines the structure of the response, ensuring it conforms to a Pydantic model.

### Single Model Response
Define a single Pydantic model as the response type for an endpoint.

```python
from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item
```

- **Key Points**:
  - `response_model=Item` ensures the response conforms to the `Item` model.
  - The endpoint accepts an `Item` and returns it, validated and serialized.
  - `-> Any` is used to allow flexibility in return type (though the response will match `Item`).

### List of Models Response
Return a list of Pydantic models using `response_model=list[Model]`.

```python
@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]
```

- **Key Points**:
  - `response_model=list[Item]` specifies a list of `Item` models.
  - FastAPI validates and serializes the response as a list of objects conforming to `Item`.
  - Missing optional fields (e.g., `description`, `tax`, `tags`) are handled automatically.

---

## Add an Output Model
Separate input and output models to control what data is sent to the client.

```python
from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user
```

- **Key Points**:
  - `UserIn` includes sensitive fields like `password`.
  - `UserOut` excludes `password` for security in responses.
  - `response_model=UserOut` ensures only `UserOut` fields are returned.
  - FastAPI automatically filters out fields not in `UserOut` (e.g., `password`).

---

## Extra Models
Use multiple models for different purposes (e.g., input, output, database).

### Multiple Models for Different Purposes
Separate models for input, output, and database storage to handle sensitive data like passwords.

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
```

- **Key Points**:
  - **Input Model (`UserIn`)**: Includes `password` for user input.
  - **Output Model (`UserOut`)**: Excludes sensitive data like `password`.
  - **Database Model (`UserInDB`)**: Stores `hashed_password` instead of raw password.
  - `fake_save_user` simulates saving a user with a hashed password.
  - `response_model=UserOut` ensures sensitive data (`hashed_password`) is not returned.

---

## Pydantic Dict and Unpacking
Pydantic models can be converted to dictionaries and unpacked for creating new model instances.

### Dict Method
Convert a Pydantic model to a dictionary using `.dict()`.

```python
user_in = UserIn(
    username="john",
    password="secret",
    email="john.doe@example.com"
)

user_dict = user_in.dict()
print(user_dict)
```

**Output**:
```json
{
    "username": "john",
    "password": "secret",
    "email": "john.doe@example.com",
    "full_name": null
}
```

- **Key Points**:
  - `.dict()` converts a Pydantic model to a Python dictionary.
  - Includes all fields, with `None` for optional fields not provided.

### Unpacking
Use dictionary unpacking to create a new model instance.

```python
user_in_db = UserInDB(**user_dict)
```

**Equivalent to**:
```python
UserInDB(
    username=user_dict["username"],
    password=user_dict["password"],
    email=user_dict["email"],
    full_name=user_dict["full_name"]
)
```

- **Key Points**:
  - `**user_dict` unpacks dictionary key-value pairs into model constructor arguments.
  - Useful for converting between models (e.g., `UserIn` to `UserInDB`).

---

## Union or AnyOf
Use `Union` to allow multiple response types for an endpoint.

```python
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type: str = "car"

class PlaneItem(BaseItem):
    type: str = "plane"
    size: int

items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5
    }
}

@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]
```

- **Key Points**:
  - `Union[PlaneItem, CarItem]` allows the response to be either `PlaneItem` or `CarItem`.
  - FastAPI validates the response against both models and selects the appropriate one.
  - Useful for endpoints returning different object types based on input.

---

## List of Models
Return a list of Pydantic models for endpoints returning multiple items.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str

items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"}
]

@app.get("/items/", response_model=list[Item])
async def read_items():
    return items
```

- **Key Points**:
  - `response_model=list[Item]` ensures all items in the list conform to the `Item` model.
  - FastAPI validates and serializes each item in the list.
  - Ideal for endpoints returning collections of data.

---

## Response Status Codes
HTTP status codes indicate the outcome of a request. FastAPI allows setting them explicitly.

### Status Code Ranges
- **100–199 (Informational)**:
  - Rarely used directly.
  - Cannot have a response body.
- **200–299 (Successful)**:
  - Most commonly used.
  - Examples:
    - `200 OK`: Default, everything worked.
    - `201 Created`: New resource created (e.g., database record).
    - `204 No Content`: Successful, but no content to return (no body).
- **300–399 (Redirection)**:
  - May have a body (except `304 Not Modified`).
  - Used for redirects.
- **400–499 (Client Error)**:
  - Common for client-side errors.
  - Examples:
    - `400 Bad Request`: Generic client error.
    - `404 Not Found`: Resource not found.
- **500–599 (Server Error)**:
  - Rarely used directly.
  - Automatically returned for server-side errors (e.g., `500 Internal Server Error`).

### Using Status Codes in FastAPI
Set status codes using the `status_code` parameter or `status` constants.

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}
```

**Using `status` constants**:
```python
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
```

- **Key Points**:
  - `status_code=201` or `status.HTTP_201_CREATED` sets the response status to `201 Created`.
  - Use `status` module for named constants (e.g., `status.HTTP_201_CREATED`) for clarity.
  - Default status code is `200 OK` if not specified.
  - Use `204 No Content` for endpoints that don’t return data.

---
