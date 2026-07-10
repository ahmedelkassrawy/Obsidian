# FastAPI with MongoDB Integration Study Notes

This Obsidian Markdown file provides a structured overview of integrating FastAPI with MongoDB using Motor (an async MongoDB driver) and Pydantic for data modeling. It covers setting up a Docker container, defining database models, handling MongoDB ObjectIds, and implementing CRUD endpoints. The content is designed for studying and quick reference.

---

## Table of Contents
- [Introduction](#introduction)
- [Setup Docker Container](#setup-docker-container)
- [MongoDB Integration](#mongodb-integration)
  - [Connecting to MongoDB with Motor](#connecting-to-mongodb-with-motor)
  - [Handling ObjectId in Pydantic](#handling-objectid-in-pydantic)
- [Database Models](#database-models)
  - [StudentModel](#studentmodel)
  - [UpdateStudent](#updatestudent)
  - [StudentCollection](#studentcollection)
- [CRUD Endpoints](#crud-endpoints)
  - [Create Student](#create-student)
  - [List Students](#list-students)
  - [Show Student](#show-student)
  - [Update Student](#update-student)
  - [Delete Student](#delete-student)
- [Study Tips](#study-tips)

---

## Introduction
FastAPI integrates seamlessly with MongoDB using **Motor**, an asynchronous MongoDB driver for Python. Pydantic is used to define data models, ensuring validation and serialization, while handling MongoDB’s `ObjectId` type requires special configuration. This guide covers setting up a FastAPI app with MongoDB, defining models, and implementing CRUD operations.

---

## Setup Docker Container
Deploy the FastAPI application with MongoDB using Docker for a consistent environment.

**Dockerfile** (assumed, as not provided in the code snippet):
```docker
FROM python:3.12

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**Build and Run**:
```bash
docker build -t myimage .
docker run -d --name mycontainer -p 80:8000 myimage
```

- **Key Points**:
  - Use `python:3.12` as the base image.
  - Install dependencies from `requirements.txt` (e.g., `fastapi`, `uvicorn`, `motor`, `pydantic`).
  - Run the FastAPI app with `uvicorn` on port `8000`.
  - Map container port `8000` to host port `80`.
  - Ensure MongoDB is accessible (e.g., running locally or in another container with `mongodb://host:27017`).

**Note**: To connect to MongoDB, ensure the `MONGO_URL` environment variable (e.g., `mongodb://mongodb:27017/`) is set correctly, and the MongoDB service is running.

---

## MongoDB Integration

### Connecting to MongoDB with Motor
Use **Motor** for asynchronous MongoDB operations in FastAPI.

```python
import os
from motor import motor_asyncio
from fastapi import FastAPI

app = FastAPI()

os.environ["MONGO_URL"] = "mongodb://localhost:27017/"
os.environ["DB_NAME"] = "db_trial"
os.environ["COLLECTION_NAME"] = "student"

client = motor_asyncio.AsyncIOMotorClient(os.environ["MONGO_URL"])
db = client.get_database(os.environ["DB_NAME"])
student_collection = db.get_collection(os.environ["COLLECTION_NAME"])
```

- **Key Points**:
  - `AsyncIOMotorClient`: Connects to MongoDB asynchronously.
  - `get_database` and `get_collection`: Access the database (`db_trial`) and collection (`student`).
  - Use environment variables (`MONGO_URL`, `DB_NAME`, `COLLECTION_NAME`) for configuration flexibility.
  - Install Motor: `pip install motor`.

### Handling ObjectId in Pydantic
MongoDB’s `ObjectId` is not JSON-serializable, so it needs special handling in Pydantic models.

```python
from typing import Annotated
from pydantic import BeforeValidator
from bson.objectid import ObjectId

PyObjectId = Annotated[str, BeforeValidator(str)]
```

- **Key Points**:
  - `PyObjectId`: A custom type that converts `ObjectId` to `str` for JSON serialization.
  - `BeforeValidator(str)`: Ensures `ObjectId` is converted to a string before validation.
  - Used in models to handle MongoDB’s `_id` field.

---

## Database Models
Define Pydantic models for MongoDB data, with configurations for `ObjectId` and field aliases.

### StudentModel
Represents a student document in MongoDB.

```python
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class StudentModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    email: EmailStr
    course: str
    gpa: float

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
```

- **Key Points**:
  - `id: Optional[PyObjectId]`: Maps to MongoDB’s `_id` field, optional with default `None`.
  - `alias="_id"`: Handles MongoDB’s `_id` field, as Python treats leading underscores as private variables.
  - `populate_by_name=True`: Allows field access by alias (e.g., `_id`) in addition to `id`.
  - `arbitrary_types_allowed=True`: Permits custom types like `PyObjectId`.
  - `json_encoders={ObjectId: str}`: Serializes `ObjectId` as strings in JSON responses.

### UpdateStudent
Model for updating student data, with all fields optional.

```python
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
import uuid

class UpdateStudent(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=uuid.uuid4, alias="_id", default=None)
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    course: Optional[str] = None
    gpa: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
```

- **Key Points**:
  - All fields are optional to allow partial updates.
  - `default_factory=uuid.uuid4`: Generates a UUID if no `id` is provided (though typically unused for updates, as MongoDB generates `_id`).
  - Same `model_config` settings as `StudentModel` for consistency.

### StudentCollection
Model for returning a list of students.

```python
class StudentCollection(BaseModel):
    students: List[StudentModel]
```

- **Key Points**:
  - Wraps a list of `StudentModel` for endpoints returning multiple students.
  - Simplifies response structure for list-based queries.

---

## CRUD Endpoints
Implement Create, Read, Update, and Delete (CRUD) operations for the `student` collection.

### Create Student
Insert a new student document into MongoDB.

```python
from fastapi import FastAPI
from pydantic import BaseModel

@app.post("/students/", response_model=StudentModel)
async def create_student(student: StudentModel):
    new_student = await student_collection.insert_one(
        student.model_dump(by_alias=True, exclude=["id"])
    )
    created_student = await student_collection.find_one({"_id": new_student.inserted_id})
    return StudentModel(**created_student)
```

- **Key Points**:
  - `response_model=StudentModel`: Ensures the response conforms to `StudentModel`.
  - `model_dump(by_alias=True, exclude=["id"])`: Converts the model to a dict, using `_id` alias and excluding `id` (MongoDB generates `_id`).
  - `insert_one`: Inserts the document and returns the generated `_id`.
  - `find_one`: Retrieves the created document to return as a `StudentModel`.

### List Students
Retrieve a list of all students.

```python
@app.get("/students/", response_model=StudentCollection)
async def list_students():
    return StudentCollection(
        students=await student_collection.find().to_list(1000)
    )
```

- **Key Points**:
  - `response_model=StudentCollection`: Returns a list of students wrapped in `StudentCollection`.
  - `find().to_list(1000)`: Retrieves up to 1000 documents from the collection.
  - Converts MongoDB documents to `StudentModel` instances via `StudentCollection`.

### Show Student
Retrieve a single student by ID.

```python
from bson.objectid import ObjectId

@app.get("/students/{id}", response_model=StudentModel)
async def show_student(id: str):
    if (student := await student_collection.find_one({"_id": ObjectId(id)})) is not None:
        return StudentModel(**student)
    raise HTTPException(status_code=404, detail="Student not found")
```

- **Key Points**:
  - `ObjectId(id)`: Converts the string `id` to a MongoDB `ObjectId`.
  - `find_one`: Retrieves the document matching `_id`.
  - Returns `StudentModel` if found; otherwise, raises `HTTPException` with `404`.

### Update Student
Update an existing student by ID.

```python
from fastapi import Body, HTTPException

@app.put("/students/{id}", response_model=StudentModel)
async def update_student(id: str, student: UpdateStudent = Body(...)):
    student_data = {
        k: v for k, v in student.model_dump(by_alias=True).items() if v is not None
    }
    update_result = await student_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": student_data}
    )
    if update_result:
        return StudentModel(**update_result)
    else:
        raise HTTPException(status_code=404, detail="Student not found")
```

- **Key Points**:
  - `UpdateStudent`: Allows partial updates (all fields optional).
  - `model_dump(by_alias=True)`: Converts to dict with `_id` alias.
  - Filters out `None` values to update only provided fields.
  - `find_one_and_update` with `$set`: Updates the document and returns the original.
  - Raises `HTTPException` if the student is not found.

### Delete Student
Delete a student by ID.

```python
from fastapi import HTTPException

@app.delete("/students/{id}")
async def delete_student(id: str):
    delete_res = await student_collection.delete_one({"_id": ObjectId(id)})
    if delete_res.deleted_count == 1:
        return {"detail": "Student deleted"}
    else:
        raise HTTPException(status_code=404, detail="Student not found")
```

- **Key Points**:
  - `delete_one`: Deletes the document matching `_id`.
  - Returns a success message if `deleted_count == 1`.
  - Raises `HTTPException` if no document is found.

---
