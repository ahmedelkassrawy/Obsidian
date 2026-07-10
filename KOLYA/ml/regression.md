## Step 1: The Hypothesis Function

The **hypothesis function** maps a given input $\mathbf{X}$ to a predicted $\mathbf{y}$. We must train this function, and we commonly call the predicted $\mathbf{y}$ as $\hat{\mathbf{y}}$ (read as y-hat) to differentiate it from the actual $\mathbf{y}$.

For linear regression, the hypothesis function is parameterized by $\theta$. It can be written in several forms:

**A. Expanded Form**

$$h_\theta(x^{(i)}) = \theta_0 + \theta_1x^{(i)}_1 + \theta_2x^{(i)}_2 + \cdots + \theta_nx^{(i)}_n$$

**B. Summation Form**

$$h_\theta(x^{(i)}) = \sum_{j=0}^n \theta_jx^{(i)}_j$$

**C. Vectorized Form** (where $\theta$ and $\mathbf{x}$ are both shape $n \times 1$)

$$h_\theta(x^{(i)}) = \boldsymbol{\theta}^T \mathbf{x}$$

**D. Matrix Form** (combines all samples; $\mathbf{X}$ is shape $m \times n$, $\theta$ is shape $n \times 1$)

$$\mathbf{h} = \mathbf{X}\boldsymbol{\theta}$$

> **Note:** Here, $\theta$ represents the parameters, weights, or coefficients. We generally prefer the Matrix form (D) because it is the easiest to implement in code. If a bias term $\theta_0$ exists, $\mathbf{X}$ will have a shape of $m \times (n+1)$, and $\theta$ will be $(n+1) \times 1$.

## Step 2: The Loss Function & Gradient Descent

To find the best parameters ($\theta$), we must define a **loss/objective function** (denoted as $J$) that measures how close our predictions $h(\mathbf{x}^{(i)})$ are to the actual $\mathbf{y}^{(i)}$:

$$J(\theta) = \frac{1}{2}\sum_{i=1}^m(h_\theta(x^{(i)}) - y^{(i)})^2$$

We use an optimization algorithm called **Gradient Descent** to minimize $J(\theta)$ by updating $\theta$ based on its derivatives (gradients).

We start with random values for $\theta$ and repeatedly perform this update simultaneously for all values of $j$:

$$\theta_j := \theta_j - \alpha * \frac{\partial J}{\partial \theta_j}$$

- $\alpha$ is the **learning rate**, typically a value between **0** and **1** (e.g., **0.001**). It is considered a hyperparameter.
    
- The partial derivative of the loss function with respect to $\theta_j$ evaluates to $(h_\theta(x) - y)x_j$ for a single example.
    

**Vectorized Update Rule (Batch Gradient Descent):**

To calculate the gradient using the entire training set at once, we use the following vectorized format:

$$\theta = \theta - \alpha * \mathbf{X}^\top (\mathbf{h} - \mathbf{y})$$

---

## Step 3: Implementing the Model from Scratch

Now, we translate the mathematical theory into a Python class using NumPy.
```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import datasets

class LinearRegression:
    def __init__(self, learning_rate=0.01, n_iters=1000):
        self.lr = learning_rate
        self.n_iters = n_iters
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for i in range(self.n_iters):
            # 1. Predict (Hypothesis Function)
            prediction = np.dot(X, self.weights) + self.bias

            # 2. Compute Gradients
            dw = (1/n_samples) * np.dot(X.T, (prediction - y))
            db = (1/n_samples) * np.sum(prediction - y)

            # 3. Step (Update weights)
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X):
        return np.dot(X, self.weights) + self.bias

def mean_squared_error(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)
```

## Step 4: Generating and Preparing Data

Before training, we need data. We use `sklearn.datasets` to generate a synthetic regression dataset and split it into training and testing sets.
```python
# Generate dummy regression data
X, y = datasets.make_regression(n_samples=100, n_features=1, noise=50, random_state=4)

# Split into 80% training and 20% testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1234)

print("Training data shape:", X_train.shape, y_train.shape)
print("Testing data shape:", X_test.shape, y_test.shape)
```

## Step 5: Training and Evaluating the Custom Model

We instantiate our custom model, train it on the training data, and evaluate its performance using Mean Squared Error (MSE).
```python
# Instantiate and train the model
regressor = LinearRegression(learning_rate=0.01, n_iters=1000)
regressor.fit(X_train, y_train)

# Make predictions on the test set
predictions = regressor.predict(X_test)

# Output learned parameters
print("Coefficient (w):", regressor.weights)
print("Intercept (b):", regressor.bias)

# Evaluate
mse = mean_squared_error(y_test, predictions)
print("MSE:", mse)

# Plot the results
y_pred_line = regressor.predict(X)
fig = plt.figure(figsize=(8, 6))
plt.scatter(X_train, y_train, color="red", s=10, label="Training data")
plt.scatter(X_test, y_test, color="blue", s=10, label="Testing data")
plt.plot(X, y_pred_line, color="black", linewidth=2, label="Prediction")
plt.legend()
plt.show()
```

## Step 6: Implementing Using Scikit-Learn

For real-world applications, we rarely write algorithms from scratch. Here is how you achieve the exact same workflow using `scikit-learn`'s built-in model.

```python
from sklearn.linear_model import LinearRegression as SklearnLinearRegression

# Instantiate and train the model
model = SklearnLinearRegression()
model.fit(X_train, y_train)

# Output learned parameters
print("Coefficient (w):", model.coef_)
print("Intercept (b):", model.intercept_)

# Predict and evaluate
pred = model.predict(X_test)
mse2 = mean_squared_error(y_test, pred)
print("Scikit-Learn MSE:", mse2)

# Plot the results
y_pred_line2 = model.predict(X)
fig = plt.figure(figsize=(8, 6))
plt.scatter(X_train, y_train, color="red", s=10)
plt.scatter(X_test, y_test, color="blue", s=10)
plt.plot(X, y_pred_line2, color="black", linewidth=2, label="Prediction")
plt.legend()
plt.show()
```

---
