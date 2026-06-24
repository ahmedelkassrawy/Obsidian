#### Step1.Setup
```python
import pandas as pd
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

import mlflow
from mlflow.models import infer_signature

# NOTE: review the links mentioned above for guidance on connecting to a managed tracking server, such as the Databricks Managed MLflow

mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")
```

#### Step2.Load training data and train a simple model
```python
# Load the Iris dataset
X, y = datasets.load_iris(return_X_y=True)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the model hyperparameters
params = {"solver": "lbfgs", "max_iter": 1000, "multi_class": "auto", "random_state": 8888}

# Train the model
lr = LogisticRegression(**params)
lr.fit(X_train, y_train)

# Predict on the test set
y_pred = lr.predict(X_test)

# Calculate accuracy as a target loss metric
accuracy = accuracy_score(y_test, y_pred)
```

#### Step3. Define MLflow Experiment
```python
mlflow.set_experiment("MLflow Quickstart")
```

#### Step4.Log the model, hyperparameters, and loss metrics to MLflow.
```python
# Start an MLflow run
with mlflow.start_run():
  # Log the hyperparameters
  mlflow.log_params(params)

  # Log the loss metric
  mlflow.log_metric("accuracy", accuracy)

  # Set a tag that we can use to remind ourselves what this run was for
  mlflow.set_tag("Training Info", "Basic LR model for iris data")

  # Infer the model signature
  signature = infer_signature(X_train, lr.predict(X_train))

  # Log the model
  model_info = mlflow.sklearn.log_model(
      sk_model=lr,
      name="iris_model",
      signature=signature,
      input_example=X_train,
      registered_model_name="tracking-quickstart",
  )
```

#### Step5. Load our saved model as a python func
```python
loaded_model = mlflow.pyfunc.load_model(model_info.model_uri)
```

#### Step6. Use our model to predict 
```python
predictions = loaded_model.predict(X_test)

iris_feature_names = datasets.load_iris().feature_names

# Convert X_test validation feature data to a Pandas DataFrame
result = pd.DataFrame(X_test, columns=iris_feature_names)

# Add the actual classes to the DataFrame
result["actual_class"] = y_test

# Add the model predictions to the DataFrame
result["predicted_class"] = predictions

result[:4]
```

-----------------------------
#### AutoLog
This will enable MLflow to automatically log various information about your run, including:

- **Metrics** - MLflow pre-selects a set of metrics to log, based on what model and library you use
- **Parameters** - hyper params specified for the training, plus default values provided by the library if not explicitly set
- **Model Signature** - logs [Model signature](https://mlflow.org/docs/latest/ml/model/signatures/) instance, which describes input and output schema of the model
- **Artifacts** - e.g. model checkpoints
- **Dataset** - dataset object used for training (if applicable), such as _tensorflow.data.Dataset_
### Step 2 - Insert `mlflow.autolog` in Your Code

For example, following code snippet shows how to enable autologging for a scikit-learn model:

```python
import mlflow

from sklearn.model_selection import train_test_split
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor

mlflow.autolog()

db = load_diabetes()
X_train, X_test, y_train, y_test = train_test_split(db.data, db.target)

rf = RandomForestRegressor(n_estimators=100, max_depth=6, max_features=3)
# MLflow triggers logging automatically upon model fitting
rf.fit(X_train, y_train)
```

### Step 3 - Execute Your Code

```python
python YOUR_ML_CODE.py
```

### Step 4 - View Your Results in the MLflow UI

Once your training job finishes, you can run following command to launch the MLflow UI:

```python
mlflow ui --port 8080
```

Then, navigate to [`http://localhost:8080`](http://localhost:8080/) in your browser to view the results.

## Enable / Disable Autologging for Specific Libraries

One common use case is to enable/disable autologging for a specific library. For example, if you train your model on PyTorch but use scikit-learn for data preprocessing, you may want to disable autologging for scikit-learn while keeping it enabled for PyTorch. You can achieve this by either (1) enable autologging only for PyTorch using PyTorch flavor (2) disable autologging for scikit-learn using its flavor with `disable=True`.

```python
import mlflow

# Option 1: Enable autologging only for PyTorch
mlflow.pytorch.autolog()

# Option 2: Disable autologging for scikit-learn, but enable it for other libraries
mlflow.sklearn.autolog(disable=True)
mlflow.autolog()
```

The following list covers the most popular libraries that support autologging within MLflow:

- [Keras/TensorFlow](https://mlflow.org/docs/latest/ml/tracking/autolog/#autolog-keras)
- [LightGBM](https://mlflow.org/docs/latest/ml/tracking/autolog/#autolog-lightgbm)
- [Paddle](https://mlflow.org/docs/latest/ml/tracking/autolog/#autolog-paddle)
- [PySpark](https://mlflow.org/docs/latest/ml/tracking/autolog/#autolog-pyspark)
- [PyTorch](https://mlflow.org/docs/latest/ml/tracking/autolog/#autolog-pytorch)
- [Scikit-learn](https://mlflow.org/docs/latest/ml/tracking/autolog/#autolog-sklearn)
- [Spark](https://mlflow.org/docs/latest/ml/tracking/autolog/#autolog-spark)
- [Statsmodels](https://mlflow.org/docs/latest/ml/tracking/autolog/#autolog-statsmodels)
- [XGBoost](https://mlflow.org/docs/latest/ml/tracking/autolog/#autolog-xgboost)
------ 
#### Tracking Server
## Start the Tracking Server

Starting the tracking server is as simple as running the following command:

```python
mlflow server --host 127.0.0.1 --port 8080
```

#### Logging to a Tracking Server
The [`mlflow.start_run()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.start_run), [`mlflow.log_param()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.log_param), and [`mlflow.log_metric()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.log_metric) calls then make API requests to your remote tracking server.
```python
import mlflow

remote_server_uri = "..."  # set to your server URI, e.g. http://127.0.0.1:8080
mlflow.set_tracking_uri(remote_server_uri)
mlflow.set_experiment("/my-experiment")
with mlflow.start_run():
    mlflow.log_param("a", 1)
    mlflow.log_metric("b", 2)
```

### Backend Store

By default, the tracking server logs runs metadata to the local filesystem under `./mlruns` directory. You can configure the different backend store by adding `--backend-store-uri` option.

### Remote artifacts store
#### Using the Tracking Server for proxied artifact access
By default, the tracking server stores artifacts in its local filesystem under `./mlartifacts` directory. To configure the tracking server to connect to remote storage and serve artifacts, start the server with `--artifacts-destination` flag.

```python
mlflow server --host 0.0.0.0  --port 8885 --artifacts-destination s3://my-bucket
```

With this setting, MLflow server works as a proxy for accessing remote artifacts. The MLflow clients make HTTP request to the server for fetching artifacts.

### Built-in Security Middleware
MLflow 3.5.0+ includes security middleware that automatically protects against common web vulnerabilities:
- **DNS Rebinding Protection**: Validates Host headers to prevent attacks on internal services
- **CORS Protection**: Controls which web applications can access your API
- **Clickjacking Prevention**: X-Frame-Options header controls iframe embedding
Configure these features with simple command-line options:

```python
mlflow server --host 0.0.0.0 \
  --allowed-hosts "mlflow.company.com" \
  --cors-allowed-origins "https://app.company.com"
```

### Authentication and Encryption

For production deployments, we recommend using a reverse proxy (NGINX, Apache httpd) or VPN to add:

- **TLS/HTTPS encryption** for secure communication
- **Authentication** via proxy authentication headers

You can pass authentication headers to MLflow using these environment variables:

- `MLFLOW_TRACKING_USERNAME` and `MLFLOW_TRACKING_PASSWORD` - username and password to use with HTTP Basic authentication. To use Basic authentication, you must set `both` environment variables.
- `MLFLOW_TRACKING_TOKEN` - token to use with HTTP Bearer authentication. Basic authentication takes precedence if set.
- `MLFLOW_TRACKING_INSECURE_TLS` - If set to the literal `true`, MLflow does not verify the TLS connection, meaning it does not validate certificates or hostnames for `https://` tracking URIs. This flag is not recommended for production environments. If this is set to `true` then `MLFLOW_TRACKING_SERVER_CERT_PATH` must not be set.
- `MLFLOW_TRACKING_SERVER_CERT_PATH` - Path to a CA bundle to use. Sets the `verify` param of the `requests.request` function (see [requests main interface](https://requests.readthedocs.io/en/master/api)). When you use a self-signed server certificate you can use this to verify it on client side. If this is set `MLFLOW_TRACKING_INSECURE_TLS` must not be set (false).
- `MLFLOW_TRACKING_CLIENT_CERT_PATH` - Path to ssl client cert file (.pem). Sets the `cert` param of the `requests.request` function (see [requests main interface](https://requests.readthedocs.io/en/master/api)). This can be used to use a (self-signed) client certificate.