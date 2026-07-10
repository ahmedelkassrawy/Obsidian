(https://github.com/h9-tec/AI_deployment#8-ai-engineering-specific-use-cases)

FastAPI, Pydantic, and SQLAlchemy form a robust stack for various AI engineering applications, from deploying machine learning models to managing complex data pipelines.

### Serving Machine Learning Models (Prediction Endpoints)

(https://github.com/h9-tec/AI_deployment#serving-machine-learning-models-prediction-endpoints)

One of the most common use cases for FastAPI in AI engineering is to serve machine learning models as RESTful APIs. This allows other applications or services to send input data and receive predictions.

```python
# main_ml_model.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Assume you have a pre-trained ML model loaded
# For demonstration, we'll use a dummy prediction function
class MyMLModel:
    def predict(self, data: List[float]) -> float:
        # In a real scenario, this would be your model inference logic
        return sum(data) / len(data) # Simple average as a dummy prediction

ml_model = MyMLModel()

class PredictionInput(BaseModel):
    features: List[float]

class PredictionOutput(BaseModel):
    prediction: float

@app.post("/predict/", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    prediction_result = ml_model.predict(input_data.features)
    return {"prediction": prediction_result}

# Example of a more complex model with multiple outputs or types
class ImageClassificationInput(BaseModel):
    image_url: str

class ImageClassificationOutput(BaseModel):
    class_label: str
    confidence: float
    top_k_labels: List[str]

@app.post("/classify_image/", response_model=ImageClassificationOutput)
async def classify_image(input_data: ImageClassificationInput):
    # In a real scenario, download image from URL, preprocess, and run inference
    # Dummy classification result
    return {
        "class_label": "cat",
        "confidence": 0.95,
        "top_k_labels": ["cat", "dog", "bird"]
    }
```

FastAPI's automatic validation with Pydantic ensures that the input features for your model are always in the expected format, reducing errors and improving reliability. The `response_model` ensures consistent output structure.

### Data Ingestion and Validation for ML Pipelines

(https://github.com/h9-tec/AI_deployment#data-ingestion-and-validation-for-ml-pipelines)

Pydantic is invaluable for defining and validating data schemas at various stages of an ML pipeline, from raw data ingestion to feature engineering.

```python
# data_pipeline_models.py

from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List
from datetime import datetime

class RawSensorData(BaseModel):
    timestamp: datetime
    sensor_id: str
    temperature: float = Field(..., ge=-50, le=100) # Temperature between -50 and 100
    humidity: float = Field(..., ge=0, le=100) # Humidity between 0 and 100
    pressure: Optional[float] = None

class CleanedFeatureData(BaseModel):
    record_id: str
    processed_timestamp: datetime
    avg_temperature_24h: float
    max_humidity_1h: float
    is_anomaly: bool

# Example usage in a data ingestion endpoint
# from fastapi import FastAPI
# from data_pipeline_models import RawSensorData

# app = FastAPI()

# @app.post("/ingest_sensor_data/")
# async def ingest_data(data: RawSensorData):
#     # Data is automatically validated by Pydantic
#     # Save to database, queue for processing, etc.
#     print(f"Received valid sensor data: {data.model_dump_json()}")
#     return {"status": "success", "data_id": data.sensor_id}

# Example of validating data within a script
try:
    valid_data = RawSensorData(timestamp="2025-01-01T10:00:00", sensor_id="S001", temperature=25.5, humidity=60.2)
    print("Valid data:", valid_data)

    invalid_data = RawSensorData(timestamp="2025-01-01T10:00:00", sensor_id="S002", temperature=120.0, humidity=50.0)
except ValidationError as e:
    print("Invalid data:", e.json(indent=2))
```

### Managing Model Metadata and Versions in a Database

(https://github.com/h9-tec/AI_deployment#managing-model-metadata-and-versions-in-a-database)

SQLAlchemy is perfect for storing and managing metadata about your machine learning models, including their versions, training parameters, performance metrics, and deployment status. This is crucial for MLOps and reproducibility.

```python
# ml_metadata_models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class MLModel(Base):
    __tablename__ = "ml_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    version = Column(String, unique=True, index=True) # e.g., v1.0, v1.1
    description = Column(String)
    training_date = Column(DateTime, default=datetime.utcnow)
    accuracy = Column(Float)
    f1_score = Column(Float)
    deployed = Column(Boolean, default=False)
    model_path = Column(String) # Path to the serialized model file

    def __repr__(self):
        return f"<MLModel(name=\"{self.name}\", version=\"{self.version}\")>"

# Example usage:
# from ml_metadata_models import MLModel, Base, engine
# from sqlalchemy.orm import Session

# Base.metadata.create_all(engine) # Create table

# def add_model_metadata(db: Session, name: str, version: str, accuracy: float, f1_score: float, model_path: str):
#     new_model = MLModel(
#         name=name,
#         version=version,
#         accuracy=accuracy,
#         f1_score=f1_score,
#         model_path=model_path
#     )
#     db.add(new_model)
#     db.commit()
#     db.refresh(new_model)
#     return new_model

# def get_latest_model_version(db: Session, model_name: str):
#     return db.query(MLModel).filter(MLModel.name == model_name).order_by(MLModel.training_date.desc()).first()
```

### Asynchronous Task Queues for ML Workloads (e.g., Celery)

(https://github.com/h9-tec/AI_deployment#asynchronous-task-queues-for-ml-workloads-eg-celery)

For long-running machine learning tasks (e.g., model training, batch inference, complex data preprocessing), it's often beneficial to offload them to an asynchronous task queue like Celery. FastAPI can be used to trigger these tasks and provide status updates.

While a full Celery setup is beyond the scope of this guide, here's how FastAPI would interact with it:

```python
# main_celery_ml.py

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List
import time

app = FastAPI()

# --- Dummy Celery-like setup for demonstration ---
# In a real app, you'd import from your Celery app instance

def run_long_ml_task(task_id: str, data: List[float]):
    print(f"Starting long ML task {task_id} with data: {data[:5]}...")
    time.sleep(10) # Simulate long-running ML process
    result = sum(data) # Dummy result
    print(f"Task {task_id} completed with result: {result}")
    # In a real app, save result to DB or cache, update task status

# --- FastAPI Endpoints ---

class MLTaskInput(BaseModel):
    data: List[float]

class MLTaskOutput(BaseModel):
    task_id: str
    status: str

@app.post("/run_ml_task/", response_model=MLTaskOutput)
async def trigger_ml_task(input_data: MLTaskInput, background_tasks: BackgroundTasks):
    task_id = f"ml_task_{int(time.time())}"
    # In a real app, this would be `celery_app.send_task("your_ml_task", args=[task_id, input_data.data])`
    background_tasks.add_task(run_long_ml_task, task_id, input_data.data)
    return {"task_id": task_id, "status": "queued"}

# You would also have an endpoint to check task status (e.g., /task_status/{task_id})
```

### Real-time Inference with WebSockets

(https://github.com/h9-tec/AI_deployment#real-time-inference-with-websockets)

For applications requiring real-time interaction, such as live model predictions based on streaming data, FastAPI supports WebSockets. This allows for persistent, bidirectional communication between the client and the server.

```python
# main_websocket_ml.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
import json

app = FastAPI()

# Dummy real-time ML model
class RealTimeMLModel:
    def process_stream(self, data_point: float) -> float:
        # Simulate a real-time model that processes data points sequentially
        # For example, a moving average, or a simple anomaly detection
        return data_point * 1.1 + 0.5 # Dummy transformation

realtime_model = RealTimeMLModel()

@app.websocket("/ws/realtime_predict")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                input_data = json.loads(data)
                data_point = input_data.get("data_point")
                if data_point is not None and isinstance(data_point, (int, float)):
                    prediction = realtime_model.process_stream(float(data_point))
                    await websocket.send_json({"prediction": prediction})
                else:
                    await websocket.send_json({"error": "Invalid data format, expected {'data_point': float}"})
            except json.JSONDecodeError:
                await websocket.send_json({"error": "Invalid JSON format"})
            except Exception as e:
                await websocket.send_json({"error": str(e)})
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
```

This setup enables low-latency communication for interactive AI applications, such as real-time dashboards, gaming, or continuous monitoring systems. Clients can send data points, and the server can immediately return predictions without the overhead of traditional HTTP request-response cycles.