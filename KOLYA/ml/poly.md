Here is the step-by-step Markdown study guide for your Polynomial Regression code. This guide contrasts a standard linear model with a polynomial model to show how the latter captures non-linear relationships in data.

# Study Guide: Polynomial Regression

This guide demonstrates how to implement and compare Linear Regression and Polynomial Regression models using `scikit-learn`.

## Step 1: Importing Libraries and the Dataset

First, we import the necessary scientific computing libraries and load our dataset using pandas. In this case, we extract the feature matrix $X$ (ignoring the first column, usually categorical/text like "Position") and the target vector $y$ ("Salary").

```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load the dataset (Make sure the path matches your environment)
dataset = pd.read_csv('/content/drive/MyDrive/Tanta - Spring 2026/ML Spring 2026/Section 4/Position_Salaries.csv')

# View the first few rows to understand the structure
dataset.head()

# Extract features (X) and target (y)
# X takes all rows, and columns from index 1 up to (but excluding) the last one
X = dataset.iloc[:, 1:-1].values

# y takes all rows, and only the last column
y = dataset.iloc[:, -1].values

```

## Step 2: Training the Linear Regression Model

As a baseline, we train a standard Linear Regression model on the entire dataset. This will attempt to fit a straight line through our data points.

```python
from sklearn.linear_model import LinearRegression

lin_reg = LinearRegression()
lin_reg.fit(X, y)

```

## Step 3: Training the Polynomial Regression Model

To capture curves in the data, we use `PolynomialFeatures` to transform our original feature matrix $X$ into a new matrix $X\_poly$ containing the original features raised to higher powers (up to a specified degree). We then fit a new Linear Regression model to this transformed data.

```python
from sklearn.preprocessing import PolynomialFeatures

# Create polynomial features up to degree 4
poly_reg = PolynomialFeatures(degree = 4)
X_poly = poly_reg.fit_transform(X)

# Train a new linear regression model on the polynomial features
lin_reg_2 = LinearRegression()
lin_reg_2.fit(X_poly, y)

# You can print X_poly to see the transformed features (x^0, x^1, x^2, x^3, x^4)
# print(X_poly)

```

## Step 4: Visualizing the Results

Visualizing both models helps us immediately see the difference in how they fit the training data.

### 4.1 Visualizing Linear Regression

This will plot the real data points in red and the model's straight-line predictions in blue.

```python
plt.scatter(X, y, color = 'red')
plt.plot(X, lin_reg.predict(X), color = 'blue')
plt.title('Truth or Bluff (Linear Regression)')
plt.xlabel('Position Level')
plt.ylabel('Salary')
plt.show()

```

### 4.2 Visualizing Polynomial Regression (Standard & High Resolution)

Because the polynomial model predicts a curve, we can use an advanced technique to make the plotted curve smoother. We create a denser grid of $X$ values (e.g., stepping by **0.1**) to generate a continuous-looking line.

```python
# Create a high-resolution grid of X values for a smoother curve
X_grid = np.arange(min(X), max(X) + 0.1, 0.1)
X_grid = X_grid.reshape((len(X_grid), 1))

plt.scatter(X, y, color = 'red')

# Predict using the polynomial regression model on the high-res grid
plt.plot(X_grid, lin_reg_2.predict(poly_reg.fit_transform(X_grid)), color = 'blue')

plt.title('Truth or Bluff (Polynomial Regression)')
plt.xlabel('Position level')
plt.ylabel('Salary')
plt.show()

```

## Step 5: Predicting a New Result

Finally, we test our models by predicting the salary for a specific position level (e.g., level **6.5**). Notice how the polynomial prediction requires the exact same `fit_transform` step applied to the input.

```python
# Predicting with the simple Linear Regression model
print("Linear Prediction:", lin_reg.predict([[6.5]]))

# Predicting with the Polynomial Regression model
# The input must first be transformed into polynomial features!
print("Polynomial Prediction:", lin_reg_2.predict(poly_reg.fit_transform([[6.5]])))

```

---

Would you like me to explain how tweaking the `degree` parameter (e.g., changing it from 4 to 2 or 10) affects the model's performance and the risk of overfitting?