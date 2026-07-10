Here is a structured Markdown study guide based on the provided code and concepts.

# Study Guide: Linear Regression - The Closed Form (Normal Equation)

This guide covers the theoretical foundation and practical implementation of the closed form (normal equation) approach to linear regression.

## 1. Theoretical Background

Gradient descent is an iterative approach to minimizing the cost function $J$, but it can take time. If we know our cost function is strictly convex or concave, we can explicitly set its derivative to zero. This mathematical derivation is known as obtaining the **normal equations** or **closed form**.

### The Normal Equation Formula

By performing matrix multiplication and inverse operations, we can solve for the optimal parameters ($\boldsymbol{\theta}$) directly:

$$\boldsymbol{\theta} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$$

### When to Use (and When Not To)

- **Advantages:** It is usually faster than gradient descent when a closed form is available, doable, and the matrix can be inversed.
    
- **Disadvantages:** It does not always exist, such as when the cost function is not convex or concave. Additionally, taking the inverse of a matrix with a huge number of features is computationally expensive, making it slow in high-dimensional spaces.
    

---

## 2. Implementation Workflow

Implementing the closed form involves a specific sequence of steps:

1. **Prepare your data:** Add an intercept, ensure matrices are the correct shape, split data, scale features, and clean missing values.
    
2. **Calculate $\boldsymbol{\theta}$:** Plug the training data into the normal equation.
    
3. **Predict $\mathbf{\hat{y}}$:** Perform a dot product between the calculated $\boldsymbol{\theta}$ and the test features.
    
4. **Evaluate:** Calculate the Mean Squared Error (MSE).
    

---

## 3. Step-by-Step Code Walkthrough

### Step 3.1: Load and Inspect Data

First, we load the dataset and verify the shapes of our feature matrix ($\mathbf{X}$) and target vector ($\mathbf{y}$).

```python
from sklearn.datasets import load_diabetes

diabetes = load_diabetes()
X = diabetes.data
y = diabetes.target

m = X.shape[0]  # number of samples
n = X.shape[1]  # number of features

# Ensure the number of samples matches the number of targets
assert m == y.shape[0]
```

### Step 3.2: Train-Test Split

We split the data to evaluate the model on unseen examples. A common practical rule for splitting is:

- < 10k samples $\rightarrow$ 20–30% test
    
- 10k–100k samples $\rightarrow$ 20% test
    
- 100k samples $\rightarrow$ 10% test
    

Python

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)
```

### Step 3.3: Feature Scaling

Standardizing data so that the mean is 0 and the variance is 1 helps algorithms converge faster by keeping values and gradients within a limited range.

> **Important:** Always split the data _before_ scaling to prevent data leakage.

Python

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
```

### Step 3.4: Add Intercept

We must append a column of ones to $\mathbf{X}$ to account for the intercept (bias) term in our equation. This changes the shape of $\mathbf{X}$ to $(m, n+1)$ and $\boldsymbol{\theta}$ to $(n+1, 1)$.

Python

```python
import numpy as np

# Add intercepts to training data
intercept_train = np.ones((X_train.shape[0], 1))
X_train = np.concatenate((intercept_train, X_train), axis=1)

# Add intercepts to test data
intercept_test = np.ones((X_test.shape[0], 1))
X_test = np.concatenate((intercept_test, X_test), axis=1)
```

### Step 3.5: Define and Fit the Algorithm

We use `numpy.linalg.inv` to translate the mathematical formula into code and apply it to our training data to find our model parameters ($\boldsymbol{\theta}$).

Python

```python
from numpy.linalg import inv

def closed_form(X, y):
    return inv(X.T @ X) @ X.T @ y

# Calculate theta (this is our trained model)
theta = closed_form(X_train, y_train)
```

### Step 3.6: Predict and Evaluate

Finally, we generate predictions ($\mathbf{\hat{y}}$) by computing the dot product of the test features and $\boldsymbol{\theta}$, then evaluate the model using Mean Squared Error (MSE). Note that this MSE uses $\frac{1}{m}$ instead of the $\frac{1}{2}$ found in the mathematical cost function $J(\boldsymbol{\theta})$.

Python

```python
# Predict yhat
yhat = X_test @ theta

# Ensure shapes match before comparison
assert y_test.shape == yhat.shape

# Calculate Mean Squared Error
mse = ((y_test - yhat)**2).sum() / X_test.shape[0]
print("Mean squared errors: ", mse)
```

---

Would you like to try calculating the closed form manually on a tiny, 3-row dataset to see how the matrix math works under the hood?