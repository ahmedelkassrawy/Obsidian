Summarizes the typical architecture of a regression MLP.
![[Pasted image 20250928140045.png]]

summarizes the typical architecture of a classification MLP
![[Pasted image 20250928140114.png]]
# 🔹 Loss Functions

Loss functions measure how well your model predictions match the target labels. Choice depends on **task type** and **label format**.

---
## 1️⃣ **Regression Losses**

- **Mean Squared Error (MSE)**
    - Formula: ( \frac{1}{n}\sum (y - \hat{y})^2 )
    - Penalizes large errors more heavily.
    - **Use case**: Predicting continuous values (house prices, stock values).
        
- **Mean Absolute Error (MAE)**
    - Formula: ( \frac{1}{n}\sum |y - \hat{y}| )
    - More robust to outliers than MSE.
    - **Use case**: When outliers exist or robustness is needed.
        
- **Huber Loss**
    - Combines MSE (for small errors) and MAE (for large errors).
    - **Use case**: Regression with outliers.
        
👉 **Most common in regression**: MSE or MAE.

---

## 2️⃣ **Classification Losses**

### 🔹 Binary Classification (2 classes)

- **Binary Crossentropy (Log Loss)**
    - Activation: **Sigmoid** in output.
    - Target format: `0` or `1`.
    - **Use case**: Spam detection, yes/no tasks.
### 🔹 Multiclass Classification (more than 2 classes)

- **Categorical Crossentropy**
    - Activation: **Softmax** in output.
    - Target format: **One-hot vectors** (e.g., [0,0,1,0,0]).
    - **Use case**: Digit classification (MNIST), object classification.
        
- **Sparse Categorical Crossentropy**
    - Activation: **Softmax** in output.
    - Target format: **Integer class labels** (e.g., `2` instead of [0,0,1,0,0]).
    - **Use case**: Same as categorical crossentropy, but labels are not one-hot encoded.
### 🔹 Multilabel Classification (each instance can belong to multiple classes)

- **Binary Crossentropy** (applied per label)
    - Activation: **Sigmoid** (one per class).
    - Target format: binary vector per sample (e.g., [1,0,1,0]).
    - **Use case**: Tagging images with multiple labels (dog + car).

👉 **Most common in classification**:

- Binary → Binary Crossentropy + Sigmoid.
- Multiclass → Categorical/Sparse Crossentropy + Softmax.
- Multilabel → Binary Crossentropy + Sigmoid (per class).
---

# 🔹 Optimizers

Optimizers update model weights based on gradients. Different optimizers balance speed, stability, and generalization.

---
## 1️⃣ **Basic Optimizers**

- **SGD (Stochastic Gradient Descent)**
    - Formula: ( w \leftarrow w - \eta \cdot \nabla L )
    - Key hyperparameter: **learning rate (η)**.
    - Often used with **momentum** to escape local minima.
    - **Use case**: Baseline, still popular in CV (ResNet, etc.) with momentum.

---
## 2️⃣ **Adaptive Optimizers**

- **Adam (Adaptive Moment Estimation)**
    - Combines momentum + RMSProp (keeps track of past gradients + adaptive learning rate).
    - Usually converges faster, less tuning needed.
    - **Use case**: NLP, CV, general deep learning.
    - Default choice in many frameworks.
        
- **RMSProp**
    - Keeps exponentially decaying average of squared gradients → adaptive learning rates.
    - Good for RNNs.
    - **Use case**: Time-series, recurrent models.
        
- **Adagrad**
    - Adapts learning rate per parameter → good for sparse features.
    - Downsides: learning rate can shrink too much over time.
    - **Use case**: NLP with sparse embeddings (historically).
---
## 3️⃣ **Variants & Advanced**

- **AdamW**
    - Adam + decoupled weight decay (regularization).
    - More stable than Adam for large models.
    - **Use case**: Transformers, LLMs, CV.
- **Nadam**
    - Adam + Nesterov momentum.
    - Sometimes improves convergence.

---
# 🔑 Common Choices in Practice

|Task|Output Activation|Loss|Optimizer|
|---|---|---|---|
|Regression|Linear|MSE / MAE|Adam / SGD (tuned LR)|
|Binary classification|Sigmoid|Binary Crossentropy|Adam (default) / SGD|
|Multiclass classification|Softmax|Categorical / Sparse Crossentropy|Adam / SGD|
|Multilabel classification|Sigmoid (per class)|Binary Crossentropy|Adam|
|Large deep nets (CV, NLP)|Depends|Crossentropy variant|AdamW (state of the art)|

---
⚡ **Rules of thumb**:
- **Start with Adam** (fast convergence, less tuning).
- If training unstable → tune learning rate or try AdamW.
- For research benchmarks (CV, ResNets) → often SGD + momentum works best.
- For regression → MSE or MAE with Adam usually fine.
---
# 🔹 How to Choose Number of Layers and Neurons

There’s no strict formula—it’s more **heuristics + experimentation**. But here are guidelines:

---

## 1️⃣ Input & Output Layers

- **Input neurons** = number of features.
    - Example: MNIST → 28×28 pixels = 784 inputs.
- **Output neurons** = depends on the task.
    - Regression → 1 (linear activation).
    - Binary classification → 1 (sigmoid).
    - Multiclass classification → `k` classes (softmax).
---
## 2️⃣ Hidden Layers

- **Shallow networks (1–2 hidden layers)**:
    - Work well for simple tasks (linear-ish decision boundaries).
- **Deep networks (3–10+ hidden layers)**:
    - Better for complex data like images, speech, NLP.
- **Rule of thumb**: Start small → add depth until validation error stops improving.

👉 More **layers** usually gives more representational power than just making each layer huge.

---
## 3️⃣ Neurons per Layer

- **Too few neurons** → bottleneck, information lost.
- **Too many neurons** → overfitting, slower training.
- Common strategies:
    - **Same size in all hidden layers** (e.g., 128, 128, 128).
    - **Slight pyramid** (e.g., 512 → 256 → 128).
    - **First hidden layer larger** than later ones.
- **Heuristic starting points**:
    - Small datasets (like MNIST): 100–500 neurons per layer.
    - Medium: 128–1024 neurons.
    - Large-scale (images, text): CNNs/Transformers, not just MLPs.
---

## 4️⃣ Regularization with Big Networks

Instead of trying to perfectly size the network:
- Use a **larger network** than needed.
- Apply:
    - **Early stopping**
    - **Dropout**
    - **Weight decay (L2 regularization)**

👉 This is the **“stretch pants” approach** from Vincent Vanhoucke.

---
# 🔹 Example in Code (Keras / TensorFlow)

Let’s use MNIST as an example.

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
x_train = x_train.reshape(-1, 28*28).astype("float32") / 255.0
x_test = x_test.reshape(-1, 28*28).astype("float32") / 255.0

# Example: 3 hidden layers, same neurons per layer
model = keras.Sequential([
    layers.Input(shape=(784,)),          # input layer = 784 features
    layers.Dense(256, activation="relu"), # hidden layer 1
    layers.Dense(256, activation="relu"), # hidden layer 2
    layers.Dense(256, activation="relu"), # hidden layer 3
    layers.Dense(10, activation="softmax") # output layer = 10 classes
])

# Compile
model.compile(
    optimizer=keras.optimizers.Adam(),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Train
model.fit(x_train, y_train, epochs=10, batch_size=64, validation_split=0.1)

# Evaluate
test_loss, test_acc = model.evaluate(x_test, y_test)
print("Test accuracy:", test_acc)
```

---
# 🔑 Key Takeaways

- Input/output layers are fixed by your problem.
- Hidden layers = 1–5 for most MLPs, more for very complex tasks.
- Neurons per layer = start with 128–512, scale up if needed.
- Bigger networks → control overfitting with regularization.
- Always tune with validation performance, not just training.
---
