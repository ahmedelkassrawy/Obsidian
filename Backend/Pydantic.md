# Pydantic: Data Validation and Settings Management Study Guide

## Overview
Pydantic is a powerful Python library that enforces type hints at runtime, providing **data validation**, **serialization**, and **settings management**. It is a cornerstone of frameworks like FastAPI, ensuring data integrity and boosting developer productivity by catching errors early.

- **Key Benefits**:
  - Runtime type checking and validation.
  - Automatic serialization to JSON (and other formats).
  - Support for complex data structures like nested models and lists.
  - Integration with environment variables for configuration.
  - Significant performance improvements in V2 (up to 50x faster due to Rust-based core).

**Note on Versions**: This guide focuses on **Pydantic V2** (latest as of 2025), with notes on V1 differences where relevant. For migration from V1, refer to the [official migration guide](https://docs.pydantic.dev/latest/migration/).

## Defining Models
Pydantic models are defined as Python classes inheriting from `BaseModel`. They use type hints to specify expected data types, defaults, and validation rules. Use `Field` for advanced options like aliases, constraints, and descriptions.

### Basic Model Examples
```python
# models.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class User(BaseModel):
    id: int
    name: str = "John Doe"  # Default value
    signup_ts: Optional[datetime] = None
    friends: List[int] = []  # List of friend IDs

class Product(BaseModel):
    product_id: str = Field(..., alias="id")  # Required field with alias (maps JSON "id" to product_id)
    name: str
    price: float = Field(..., gt=0)  # Required, must be > 0
    tags: List[str] = []

# Nested model example
class Order(BaseModel):
    order_id: int
    user: User  # Nested User model
    products: List[Product]  # List of Product models
    created_at: datetime = Field(default_factory=datetime.now)  # Factory for current timestamp
```

- **Key Concepts**:
  - `...` indicates a required field (no default).
  - `alias="id"`: Allows incoming data (e.g., JSON) to use a different key name.
  - `gt=0`: Validation constraint (greater than 0). Other constraints: `lt`, `ge`, `le`, `min_length`, etc.
  - `default_factory`: Use for mutable defaults like lists or timestamps to avoid shared state issues.
  - **V1 Difference**: In V1, use `= Field(alias="id")`; V2 is similar but with improved performance.

### Tips
- Import `typing` for `List`, `Optional`, etc.
- Models support generics and unions for advanced types.

## Data Validation and Serialization
Pydantic validates data automatically upon instantiation. Invalid data raises a `ValidationError` with detailed error info. Models can be serialized to JSON using `model_dump_json()` (V2) or `json()` (V1).

### Validation Example
```python
from models import User, Product, Order
from pydantic import ValidationError

# Valid data
user_data = {"id": 123, "name": "Alice"}
user = User(**user_data)  # Unpacks dict into model
print(user.model_dump_json(indent=2))
# Output:
# {
#   "id": 123,
#   "name": "Alice",
#   "signup_ts": null,
#   "friends": []
# }

# Invalid data - missing required field
try:
    invalid_user_data = {"name": "Bob"}
    User(**invalid_user_data)
except ValidationError as e:
    print(e.json(indent=2))
# Output (excerpt):
# [
#   {
#     "type": "missing",
#     "loc": ["id"],
#     "msg": "Field required",
#     "input": {"name": "Bob"}
#   }
# ]
```

### Serialization Examples
```python
# Single model serialization
product_data = {"id": "P001", "name": "Laptop", "price": 1200.50}
product = Product(**product_data)
print(product.model_dump_json(indent=2))
# Output:
# {
#   "product_id": "P001",
#   "name": "Laptop",
#   "price": 1200.5,
#   "tags": []
# }

# Nested model validation and serialization
order_data = {
    "order_id": 1,
    "user": {"id": 456, "name": "Charlie"},
    "products": [
        {"id": "P002", "name": "Mouse", "price": 25.0},
        {"id": "P003", "name": "Keyboard", "price": 75.0}
    ]
}
order = Order(**order_data)  # Validates nested structures
print(order.model_dump_json(indent=2))
# Output: JSON with nested User and Products, respecting aliases and validations
```

- **Key Methods**:
  - `model_validate(data)`: Alternative to `**data` for validation (useful for ORMs in V2 with `from_attributes=True`).
  - `model_dump()`: Serialize to dict (V2; use `dict()` in V1).
  - `model_dump_json()`: Serialize to JSON string (V2; use `json()` in V1).
- **Error Handling**: `ValidationError` provides location (`loc`), message (`msg`), and input context.
- **V1 vs V2**: V2 is stricter on types and faster; no more "magic" coercion by default (use `strict=False` if needed).

### Common Validation Scenarios
| Scenario | Example Constraint | Notes |
|----------|--------------------|-------|
| Required Field | `Field(...)` | Raises error if missing. |
| Range | `Field(gt=0, lt=100)` | Numeric bounds. |
| String Length | `Field(min_length=3, max_length=50)` | For strings. |
| Regex | `Field(regex=r"^[a-zA-Z0-9]+$")` | Pattern matching. |
| Nested Validation | Embed models | Recursively validates sub-models. |
| Custom Types | Use `conint` from `pydantic.types` | Constrained integers (e.g., `conint(gt=0)`). |

## Settings Management
Pydantic's `BaseSettings` (moved to `pydantic-settings` in V2) loads and validates configuration from environment variables, `.env` files, and more. It supports type coercion and defaults.

### Settings Example
```python
# settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "My Awesome App"
    admin_email: str
    database_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")  # V2 config

# V1 Equivalent (for reference):
# from pydantic import BaseSettings
# class Settings(BaseSettings):
#     # ... fields ...
#     class Config:
#         env_file = ".env"
#         extra = "ignore"

# Usage
# Create .env file:
# ADMIN_EMAIL="admin@example.com"
# DATABASE_URL="postgresql://user:password@host:port/dbname"

settings = Settings()
print(f"App Name: {settings.app_name}")
print(f"Admin Email: {settings.admin_email}")
print(f"Database URL: {settings.database_url}")
```

- **Key Features**:
  - Automatically maps env vars (e.g., `ADMIN_EMAIL` to `admin_email`).
  - Supports `.env` files via `env_file`.
  - `extra="ignore"`: Ignores extra fields (options: `"allow"`, `"forbid"`).
  - Prefix env vars with app name if needed (e.g., `MYAPP_ADMIN_EMAIL`).
- **V2 Changes**: Import from `pydantic_settings`; use `SettingsConfigDict` instead of `class Config`. Custom sources (e.g., YAML) use `settings_customise_sources`.
- **Best Practices**: Use for dev/prod configs; validate types like URLs or secrets.

## Custom Validators
For business logic beyond built-in constraints, use `@field_validator` (V2) or `@validator` (V1). Validators run during instantiation and can raise `ValueError` for failures.

### Custom Validator Example
```python
# models.py (continued)
from pydantic import BaseModel, field_validator, ValidationError

class UserProfile(BaseModel):
    username: str
    email: str
    age: int

    @field_validator('email')  # V2: Decorator for field-specific validation
    @classmethod
    def validate_email_domain(cls, v: str) -> str:
        if "@example.com" not in v:
            raise ValueError("Email must be from example.com domain")
        return v

    # V1 Equivalent:
    # from pydantic import validator
    # @validator('email')
    # def validate_email_domain(cls, v):
    #     if "@example.com" not in v:
    #         raise ValueError("Email must be from example.com domain")
    #     return v

# Test
try:
    user_profile = UserProfile(username="testuser", email="test@example.com", age=30)
    print(user_profile)

    invalid_user_profile = UserProfile(username="another", email="another@gmail.com", age=25)
except ValidationError as e:
    print(e.json(indent=2))  # Shows validation error details
```

- **Key Points**:
  - `@field_validator('field_name')`: Targets specific fields; `@classmethod` for class-level.
  - Access other fields via `values` dict in V2 (e.g., `def validator(cls, v, values)` for dependencies).
  - For model-wide validation, use `@model_validator` (V2; `@root_validator` in V1).
  - Raise `ValueError` for custom errors; Pydantic wraps it in `ValidationError`.
- **V2 Enhancements**: Validators are faster; supports `mode='before'/'after'` for pre/post-validation logic. No more `each_item=True` for lists—use separate validators or `TypeAdapter`.

## Pydantic V1 vs V2 Comparison
| Feature | V1 | V2 | Migration Notes |
|---------|----|----|-----------------|
| **BaseSettings** | In `pydantic` | In `pydantic-settings` | Install separately; use `SettingsConfigDict`. |
| **Validators** | `@validator` | `@field_validator` or annotated validators | Update decorators; V2 is stricter and faster. |
| **Serialization** | `dict()`, `json()` | `model_dump()`, `model_dump_json()` | Similar output; V2 excludes None by default if specified. |
| **Config** | `class Config` | `model_config = ConfigDict(...)` | Nested dict for settings like `extra="ignore"`. |
| **Performance** | Python-based | Rust core (pydantic-core) | 4-50x faster; strict mode by default. |
| **Other** | `parse_obj()` | `model_validate()` | Supports `from_attributes=True` for ORM. |

- **When to Upgrade**: V2 is recommended for new projects; use V1 compatibility mode (`from pydantic import v1`) for gradual migration.
- **Common Pitfalls**: V2 is stricter (e.g., no auto-coercion); test thoroughly.