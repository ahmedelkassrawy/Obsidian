---
description: "Community-talk notes on getting models to production: MLOps maturity levels and anti-patterns, Python project structure with pyproject.toml, serving a model as a REST API, and ONNX export."
domain: ml
type: concept
status: digested
tags:
  - domain/ml
  - type/concept
  - status/digested
  - topic/mlops
  - topic/docker
  - topic/api-design
  - topic/testing
  - mlops
  - fastapi
  - onnx
  - docker
  - pytest
  - serialization
  - logging
  - python
aliases:
  - "1."
  - "MLOps maturity levels"
  - "model as REST API"
  - "ONNX"
hubs:
  - "[[MLOps]]"
  - "[[Docker]]"
  - "[[API Design]]"
  - "[[Testing]]"
---

## MLOps Maturity Levels

How far a team has automated the path from notebook to production.

| Level | Name | What it looks like |
| --- | --- | --- |
| 0 | No MLOps | Notebook only, everything manual |
| 1 | Manual Process | Scripts exist, but deployments are manual |
| 2 | ML Pipeline | Automated training, experiment tracking, basic CI |
| 3 | CD for ML | Auto-retraining on a trigger, model registry, monitoring |
| 4 | Full MLOps | Zero-touch pipelines, auto-rollback, full observability |

> [!note] The source had two "Level 1"s
> The original note labeled both "No MLOPS" and "Manual Process" as Level 1. I renumbered them 0–4 so each level is distinct. Flagging in case the course actually uses 1–5 — easy to shift.

## Common Anti-Patterns

Things that quietly break a model project:

- **Hardcoded / static paths** — should be environment variables or a secrets vault.
- **No input validation** — malformed input creates unexpected data downstream.
- **No API** — if nothing exposes the model, nobody else can call it.
- **No versioning** — you can't tell which model is in production right now.

## Python Project Structure

A clean layout that CI and tooling understand from day one.

| Folder / file | Why it exists |
| --- | --- |
| `src/` | Installable package — import your own code cleanly |
| `tests/` | Auto-discovered by pytest — CI-ready from day 1 |
| `configs/` | Separate config from code — no magic constants |
| `notebooks/` | Exploration only — never import from notebooks |
| `Dockerfile` | Reproducible runtime — same environment everywhere |
| `pyproject.toml` | Single source of truth for dependencies and tools |

> [!definition] `__init__.py`
> An empty (or small) file that marks a folder as a Python package, which makes the modules inside it importable.

```text
src/
    __init__.py
    model.py
    pipeline.py
    utils.py
tests/
    test_model.py
configs/
    config.yaml
notebooks/
    exploration.ipynb
Dockerfile
pyproject.toml
README.md
```

> [!example]- Line by line: the folder layout
> The idea is **separate things that change for different reasons**.
> - `src/` is your real code, packaged so you can write `from src.model import ...` from anywhere.
> - `tests/` is where pytest looks automatically.
> - `configs/` holds numbers and paths that change per environment, so they are not buried in code.
> - `notebooks/` is for exploring only. Never import from a notebook: cells run out of order and hide state.
> - `pyproject.toml` lists dependencies and tool settings in one file.
> - `__init__.py` is an empty file that tells Python "this folder is a package". Without it `import src.model` fails.


> [!question] The team problem this solves
> An ML team where each person uses a different framework, everyone predicts locally, and nobody can share the project or the predictions. The structure above (plus a shared API and serialization) is what fixes it.

## pyproject.toml

One file to rule all your tooling. It contains:

1. Project metadata (name, version, Python constraint).
2. Dev dependencies, kept separate from runtime deps.
3. Ruff configuration.
4. An editable install of your package.

Set it up with `uv`:

```bash
uv init project-name
```

```bash
uv add fastapi
```

> [!example]- What uv does here
> `uv` is a fast replacement for pip + venv.
> - `uv init` creates `pyproject.toml`.
> - `uv add fastapi` installs FastAPI **and** writes it into `pyproject.toml`, so the next person can rebuild the environment exactly.
> The point: dependencies are recorded, not remembered.


## OOP and Type Hints

Define a base class so every model is forced to implement `.predict()`.

```python
from abc import ABC, abstractmethod


class ModelBase(ABC):
    @abstractmethod
    def predict(self, X: list[float]) -> float: ...


class RideDurationModel(ModelBase):
    def __init__(self, threshold: float = 60.0) -> None:
        self.threshold = threshold
        self._model = None

    def predict(self, X: list[float]) -> float:
        pred = self._model.predict([X])[0]
        return min(pred, self.threshold)
```

> [!example]- Line by line: ModelBase and RideDurationModel
> ```python
> class ModelBase(ABC):
>     @abstractmethod
>     def predict(self, X: list[float]) -> float: ...
> ```
> - `ABC` = abstract base class. You cannot create it directly; it exists only to define a contract.
> - `@abstractmethod` says "any child class MUST write its own `predict`, or Python refuses to create it".
> - Result: every model, whatever library is inside, has `.predict(list_of_floats) -> float`. The API code can treat all models the same.
>
> ```python
> def __init__(self, threshold: float = 60.0) -> None:
>     self.threshold = threshold
>     self._model = None
> ```
> - `threshold` caps the prediction (a ride never predicts longer than 60 minutes).
> - `self._model` is where the real sklearn/XGBoost object will live. The underscore means "private, do not touch from outside".
> - This is **composition**: the class *holds* a model instead of *being* a subclass of sklearn's class, so you can swap the inner model without changing the outside.
>
> ```python
> pred = self._model.predict([X])[0]
> return min(pred, self.threshold)
> ```
> - sklearn wants a 2D input (a batch of rows), so the single row `X` is wrapped as `[X]`, and `[0]` takes the one answer back out.
> - `min(...)` applies the cap.
>
> Type hints like `X: list[float]` do not change behaviour at runtime. They let tools (mypy, your editor) catch "you passed a string" before the code runs.


Why it's written this way:

- **Abstract base class** — forces every model to implement `.predict()`.
- **Type hints** — catch bugs before runtime.
- **Docstrings** — keep the code documentation-focused.
- **Composition** — the real model is kept private (`self._model`), not inherited from a parent class.

## Your Model as a REST API

Wrap the model in FastAPI so anyone can call it over HTTP.

Key ideas:

- **Pydantic validation** — reject bad input at the door.
- **Load the model once** — not on every request.
- **`response_model`** — FastAPI validates your response too, not just the request.

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
from src.model import RideDurationModel

app = FastAPI(title="Ride Duration API")
model = RideDurationModel()  # loaded once


class PredictRequest(BaseModel):
    distance_km: float = Field(..., gt=0)
    passengers: int = Field(1, ge=1)


class PredictResponse(BaseModel):
    duration_min: float


@app.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest):
    d = model.predict([req.distance_km, req.passengers])
    return PredictResponse(duration_min=round(d, 2))
```

> [!example]- Line by line: the FastAPI app
> ```python
> app = FastAPI(title="Ride Duration API")
> model = RideDurationModel()  # loaded once
> ```
> The model is created at import time, once, when the server starts. If it were created inside the endpoint, every request would reload the model file (hundreds of ms each).
>
> ```python
> class PredictRequest(BaseModel):
>     distance_km: float = Field(..., gt=0)
>     passengers: int = Field(1, ge=1)
> ```
> Pydantic models describe the JSON you accept. `Field(..., gt=0)` = required (`...`) and must be greater than 0. `Field(1, ge=1)` = default 1, must be at least 1. If a client sends `distance_km: -1`, FastAPI rejects it with a 422 **before your code runs**. That is "reject bad input at the door".
>
> ```python
> @app.post("/predict", response_model=PredictResponse)
> async def predict(req: PredictRequest):
> ```
> - `@app.post("/predict")` registers this function to handle `POST /predict`.
> - `req: PredictRequest` tells FastAPI to parse and validate the JSON body into that class.
> - `response_model=PredictResponse` validates what you *return* too, and documents it at `/docs`.
> - `async def` lets the server handle other requests while this one *waits*. One warning the source skips: `model.predict` is CPU work, not waiting, so `async` alone does not help here. For heavy models use a plain `def` (FastAPI runs it in a thread pool) or offload to a worker. See [[Concurrency & Async]].


### API Checklist

| Practice | Why it matters |
| --- | --- |
| Input validation | Reject malformed data before it reaches the model |
| Health endpoint | Load balancers read `/health` to route traffic |
| Model loaded once | Loading on every request adds 200–500 ms |
| Async handlers | Sync handlers block the server under load → use `async def predict` |
| Response schema | Unvalidated responses hide bugs until production → `response_model=PredictResponse` |
| Auto-generated docs | Available at `/docs` |

## Serialization Formats

How you save a model or message to bytes, and the trade-offs.

| Format | Type | Speed | Size | Human-readable | Best for |
| --- | --- | --- | --- | --- | --- |
| **JSON** | Text | Slow | Large | Yes | REST APIs, configs, logging |
| **MessagePack** | Binary | Fast | Small | No | High-throughput inter-service calls |
| **Protobuf** | Binary | Fast | Tiny | No | gRPC services, streaming pipelines |
| **Pickle** | Binary | Fast | Medium | No | Python-only model files — never in APIs |
| **ONNX** | Binary | — | Medium | No | Cross-framework model portability |

> [!example]- What serialization means
> Serialization = turning an object into bytes to save or send.
> - JSON is text and readable, so it is the default for APIs.
> - MessagePack and Protobuf are binary: smaller and faster, for service-to-service traffic.
> - Pickle is Python-only and can execute code when loaded. Never accept a pickle from outside.
> - ONNX is a serialization format specifically for models.


## ONNX

> [!definition] ONNX
> A common computation-graph format. A model trained in one framework can run in a completely different runtime.

The workflow:

1. **Train** — in PyTorch, TensorFlow, scikit-learn, or XGBoost.
2. **Export** — convert to the `.onnx` graph.
3. **Optimize** — quantize, fuse ops, prune.
4. **Run anywhere** — C++, Java, edge devices.

Why it's worth it:

- **Framework independence** — train in PyTorch, serve with ONNX Runtime, no PyTorch in production.
- **Smaller production image** — drop the training frameworks.
- **Cross-language serving** — run the same file from C++ or JavaScript.
- **Hardware acceleration** — execution providers target CUDA, TensorRT, CoreML.

### Exporting a PyTorch Model

From trained weights to a portable graph.

```python
# export_onnx.py
import torch, onnx

model = RideDurationTorchModel()
model.eval()  # disable dropout / batchnorm

dummy = torch.randn(1, 2)  # shape only

torch.onnx.export(
    model, dummy, "model.onnx",
    export_params=True,
    opset_version=17,
    input_names=["features"],
    output_names=["duration"],
    dynamic_axes={
        "features": {0: "batch"},
        "duration": {0: "batch"},
    },
)

onnx.checker.check_model(onnx.load("model.onnx"))
```

> [!example]- Line by line: PyTorch to ONNX
> ```python
> model.eval()
> ```
> Switches off training-only behaviour (dropout, batch-norm running stats). Forget this and the exported model predicts slightly wrong numbers with no error.
>
> ```python
> dummy = torch.randn(1, 2)
> ```
> ONNX export works by **tracing**: PyTorch runs the model once on a fake input and records every operation. The values do not matter, only the shape `(1 row, 2 features)` and dtype.
>
> ```python
> torch.onnx.export(model, dummy, "model.onnx",
>     export_params=True,     # bake the trained weights into the file
>     opset_version=17,       # which ONNX "dialect" of operators to use
>     input_names=["features"], output_names=["duration"],   # readable names
>     dynamic_axes={"features": {0: "batch"}, "duration": {0: "batch"}})
> ```
> `dynamic_axes` says "dimension 0 can be any size". Without it the graph is frozen to exactly 1 row and batch inference fails.
>
> ```python
> onnx.checker.check_model(onnx.load("model.onnx"))
> ```
> Reloads the file and validates the graph. Catches a broken export before it reaches production.


- **`model.eval()`** — forgetting this leaves dropout in training mode → silently wrong predictions.
- **`dummy_input`** — only shape and dtype matter. PyTorch tracks the graph by running it once.
- **`dynamic_axes`** — without it the model is locked to batch size 1.
- **`onnx.checker`** — validate before shipping. A broken export fails silently in some runtimes.

### scikit-learn and Inference

Export, then run anywhere.

![[Pasted image 20260915182927.png]]

```python
# onnx_sklearn.py
from skl2onnx import to_onnx
from skl2onnx.common.data_types import FloatTensorType

sk_model = RideDurationModel()._model  # fitted
init_type = [("features", FloatTensorType([None, 2]))]
onnx_model = to_onnx(sk_model, initial_types=init_type)

with open("model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

# Run it
import onnxruntime as ort, numpy as np

sess = ort.InferenceSession("model.onnx")
name_in = sess.get_inputs()[0].name
name_out = sess.get_outputs()[0].name

batch = np.array([[5.0, 2]], dtype=np.float32)
out = sess.run([name_out], {name_in: batch})[0]
```

> [!example]- Line by line: scikit-learn to ONNX and running it
> ```python
> init_type = [("features", FloatTensorType([None, 2]))]
> onnx_model = to_onnx(sk_model, initial_types=init_type)
> ```
> sklearn cannot be traced like PyTorch, so `skl2onnx` needs you to declare the input: named `features`, float32, shape `[any rows, 2 columns]`. `None` is the dynamic batch dimension.
>
> ```python
> f.write(onnx_model.SerializeToString())
> ```
> The ONNX model is a Protobuf object. `SerializeToString()` turns it into bytes for the file.
>
> ```python
> sess = ort.InferenceSession("model.onnx")
> name_in = sess.get_inputs()[0].name
> name_out = sess.get_outputs()[0].name
> ```
> ONNX Runtime loads the file. Reading the input/output names from the session instead of hardcoding "features" means the code survives a rename.
>
> ```python
> batch = np.array([[5.0, 2]], dtype=np.float32)
> out = sess.run([name_out], {name_in: batch})[0]
> ```
> `run` takes "which outputs I want" and "a dict of input name -> array". The explicit `float32` matters: ONNX is strict about dtype, and numpy defaults to float64, which errors.


- **`skl2onnx`** — converts most sklearn estimators and Pipelines.
- **`providers`** — pick the backend: CPU, CUDA, TensorRT, or OpenVINO — same file.
- **`get_inputs`** — read names from the model. Never hardcode them.
- **Batch inference** — only works because `dynamic_axes` was set at export.

### What Converts, and How Well

![[Pasted image 20260915183111.png]]

| Source framework | Converter | Notes |
| --- | --- | --- |
| PyTorch | `torch.onnx` (built in) | Best supported — native export API |
| scikit-learn | `skl2onnx` | Covers most estimators and Pipelines |
| XGBoost / LightGBM | `onnxmltools` | Tree ensembles convert well |
| TensorFlow / Keras | `tf2onnx` | Some custom layers need manual ops |
| Hugging Face | `optimum.onnxruntime` | Transformers export with attention support |

> [!tip] The serving goal
> Low latency, high throughput, high concurrency.

## Docker

### Dockerfile Anatomy

Every line is a frozen decision.

![[Pasted image 20260915185425.png]]

```dockerfile
# Stage 1: build
FROM python:3.11-slim AS builder
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .[dev]

# Stage 2: runtime
FROM python:3.11-slim AS runtime
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11 \
     /usr/local/lib/python3.11
COPY src/ ./src/

RUN adduser --disabled-password appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0"]
```

> [!example]- Line by line: the Dockerfile
> ```dockerfile
> FROM python:3.11-slim AS builder
> WORKDIR /app
> COPY pyproject.toml .
> RUN pip install --no-cache-dir -e .[dev]
> ```
> Stage 1, named `builder`. Start from a small Python image, copy only the dependency file, install. `-e .[dev]` = editable install of this project plus its dev extras.
>
> **Layer caching:** Docker caches each line. If `pyproject.toml` did not change, the slow `pip install` line is reused from cache. That is why deps are copied *before* `src/`: code changes daily, deps change monthly.
>
> ```dockerfile
> FROM python:3.11-slim AS runtime
> COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
> COPY src/ ./src/
> ```
> Stage 2 starts fresh and copies only the installed packages from stage 1. Build tools, caches and compilers from stage 1 are thrown away. Smaller image, smaller attack surface.
>
> ```dockerfile
> RUN adduser --disabled-password appuser
> USER appuser
> ```
> Create a normal user and switch to it. If someone exploits the app, they are not root inside the container.
>
> ```dockerfile
> EXPOSE 8000
> CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0"]
> ```
> `EXPOSE` is documentation only. `CMD` is the default command: run uvicorn (the ASGI server) serving the `app` object in `src/api.py`. `0.0.0.0` means listen on all interfaces. Inside a container this is required, or nothing outside can reach it.


- **Multi-stage build** — builder installs everything, runtime copies only what runs. ~60% smaller.
- **Layer caching** — `COPY pyproject.toml` before `COPY src/`. Deps change rarely, code changes often.
- **Non-root user** — never run as root. If the app is exploited, damage is contained.
- **CMD vs ENTRYPOINT** — CMD is the default command. ENTRYPOINT is the fixed binary.

### docker-compose

Your API and MLflow, one command.

![[Pasted image 20260915185431.png]]

```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports: ["8000:8000"]
    environment:
      - MODEL_PATH=/models/v1/model.pkl
      - LOG_LEVEL=INFO
    volumes:
      - ./models:/models:ro
    depends_on: [mlflow]

  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.12.1
    ports: ["5000:5000"]
    volumes:
      - mlflow-data:/artifacts
```

> [!example]- Line by line: docker-compose
> Two containers run as one unit.
> - `build: .` builds the Dockerfile above.
> - `ports: ["8000:8000"]` is `host:container`. Your laptop's 8000 maps to the container's 8000.
> - `environment` injects config, so the same image runs with a different model path in staging vs prod.
> - `volumes: ./models:/models:ro` mounts your local `./models` folder into the container at `/models`, read-only.
> - `depends_on` only controls start *order*, not readiness. In production add a healthcheck so the API waits until MLflow actually answers.


- **Environment variables** — inject config at runtime. Never hardcode paths or secrets.
- **Read-only volumes** — `:ro` means the API can read models but not modify them.
- **`depends_on`** — API waits for MLflow. In production, add healthcheck conditions.
- **Daily commands** — `docker compose up -d`, `ps`, `logs -f api`.

## Logging

> [!warning] JSON logs are searchable. `print()` is not.
> Structured logs can be filtered, queried, and correlated. Print statements can't.

Bad — `print()`:

```python
print("Prediction made: 23.5")
print("ERROR: model not loaded")
```

Good — structlog:

```python
log.info("prediction.made", value=23.5,
         model_version="v1.2", latency_ms=4.1)
```

Configuring it:

```python
# src/logging.py
import structlog, logging

logging.basicConfig(format="%(message)s", level=logging.INFO)

structlog.configure(processors=[
    structlog.processors.add_log_level,
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.JSONRenderer(),
])

log = structlog.get_logger().bind(
    request_id=data.request_id,  # correlation ID
    endpoint="/predict",
)
log.info("predict.start", distance=data.distance_km)
```

> [!example]- Line by line: structlog
> ```python
> print("Prediction made: 23.5")
> ```
> Bad because it is a free-text string. Nothing downstream can ask "show me all predictions over 20 for model v1.2".
>
> ```python
> log.info("prediction.made", value=23.5, model_version="v1.2", latency_ms=4.1)
> ```
> Same event, but as key-value fields. Rendered as JSON, a log tool can filter and graph it.
>
> ```python
> structlog.configure(processors=[
>     structlog.processors.add_log_level,
>     structlog.processors.TimeStamper(fmt="iso"),
>     structlog.processors.JSONRenderer(),
> ])
> ```
> Processors are a pipeline every log line passes through: add the level, add an ISO timestamp, render as JSON.
>
> ```python
> log = structlog.get_logger().bind(request_id=data.request_id, endpoint="/predict")
> ```
> `bind` attaches fields to every later line from this logger. `request_id` is a **correlation ID**: one ID per request, so you can pull every log line for one user's call across services. See [[Observability]].


## Testing

### Unit Testing with pytest

> [!quote] Code that cannot be tested cannot be trusted.

![[Pasted image 20260915185449.png]]

```python
# tests/test_model.py
import pytest
from unittest.mock import MagicMock
from src.model import RideDurationModel


def test_predict_returns_float():
    model = RideDurationModel()
    model._model = MagicMock()
    model._model.predict.return_value = [23.5]
    assert model.predict([5.0, 1]) == 23.5


@pytest.mark.parametrize("dist, pax, expected", [
    (1.0, 1, 5.2), (10.0, 2, 24.8), (0.5, 4, 3.1),
])
def test_predict_inputs(dist, pax, expected):
    model = RideDurationModel()
    model._model = MagicMock()
    model._model.predict.return_value = [expected]
    assert model.predict([dist, pax]) == expected
```

> [!example]- Line by line: unit tests with mocks
> ```python
> model = RideDurationModel()
> model._model = MagicMock()
> model._model.predict.return_value = [23.5]
> assert model.predict([5.0, 1]) == 23.5
> ```
> The real model file may be huge or absent on CI. `MagicMock()` is a fake object that accepts any call. You tell it "when `.predict` is called, return `[23.5]`". Now the test checks *your* wrapper logic (the `[0]` indexing, the `min` cap) without touching real ML.
>
> ```python
> @pytest.mark.parametrize("dist, pax, expected", [(1.0, 1, 5.2), (10.0, 2, 24.8), ...])
> def test_predict_inputs(dist, pax, expected):
> ```
> Runs the same test body once per tuple. Three cases, one function. Pytest reports them as three separate tests. See [[Testing]].


- **`MagicMock`** — never call real ML code in unit tests.
- **`parametrize`** — one test function, many inputs.
- **Fixtures** — shared setup, injected by argument name.
- **Assert semantics** — pytest shows actual vs expected on failure.

### Testing the API

Full request cycle, no running server.

![[Pasted image 20260915185455.png]]

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


def test_predict_success():
    resp = client.post("/predict",
        json={"distance_km": 5.0, "passengers": 2})
    assert resp.status_code == 200
    assert "duration_min" in resp.json()


def test_predict_negative_distance():
    resp = client.post("/predict",
        json={"distance_km": -1.0, "passengers": 1})
    assert resp.status_code == 422  # Pydantic catches it
```

Run with coverage:

```bash
pytest --cov=src --cov-report=html
```

> [!example]- Line by line: API tests
> ```python
> client = TestClient(app)
> resp = client.post("/predict", json={"distance_km": 5.0, "passengers": 2})
> assert resp.status_code == 200
> ```
> `TestClient` calls your FastAPI app in-process: no server, no network. `json=` sends a JSON body.
>
> The second test sends `distance_km: -1.0` and asserts `422`, proving the Pydantic `gt=0` rule works. That is "test the contract": one happy path, one rejection path.
>
> ```bash
> pytest --cov=src --cov-report=html
> ```
> Runs the tests and measures which lines in `src/` were executed. Coverage says what *ran*, not whether it is *correct*.


- **`TestClient`** — no server needed; requests are processed in-process.
- **Test the contract** — the happy path and the rejection path, both.
- **Status codes** — 200 for success, 422 for a schema violation.

### What Good Coverage Looks Like

> [!info] Coverage measures test thoroughness, not correctness.

| Coverage | Meaning |
| --- | --- |
| **≥ 80%** | Minimum threshold for a CI gate |
| **≥ 90%** | Recommended for core business logic |
| **< 70%** | Red flag — what is not being tested? |
| **100%** | Achievable for schemas and pure functions |

> [!success] Course target
> At least 80% coverage across `src/`.

## How it all ties together

The note is one story. A model is a package (`src/`), behind a contract (`ModelBase`), exposed as a validated API (FastAPI + Pydantic), shipped as a small image (multi-stage Docker), configured from outside (env vars, compose), observable (structlog), and tested without the real model (mocks, `TestClient`). Every block is one link in that chain.

> [!warning] The one thing this note skips
> `async def predict` with a CPU-bound `model.predict` can stall the whole server, because async only helps while *waiting*, not while *computing*. That is the "Async Python + GIL" gap in [[Knowledge Gaps Audit 2026-09-15]].

## Resources

Where to go deeper.

| Resource | Link | Note |
| --- | --- | --- |
| FastAPI | fastapi.tiangolo.com/tutorial | The best framework docs I have read |
| pytest | docs.pytest.org | Fixtures, parametrize, marks |
| Pydantic v2 | docs.pydantic.dev | Field validators, model config, JSON schema |
| MLOps Zoomcamp | github.com/DataTalksClub/mlops-zoomcamp | The free 9-week course this aligns with |
| Docker | docs.docker.com/get-started | Official Getting Started series |
| structlog | structlog.org | The structured logging library used here |
| Made With ML | madewithml.com | End-to-end MLOps reference — free |
| TechWorld with Nana | youtube.com/@TechWorldwithNana | 3-hour Docker crash course |
