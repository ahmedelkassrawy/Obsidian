What Gets Automatically Generated
#### Performance Metrics
- 📊 **Classification**: Accuracy, precision, recall, F1-score, ROC-AUC, confusion matrices
- 📈 **Regression**: MAE, MSE, RMSE, R², residual analysis, prediction vs actual plots
- 🎯 **Custom Metrics**: Domain-specific measures defined with simple Python functions
#### Visual Diagnostics
- 📊 **Performance Plots**: ROC curves, precision-recall curves, calibration plots
- 📈 **Feature Importance**: SHAP values, permutation importance, feature interactions
#### Model Explanations
- 🧠 **Global Explanations**: Overall model behavior and feature contributions (with `shap`)
- 🔍 **Local Explanations**: Individual prediction explanations and decision paths (with `shap`)
```python
import mlflow
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_wine

# Load and prepare data
wine = load_wine()
X_train, X_test, y_train, y_test = train_test_split(
    wine.data, wine.target, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Create evaluation dataset
eval_data = X_test
eval_data["target"] = y_test

with mlflow.start_run():
    # Log model
    mlflow.sklearn.log_model(model, name="model")

    # Comprehensive evaluation with one line
    result = mlflow.models.evaluate(
        model="models:/my-model/1",
        data=eval_data,
        targets="target",
        model_type="classifier",
        evaluators=["default"],
    )
```

#### Func Evaluation
## Quick Start: Evaluating a Simple Function

The most straightforward function evaluation involves a callable that takes data and returns predictions:

```python
import mlflow
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Generate sample data
X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Train a model (we'll use this in our function)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


# Define a prediction function
def predict_function(input_data):
    """Custom prediction function that can include business logic."""

    # Get base model predictions
    base_predictions = model.predict(input_data)

    # Add custom business logic
    # Example: Override predictions for specific conditions
    feature_sum = input_data.sum(axis=1)
    high_feature_mask = feature_sum > feature_sum.quantile(0.9)

    # Custom rule: high feature sum values are always class 1
    final_predictions = base_predictions.copy()
    final_predictions[high_feature_mask] = 1

    return final_predictions


# Create evaluation dataset
eval_data = pd.DataFrame(X_test)
eval_data["target"] = y_test

with mlflow.start_run():
    # Evaluate function directly - no model logging needed!
    result = mlflow.evaluate(
        predict_function,  # Function to evaluate
        eval_data,  # Evaluation data
        targets="target",  # Target column
        model_type="classifier",  # Task type
    )

    print(f"Function Accuracy: {result.metrics['accuracy_score']:.3f}")
    print(f"Function F1 Score: {result.metrics['f1_score']:.3f}")
```

This approach is ideal when:

- You want to test functions quickly without model persistence
- Your prediction logic includes complex business rules
- You're prototyping custom algorithms or ensemble methods
- You need to evaluate preprocessing + prediction pipelines

## Best Practices

When using function evaluation, consider these best practices:

- **Stateless Functions**: Design functions to be stateless when possible to ensure reproducible results
- **Parameter Logging**: Always log function parameters and configuration for reproducibility
- **Input Validation**: Include input validation and error handling in production functions
- **Performance Monitoring**: Track execution time and resource usage for production functions
- **Version Control**: Use MLflow's tagging and naming conventions to track function versions

[Dataset Evaluation | MLflow](https://mlflow.org/docs/latest/ml/evaluation/dataset-eval/)
[Model Evaluation | MLflow](https://mlflow.org/docs/latest/ml/evaluation/model-eval/)