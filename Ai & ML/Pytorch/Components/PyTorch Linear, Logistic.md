
## Training a Linear Model with Gradient Descent

### Loss Function

The loss for linear regression is Mean Squared Error (MSE):
### Model Setup

```python
# Define linear model: 2 inputs, 1 output (bias included)
linear = nn.Linear(2, 1)

# Define loss function: MSE
loss_function = nn.MSELoss()

# Define optimizer: Stochastic Gradient Descent (SGD) with learning rate 0.1
optimizer = torch.optim.SGD(linear.parameters(), lr=0.1)
```

### Training Loop

Train the model for 100 epochs, tracking loss and test accuracy.

```python
# Number of epochs
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

# Assuming X_train (shape: [N, 2]) and y_train (shape: [N, 1]) are defined tensors
# Example: X_train = torch.randn(100, 2), y_train = torch.randn(100, 1)

# Model, loss function, and optimizer
model = nn.Linear(2, 1)  # 2 inputs, 1 output
loss_fn = nn.MSELoss()   # Mean squared error loss
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)  # SGD optimizer

# Training setup
epochs = 100
loss_log = []
batch_size = 32

# Create DataLoader for batch processing
train_dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# Training loop
for epoch in range(epochs):
    model.train()  # Set model to training mode
    epoch_loss = 0.0

    # Iterate over batches
    for batch_X, batch_y in train_loader:
        # Forward pass
        y_pred = model(batch_X)  # Pass input data to model
        loss = loss_fn(y_pred, batch_y)  # Compute MSE loss

        # Backward pass and optimization
        optimizer.zero_grad()  # Clear previous gradients
        loss.backward()       # Compute gradients
        optimizer.step()      # Update model parameters

        # Track loss
        epoch_loss += loss.item()

    # Average loss for the epoch
    avg_loss = epoch_loss / len(train_loader)
    loss_log.append(avg_loss)

    # Print progress
    print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.6f}")
```

### Visualizing Training Progress

Plot accuracy and loss over epochs.

```python
# Plot accuracy
plt.plot(acc)
plt.title("Model accuracy per iteration")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
```

```python
# Plot loss
plt.plot(loss_log)
plt.title("Model loss per iteration")
plt.xlabel("Epoch")
plt.ylabel("MSE Loss")
```

---

## Logistic Regression

Linear regression with MSE is suboptimal for binary classification because it penalizes correct predictions far from the decision boundary. Logistic regression addresses this by:

- Using a **sigmoid function** to map outputs to ([0, 1]).
- Optimizing with **Binary Cross-Entropy (BCE) loss** to maximize the distance between classes.

### Sigmoid Function

The sigmoid function maps real numbers to ([0, 1]):


![Sigmoid Curve](https://upload.wikimedia.org/wikipedia/commons/8/88/Logistic-curve.svg)

- **Goal**: Push positive class predictions toward (+\infty) (sigmoid → 1) and negative class predictions toward (-\infty) (sigmoid → 0).
- **Issue with MSE**: The sigmoid’s flat gradients for large inputs slow down training with MSE loss.

### Cross-Entropy Loss

Use BCE loss for logistic regression:
- This loss models the output as a probability distribution, optimizing for classification.

**Note**: The model remains linear (only the loss and output activation differ).

### Logistic Regression Model Setup

```python
# Define linear model: 2 inputs, 1 output (bias included)
logistic_linear = nn.Linear(2, 1)

# Define loss function: BCE with logits (combines sigmoid and BCE)
loss_function = nn.BCEWithLogitsLoss()

# Define optimizer: SGD with learning rate 0.1
logistic_optimizer = torch.optim.SGD(logistic_linear.parameters(), lr=0.1)
```

### Training Loop

Train the logistic regression model for 100 epochs.

```python
# Number of epochs
max_epoch = 100

logistic_loss_log = []  # Track loss values
logistic_acc = []       # Track test accuracy
for epoch in range(max_epoch):
    # Test set accuracy (no gradient computation)
    with torch.no_grad():
        y_test_hat = logistic_linear(x_test)
        class_pred = (torch.sigmoid(y_test_hat) > 0.5).float()
        logistic_acc.append((class_pred.eq(y_test).float().mean().item()))

    # Training step
    y_train_hat = logistic_linear(x_train)  # Forward pass
    loss = loss_function(y_train_hat, y_train)  # Compute loss
    logistic_optimizer.zero_grad()  # Zero gradients
    loss.backward()  # Backpropagation
    logistic_optimizer.step()  # Update parameters
    logistic_loss_log.append(loss.item())  # Log loss
    
print("Accuracy of logistic model (GD): %.2f%% " % (logistic_acc[-1] * 100))
```

### Visualizing Training Progress

Plot accuracy and loss for the logistic model.

```python
# Plot accuracy
plt.plot(logistic_acc)
plt.title("Model accuracy per iteration")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
```

```python
# Plot loss
plt.plot(logistic_loss_log)
plt.title("Model loss per iteration")
plt.xlabel("Epoch")
plt.ylabel("BCE Loss")
```

---
