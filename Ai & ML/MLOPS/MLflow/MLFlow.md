# MLflow Guide for Experiment Tracking and Model Management

This guide covers key MLflow functionalities for experiment tracking, model logging, and evaluation, tailored for machine learning workflows in Python. It includes code snippets for experiment creation, logging, searching runs, model management, custom models, evaluation, and REST API usage.

## 1. Experiment Creation and Setup

### Create a New Experiment

```python
import mlflow

# Create a new experiment
mlflow.create_experiment("My Experiment")
```

### Set Experiment Tags

```python
# Tag the experiment
mlflow.set_experiment_tag("scikit-learn", "lr")
```

### Set Active Experiment

```python
# Set the experiment for tracking
mlflow.set_experiment("My Experiment")
```

## 2. MLflow Tracking

### Start and End a Run

```python
import mlflow

# Start a run
mlflow.start_run()

# End the run
mlflow.end_run()
```

### Logging Metrics and Parameters

```python
# Log a single metric
mlflow.log_metric("accuracy", 0.90)

# Log multiple metrics
mlflow.log_metrics({"accuracy": 0.90, "loss": 0.50})

# Log a single parameter
mlflow.log_param("n_jobs", 1)

# Log multiple parameters
mlflow.log_params({"n_jobs": 1, "fit_intercept": False})

# Log a single artifact (e.g., a file)
mlflow.log_artifact("file.py")

# Log all files in a directory
mlflow.log_artifacts("./directory/")
```

### Logging a Run Example

```python
import mlflow
from sklearn.linear_model import LogisticRegression

# Set experiment
mlflow.set_experiment("LR Experiment")

# Start a run
with mlflow.start_run():
    # Initialize and train model
    lr = LogisticRegression(n_jobs=1)
    lr.fit(X, y)
    score = lr.score(X, y)

    # Log metrics, parameters, and artifacts
    mlflow.log_metric("score", score)
    mlflow.log_param("n_jobs", 1)
    mlflow.log_artifact("train_code.py")
```

## 3. Searching Runs

### Basic Run Search

```python
# Search all runs in the current experiment
mlflow.search_runs()
```

### Filtered Run Search

```python
# Create a filter string for R-squared score
r_squared_filter = "metrics.r2_score > .70"

# Search runs across specific experiments
mlflow.search_runs(
    experiment_names=["Unicorn Sklearn Experiments", "Unicorn Other Experiments"],
    filter_string=r_squared_filter,
    order_by=["metrics.r2_score DESC"]
)
```

## 4. Model Flavors

### Autologging with Scikit-learn

```python
import mlflow
from sklearn.linear_model import LinearRegression

# Enable autologging for scikit-learn
mlflow.sklearn.autolog()

# Train model (automatically logs metrics and parameters)
lr = LinearRegression()
lr.fit(X, y)

# Retrieve model parameters
params = lr.get_params(deep=True)
print(params)
```

## 5. Model API Functions

### Saving and Loading Models

```python
# Save a model to a local path
mlflow.sklearn.save_model(model, path)

# Log a model to MLflow Tracking
mlflow.sklearn.log_model(model, artifact_path)

# Load a model from a URI
model = mlflow.sklearn.load_model(model_uri)
```

### Example: Logging and Loading a Model

```python
# Log a scikit-learn model
mlflow.sklearn.log_model(lr_model, "lr_tracking")

# Get the last active run
run = mlflow.last_active_run()

# Get the run ID
run_id = run.info.run_id

# Load model using run ID and artifact path
model = mlflow.sklearn.load_model(f"runs:/{run_id}/lr_tracking")
```

## 6. Custom Models

### Defining a Custom Model

```python
import mlflow.pyfunc

class Induced
class CustomPredict(mlflow.pyfunc.PythonModel):
    # Load artifacts
    def load_context(self, context):
        self.model = mlflow.sklearn.load_model(context.artifacts["custom_model"])

    def predict(self, context, model_input):
        prediction = self.model.predict(model_input)
        return custom_function(prediction)
```

### Saving and Logging Custom Models

```python
# Save custom model
mlflow.pyfunc.save_model(path="custom_model", python_model=CustomPredict())

# Log custom model
mlflow.pyfunc.log_model(artifact_path="custom_model", python_model=CustomPredict())
```

## 7. Model Evaluation

### Evaluating a Model

```python
# Evaluate a model using MLflow
mlflow.evaluate(
    "runs:/run_id/model",
    eval_data,
    targets="test_label",
    model_type="regressor"
)
```

## 8. Example: Logging a Random Forest Model

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import mlflow

# Split data
X = data.drop(columns=["date", "demand"])
y = data["demand"]
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Model parameters
params = {
    "n_estimators": 100,
    "max_depth": 6,
    "min_samples_split": 10,
    "min_samples_leaf": 4,
    "bootstrap": True,
    "oob_score": False,
    "random_state": 888,
}

# Train model
rf = RandomForestRegressor(**params)
rf.fit(X_train, y_train)

# Predict and calculate metrics
y_pred = rf.predict(X_val)
mae = mean_absolute_error(y_val, y_pred)
mse = mean_squared_error(y_val, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_val, y_pred)

# Log to MLflow
metrics = {"mae": mae, "mse": mse, "rmse": rmse, "r2": r2}
with mlflow.start_run(run_name="rf_run"):
    mlflow.log_params(params)
    mlflow.log_metrics(metrics)
    mlflow.sklearn.log_model(sk_model=rf, input_example=X_val, artifact_path="rf_model")
```

## 9. MLflow REST API

The MLflow REST API provides endpoints for various functionalities:

- `/ping`: Health check
- `/health`: Health check
- `/version`: Get MLflow version
- `/invocations`: Model scoring

## Notes

- **Autologging**: Use `mlflow.sklearn.autolog()` for automatic logging of scikit-learn models, metrics, and parameters.
- **Artifacts**: Log scripts, configurations, or datasets as artifacts to track associated files.
- **Custom Models**: Extend MLflow with custom Python models for specialized prediction logic.
- **Evaluation**: Use `mlflow.evaluate` for automated model performance analysis.
- **Colab Setup**: Ensure MLflow is installed (`!pip install mlflow`) and configure a tracking server if needed (local or remote).

This guide provides a comprehensive overview of MLflow for tracking, managing, and evaluating machine learning experiments, particularly for scikit-learn models.