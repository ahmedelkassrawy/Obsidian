
---
## What are Regression Trees?

**Regression Trees** are decision trees designed to solve **regression problems**, where the target variable is **continuous** (e.g., house prices, temperatures). Unlike classification trees, which predict categorical labels (e.g., spam vs. not spam), regression trees predict numerical values.

### Key Differences

| **Task**           | **Target Type** | **Example**                       |
| ------------------ | --------------- | --------------------------------- |
| **Classification** | Categorical     | Predicting email as spam/not spam |
| **Regression**     | Continuous      | Predicting house price            |

> **Analogy**: A regression tree is like a flowchart that guides you to a number (e.g., a price) by asking questions about features (e.g., house size, location), with each final answer being the average of similar cases.

---

## How Regression Trees Work

Regression trees split the dataset into subsets based on feature values, creating a **tree-like structure**. Each leaf node represents a predicted value, calculated as the **average** of the target values for the data points in that node.

### Key Mechanics

1. **Splitting**:
    - The tree recursively splits the dataset into subsets to **maximize information gain** by reducing variance in the target variable.
    - **Splitting Criterion**: Choose features and thresholds that **minimize the error** between actual and predicted values (typically measured by variance reduction).
2. **Prediction**:
    - At each **leaf node**, the prediction is the **average value** of the target values for the data points in that node.
3. **Goal**:
    - Minimize the randomness (variance) of the target values within each split node, creating homogeneous subsets.

> [!tip] Variance Reduction  
> Regression trees select splits that reduce the variance of the target variable in each subset, ensuring predictions are as accurate as possible.
> reducing the variance -> overfitting potentials reduce

---

## Creating Regression Trees

The process of building a regression tree involves the following steps:

1. **Start with the full dataset**:
    - Consider all features and possible split points.
2. **Recursively split the data**:
    - Evaluate each feature and threshold to find the split that **maximizes variance reduction** (or minimizes error, e.g., mean squared error).
    - Split the data into two or more subsets based on the chosen feature and threshold.
3. **Build the tree structure**:
    - Continue splitting until a stopping criterion is met (e.g., maximum depth, minimum samples per node, or negligible variance reduction).
4. **Assign predictions**:
    - For each leaf node, compute the **average** of the target values for the data points in that node.
5. **Generate the final tree**:
    - The result is a tree-like structure where each path from root to leaf predicts a continuous value.

### Splitting Criterion

- **Objective**: Minimize the error between actual and predicted values.
- **Metric**: Variance reduction, often measured as the decrease in mean squared error (MSE) after a split.
> [!note] Stopping Criteria  
> To prevent overfitting, use regularization parameters like `max_depth`, `min_samples_split`, or `min_samples_leaf` (see DecisionTreeRegressor below).

---

## Code Example: Regression Tree with Scikit-Learn

Below is a practical example using scikit-learn’s `DecisionTreeRegressor` to build and evaluate a regression tree.

```python
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression
from sklearn.metrics import mean_squared_error

# Generate sample regression data
X, y = make_regression(n_samples=100, n_features=2, noise=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize and train regression tree
reg_tree = DecisionTreeRegressor(max_depth=5, min_samples_leaf=5, random_state=42)
reg_tree.fit(X_train, y_train)

# Predict and evaluate
y_pred = reg_tree.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")

# Example prediction
sample = X_test[:1]
print(f"Predicted value for sample: {reg_tree.predict(sample)[0]:.2f}")
```

### Output Example

```
Mean Squared Error: 150.45
Predicted value for sample: 42.78
```

---

## Practical Tips

1. **Prevent Overfitting**
    - Regularize with `max_depth`, `min_samples_split`, `min_samples_leaf`.
    - Example: `DecisionTreeRegressor(max_depth=5, min_samples_leaf=5)` limits tree complexity.
2. **Feature Selection**
    - Use feature importance scores (`reg_tree.feature_importances_`) to identify key predictors.
3. **Validation**
    - Use cross-validation or a test set to assess generalization.
4. **Ensemble Methods**
    - Combine regression trees in ensembles (e.g., Random Forest Regressor, Gradient Boosting) to reduce variance and improve accuracy.

```python
from sklearn.ensemble import RandomForestRegressor

# Random Forest for regression
rf_reg = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
rf_reg.fit(X_train, y_train)
print(f"Random Forest MSE: {mean_squared_error(y_test, rf_reg.predict(X_test)):.2f}")
```

---

## Summary

- **Regression Trees**: Decision trees adapted for **continuous target** prediction.
- **Splitting**: Uses **variance reduction** to minimize error between actual and predicted values.
- **Prediction**: Leaf nodes predict the **average** of target values.
- **Creation**: Recursively splits data to maximize information gain, forming a tree structure.
- **Regularization**: Use `max_depth`, `min_samples_leaf`, etc., to prevent overfitting.
