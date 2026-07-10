# FastAPI Request Files, MLOps, and API Metadata 

This Obsidian Markdown file provides a structured overview of FastAPI's file handling, MLOps integration with Prometheus and Evidently, error handling, HTTP status codes, endpoint tagging, and metadata for API documentation. It is designed for studying and quick reference.

---

## Table of Contents
- [Introduction](#introduction)
- [Request Files](#request-files)
  - [Single File Upload](#single-file-upload)
  - [Multiple File Uploads](#multiple-file-uploads)
  - [Dockerizing FastAPI](#dockerizing-fastapi)
- [MLOps Integration](#mlops-integration)
  - [Prometheus Metrics](#prometheus-metrics)
  - [Evidently Data Drift Monitoring](#evidently-data-drift-monitoring)
- [Handling Errors](#handling-errors)
  - [HTTPException](#httpexception)
  - [Response Status Code](#response-status-code)
- [Endpoint Tagging](#endpoint-tagging)
  - [Basic Tags](#basic-tags)
  - [Tags with Enum](#tags-with-enum)
- [API Metadata](#api-metadata)
  - [Summary and Description](#summary-and-description)
  - [Description from Docstring](#description-from-docstring)
  - [Response Description](#response-description)
  - [Deprecating Path Operations](#deprecating-path-operations)
- [Study Tips](#study-tips)

---

## Introduction
FastAPI supports advanced features like file uploads, MLOps integration for monitoring machine learning models, error handling with `HTTPException`, and enhanced API documentation through tags and metadata. This guide covers these concepts with practical examples and best practices for building robust APIs.

---

## Request Files
FastAPI handles file uploads using `File` and `UploadFile`, requiring the `python-multipart` dependency.

### Single File Upload
Handle a single file as raw bytes or an `UploadFile` object.

```python
from typing import Annotated
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # Create uploads directory if it doesn't exist
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    file_location = os.path.join(upload_dir, file.filename)
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}
```

- **Key Points**:
  - `File()`: Extracts raw bytes (`bytes`) from the request.
  - `UploadFile`: Provides metadata (e.g., `filename`) and supports streaming.
  - Use `Annotated` to add metadata or constraints to the file parameter.
  - Install dependency: `pip install python-multipart`.

### Multiple File Uploads
Handle multiple files as a list of `bytes` or `UploadFile` objects.

```python
from typing import Annotated
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.post("/files/")
async def create_files(files: Annotated[list[bytes], File(description="Multiple files as bytes")]):
    return {"file_sizes": [len(file) for file in files]}

@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[list[UploadFile], File(description="Multiple files as UploadFile")]
):
    return {"filenames": [file.filename for file in files]}
```

- **Key Points**:
  - Use `list[bytes]` or `list[UploadFile]` for multiple files.
  - `description` in `File()` adds metadata to OpenAPI docs.
  - `UploadFile` provides access to file metadata like `filename`.

### Dockerizing FastAPI
Deploy FastAPI applications using Docker for consistent environments.

**Dockerfile**:
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
docker run -d --name mycontainer -p 80:80 myimage
```

- **Key Points**:
  - Use `python:3.12` as the base image.
  - Copy `requirements.txt` and install dependencies.
  - Run FastAPI with `uvicorn` on port `8000`.
  - Map container port `80` to host port `80` for external access.

---

## MLOps Integration
FastAPI integrates with MLOps tools like Prometheus for metrics and Evidently for data drift monitoring.

### Prometheus Metrics
Track API performance and predictions using Prometheus metrics.

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY

# Define metrics
REQUEST_COUNT = Counter("request_count", "Total number of requests", ["endpoint", "method"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency", ["endpoint"])
PREDICTION_COUNT = Counter("prediction_count", "Total number of predictions")
PREDICTION_LATENCY = Histogram("prediction_latency_seconds", "Prediction latency")

@app.post("/predict")
async def predict_rainfall(data: List[Rainfall]):
    REQUEST_COUNT.labels(endpoint="/predict", method="POST").inc()
    start_time = time()
    pred = model.predict(input_data)
    latency = time() - start_time
    REQUEST_LATENCY.labels(endpoint="/predict").observe(latency)
    PREDICTION_COUNT.inc()
    PREDICTION_LATENCY.observe(latency)
    return {"predictions": pred}
```

- **Key Points**:
  - `Counter`: Tracks the number of occurrences (e.g., requests, predictions).
  - `Histogram`: Measures latency distributions.
  - Use labels (e.g., `endpoint`, `method`) for granular metrics.
  - Expose metrics via `/metrics` endpoint with `prometheus_client`.

### Evidently Data Drift Monitoring
Monitor data drift in machine learning models using Evidently.

```python
from evidently import Report
from evidently.presets import DataDriftPreset
import pandas as pd

# Define gauges
DRIFT_SCORE = Gauge("drift_score", "Data drift score")
DRIFT_DETECTED = Gauge("drift_detected", "Data drift detected (1 or 0)")

live_data = []  # Buffer for incoming data

@app.post("/predict")
async def predict_rainfall(data: List[Rainfall]):
    input_data = [item.dict() for item in data]
    live_data.extend(input_data)
    
    if len(live_data) >= 50:  # Run drift check every 50 requests
        current_df = pd.DataFrame(live_data, columns=reference_data.columns)
        drift_report = Report(metrics=[DataDriftPreset()])
        drift_report.run(reference_data=reference_data, current_data=current_df)
        
        result = drift_report.as_dict()
        drift_score = result["metrics"][0]["result"]["drift_score"]
        drift_detected = int(result["metrics"][0]["result"]["dataset_drift"])
        
        DRIFT_SCORE.set(drift_score)
        DRIFT_DETECTED.set(drift_detected)
        
        live_data.clear()  # Clear buffer after drift check
    
    return {"predictions": model.predict(input_data)}
```

- **Key Points**:
  - Use `evidently` to detect data drift between reference and live data.
  - Run drift checks periodically (e.g., every 50 requests).
  - Store live data in a buffer (`live_data`) and convert to `pandas.DataFrame`.
  - Update Prometheus gauges (`DRIFT_SCORE`, `DRIFT_DETECTED`) with drift results.
  - Clear buffer after analysis to manage memory.

---

## Handling Errors
FastAPI provides mechanisms to handle errors gracefully.

### HTTPException
Raise `HTTPException` to return custom error responses.

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()
items = {"foo": "The Foo Wrestlers"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

- **Key Points**:
  - `HTTPException(status_code, detail)` returns an error with a specific status code and message.
  - Common status code: `404 Not Found` for missing resources.
  - `detail` provides a human-readable error message.

### Response Status Code
Set the HTTP status code for successful responses.

```python
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item
```

- **Key Points**:
  - Use `status_code=status.HTTP_201_CREATED` for resource creation.
  - Import `status` from `fastapi` for named status code constants.
  - Combines with `response_model` for validated responses.

---

## Endpoint Tagging
Tags organize endpoints in OpenAPI documentation (e.g., Swagger UI).

### Basic Tags
Group endpoints using the `tags` parameter.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

@app.post("/items/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item

@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]

@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]
```

- **Key Points**:
  - `tags=["items"]` groups endpoints under the "items" section in Swagger UI.
  - Improves API organization for large applications.
  - Example: `/docs` shows separate "Items" and "Users" sections.

### Tags with Enum
Use `Enum` to ensure consistent tag usage across endpoints.

```python
from enum import Enum
from fastapi import FastAPI

app = FastAPI()

class Tags(Enum):
    items = "items"
    users = "users"

@app.get("/items/", tags=[Tags.items])
async def get_items():
    return ["Portal gun", "Plumbus"]

@app.get("/users/", tags=[Tags.users])
async def read_users():
    return ["Rick", "Morty"]
```

- **Key Points**:
  - `Enum` prevents typos and ensures consistent tag names.
  - Use `Tags.<name>.value` (e.g., `Tags.items`) in the `tags` parameter.
  - Ideal for large APIs with many tags.

---

## API Metadata
Enhance OpenAPI documentation with summaries, descriptions, and deprecation markers.

### Summary and Description
Add a brief summary and detailed description to endpoints.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    return item
```

- **Key Points**:
  - `summary`: Short title for the endpoint.
  - `description`: Detailed explanation, displayed in Swagger UI.
  - Improves API usability and documentation clarity.

### Description from Docstring
Use function docstrings for endpoint descriptions.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

@app.post("/items/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item
```

- **Key Points**:
  - FastAPI extracts the docstring as the endpoint description.
  - Use Markdown in docstrings for formatted documentation (e.g., bold, lists).
  - Ideal for detailed, multi-line descriptions.

### Response Description
Specify the response description with `response_description`.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item",
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item
```

- **Key Points**:
  - `response_description` describes the response content in Swagger UI.
  - Complements `summary` and `description` for complete documentation.

### Deprecating Path Operations
Mark endpoints as deprecated without removing them.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]

@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]

@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]
```

- **Key Points**:
  - `deprecated=True` marks the endpoint as deprecated in Swagger UI.
  - Deprecated endpoints remain functional but are visually marked.
  - Useful for transitioning APIs without breaking existing clients.

---
