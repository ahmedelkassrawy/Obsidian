# Linear Regression Notes

## Simple Linear Regression

Simple linear regression models the relationship between one independent variable and a dependent variable.

### Code Example: Simple Linear Regression with Radio Expenditure

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Create X from the radio column's values
X = sales_df["radio"].values
y = sales_df["sales"].values

# Reshape X to 2D array (required for sklearn)
X = X.reshape(-1,1)

# Check shapes
print(X.shape, y.shape)

# Create and fit the model
reg = LinearRegression()
reg.fit(X, y)

# Make predictions
predictions = reg.predict(X)

# Visualize
plt.scatter(X, y, color="blue")
plt.plot(X, predictions, color="red")
plt.xlabel("Radio Expenditure ($)")
plt.ylabel("Sales ($)")
plt.show()
```

## Multiple Linear Regression

Multiple linear regression uses multiple independent variables to predict a dependent variable. It can capture more complex relationships but risks overfitting with too many variables.

### Advantages Over Simple Linear Regression

- **Better explanatory power**: Incorporates multiple features, explaining more variance in the data (higher R²).
- **Handles complex relationships**: Captures interactions between variables.
- **Improved predictions**: More features can lead to better predictions, provided overfitting is managed.

### Risk of Overfitting

- **Too many variables**: Including irrelevant or highly correlated features can lead to overfitting, where the model fits noise rather than the true pattern.
- **Solutions**:
    - Use feature selection techniques (e.g., removing low-importance variables).
    - Apply regularization (e.g., Ridge or Lasso regression).
    - Perform cross-validation to assess model generalization.

### Handling Categorical Variables

To improve predictions, convert categorical independent variables into numerical formats:

- **One-hot encoding**: Create binary columns for each category (e.g., `pd.get_dummies()` in pandas).
- **Label encoding**: Assign integers to categories (useful for ordinal data).
- Example: If a dataset has a "region" column with values ["North", "South", "West"], one-hot encoding creates three binary columns.

### Code Example: Multiple Linear Regression

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Create X and y arrays
X = sales_df.drop("sales", axis=1).values  # All features except sales
y = sales_df["sales"].values

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create and fit the model
reg = LinearRegression()
reg.fit(X_train, y_train)

# Make predictions
y_pred = reg.predict(X_test)
print("Predictions: {}, Actual Values: {}".format(y_pred[:2], y_test[:2]))

# Evaluate model
r_squared = reg.score(X_test, y_test)
rmse = mean_squared_error(y_test, y_pred, squared=False)
print("R^2: {}".format(r_squared))
print("RMSE: {}".format(rmse))
```

### Metrics Explanation

- **R² (R-squared)**: Proportion of variance in the dependent variable explained by the model. Ranges from 0 to 1; higher is better.
- **RMSE (Root Mean Squared Error)**: Average magnitude of prediction errors in the same units as the dependent variable. Lower is better.

## Cross-Validation

Cross-validation assesses model performance on different subsets of data to ensure generalization.

### Code Example: Cross-Validation

```python
from sklearn.model_selection import cross_val_score, KFold
import numpy as np

# Create KFold object
kf = KFold(n_splits=6, shuffle=True, random_state=5)

# Create model
reg = LinearRegression()

# Compute 6-fold cross-validation scores
cv_scores = cross_val_score(reg, X, y, cv=kf)

# Print results
print("Cross-validation scores:", cv_scores)
print("Mean CV score:", np.mean(cv_scores))
print("Standard deviation:", np.std(cv_scores))
print("95% confidence interval:", np.quantile(cv_scores, [0.025, 0.975]))
```

### Key Points

- **Cross-validation scores**: Show model performance across different folds.
- **Mean and standard deviation**: Indicate average performance and variability.
- **Confidence interval**: Provides a range for expected model performance.