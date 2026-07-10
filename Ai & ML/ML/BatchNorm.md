## Batch Normalization vs Layer Normalization

So far, we learned how batch and layer normalization work. Let’s summarize the key differences between the two techniques.

- Batch normalization normalizes each feature independently across the mini-batch. 
- Layer normalization normalizes each of the inputs in the batch independently across all features.

- As batch normalization is dependent on batch size, it’s not effective for small batch sizes. 
- Layer normalization is independent of the batch size, so it can be applied to batches with smaller sizes as well.

- Batch normalization requires different processing at training and inference times. 
- As layer normalization is done along the length of input to a specific layer, the same set of operations can be used at both training and inference times.

#### **Definition**
**Batch Normalization** is a technique that **normalizes the activations (outputs) of a layer** for each mini-batch during training.

In simple terms:
> It keeps the **inputs to each layer** in a neural network **well-behaved** (not too large or too small), so the network trains faster and more reliably.
---
## ⚙️ **Why It’s Needed**
When training deep neural networks:
- Values flowing through layers can **explode** (become too large) or **vanish** (become too small).
- This makes training **unstable** or **slow**.
- BatchNorm **fixes this** by rescaling values to have a stable mean and variance.
---
## 🚀 **Benefits**

✅ Faster convergence (you can use higher learning rates)  
✅ Helps prevent vanishing/exploding gradients  
✅ Acts as a mild regularizer (reduces overfitting slightly)  
✅ Stabilizes training — especially for deep networks

---
## 💻 **Code Example (PyTorch)**

```python
import torch
import torch.nn as nn

# Example CNN layer with Batch Normalization
model = nn.Sequential(
    nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1),
    nn.BatchNorm2d(64),   # Normalize 64 feature maps
    nn.ReLU(),
    nn.MaxPool2d(2)
)
```

For fully connected (dense) layers, you’d use `nn.BatchNorm1d(num_features)` instead.

---
## 🧩 **Where It Fits**

BatchNorm is usually placed:
- **After a linear or convolutional layer**
- **Before** the activation function (like ReLU)
Example:  
`Linear → BatchNorm → ReLU`

---
## ⚠️ **Notes**
- During **training**, BatchNorm uses **batch statistics** (mean, variance).
- During **inference**, it uses **running averages** collected during training.
- If your **batch size is very small**, BatchNorm may perform poorly — you can use **LayerNorm** or **GroupNorm** instead.
---
