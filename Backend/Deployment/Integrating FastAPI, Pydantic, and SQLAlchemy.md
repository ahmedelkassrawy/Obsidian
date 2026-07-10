(https://github.com/h9-tec/AI_deployment#6-integrating-fastapi-pydantic-and-sqlalchemy)

This section brings together FastAPI, Pydantic, and SQLAlchemy to build a complete, functional API. We will demonstrate how to manage database sessions using FastAPI's dependency injection system and how to use Pydantic models for both request validation and response serialization.

### Database Session Dependency
[https://github.com/h9-tec/AI_deployment#database-session-dependency]

FastAPI's dependency injection system is perfect for managing database sessions. We'll create a dependency that provides a database session for each request and ensures it's closed afterward.

First, ensure you have your `database_orm.py` and `models_orm.py` set up as described in the previous sections. We'll use the `get_db` function from `database_orm.py` as a dependency.

```python
# main_integrated.py

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Import Pydantic models (from models.py or models_orm.py if you prefer)
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True # Pydantic V2: orm_mode = True in Pydantic V1

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    owner_id: int

    class Config:
        from_attributes = True # Pydantic V2: orm_mode = True in Pydantic V1

# Import SQLAlchemy ORM models and session setup
from models_orm import Base, User, Product, engine
from database_orm import get_db # This is our dependency

# Create all tables (run once)
Base.metadata.create_all(bind=engine)

app = FastAPI()

### Creating API Endpoints with Database Operations

Let's create API endpoints for users and products, demonstrating how to use the database session dependency and Pydantic models.
```

```python
# main_integrated.py (continued)
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/{user_id}/products/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product_for_user(
    user_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_product = Product(**product.model_dump(), owner_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
```

To run this integrated application, save the code above as `main_integrated.py` (or merge it into your `main.py` if you prefer) and run:

```shell
uvicorn main_integrated:app --reload
```

Then, navigate to `http://127.0.0.1:8000/docs` to interact with the API.

### Handling Request and Response Models with Pydantic

(https://github.com/h9-tec/AI_deployment#handling-request-and-response-models-with-pydantic)

In the example above, notice the use of Pydantic models for both incoming request bodies and outgoing responses:

- **Request Models (`UserCreate`, `ProductCreate`)**: These models define the expected structure and types of data that clients send to your API. FastAPI automatically validates the incoming JSON against these Pydantic models. If the data is invalid, FastAPI returns a clear error message.
    
- **Response Models (`UserResponse`, `ProductResponse`)**: These models define the structure of the data that your API sends back to clients. The `response_model` argument in FastAPI's path operation decorators (`@app.post`, `@app.get`) ensures that the data returned by your endpoint function is automatically serialized and validated against the specified Pydantic model. This is crucial for:
    
    - **Data Filtering**: You can exclude sensitive fields (e.g., passwords) from responses by not including them in the `Response` model.
    - **Data Transformation**: You can transform data before sending it to the client (e.g., formatting dates).
    - **Automatic Documentation**: FastAPI uses these models to generate accurate OpenAPI (Swagger UI) documentation for your API's responses.

The `Config.from_attributes = True` (or `Config.orm_mode = True` in Pydantic V1) in the `UserResponse` and `ProductResponse` models is essential when working with SQLAlchemy ORM objects. It tells Pydantic to read data from object attributes (like `user.id`, `user.username`) rather than just dictionary keys, allowing you to directly pass SQLAlchemy ORM instances to your Pydantic response models for serialization. This seamless integration greatly simplifies data handling between your database and API.