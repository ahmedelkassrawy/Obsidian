## Overview
- **Autoencoders**: Unsupervised neural networks that learn **dense latent representations** (codings) of input data.
  - Lower dimensionality than input → useful for **dimensionality reduction** (esp. visualization).
  - Act as **feature detectors**.
  - Used for **unsupervised pretraining** of deep networks.
  - Useful for **anomaly detection**.
  - Some are **generative models** (can generate new data similar to training data, e.g., faces).

- **GANs (Generative Adversarial Networks)**:
  - Generate highly convincing data
  - Applications: super resolution, colorization, image editing, sketch-to-photo, video frame prediction, data augmentation, text/audio/time series generation, identifying model weaknesses.
  - Largely replaced by **diffusion models** since early 2020s:
    - Diffusion models produce **more diverse and higher-quality images**.
    - Easier to train.
    - Much slower → GANs still used when **fast generation** is needed.

- **Common traits** (Autoencoders, GANs, Diffusion models):
  - Unsupervised.
  - Learn latent representations.
  - Can be generative models.
  - Overlap in applications.
  - Work very differently.

## Key Differences

| Model             | Core Mechanism                                                                 | Training Constraint/Approach                          | Generative Capability                          |
|-------------------|--------------------------------------------------------------------------------|------------------------------------------------------|------------------------------------------------|
| **Autoencoders**  | Learn to copy inputs to outputs (identity function) under constraints          | Constraints (e.g., small latent space, noise) force efficient representations | Yes (some variants)                            |
| **GANs**          | Two networks: Generator (produces fake data) vs. Discriminator (detects fake)  | Adversarial training (generator vs. discriminator)   | Yes (high-quality, fast)                       |
| **Diffusion**     | Gradually remove noise from noisy images                                       | Trained on denoising; generation starts from pure noise | Yes (highest quality/diversity, slow)          |

## Efficient Data Representations

### Memorization Example
- Sequence 1: 40, 27, 25, 36, 81, 57, 10, 73, 19, 68 (short but no pattern)
- Sequence 2: 50, 48, 46, ..., 14 (long but clear pattern: decreasing even numbers from 50 to 14)

**Insight**: Pattern recognition makes long sequences easier to remember despite length.  
→ Constraining memory forces discovery of efficient representations (patterns).


**Analogy to Autoencoders**:
- Autoencoder observes inputs → converts to efficient latent representation → reconstructs inputs.
- Constraints force learning of important patterns/features.

## Autoencoder Architecture

- Always composed of two parts:
  1. **Encoder** (recognition network): input → latent representation (coding)
  2. **Decoder** (generative network): latent representation → output (reconstruction)

- Example (simple MLP):
  - Input: 3 dimensions
  - Encoder: reduces to 2D latent space
  - Decoder: reconstructs back to 3D output
  - Output layer size = input size

- **Outputs** = **Reconstructions**
- **Cost function**: Includes **reconstruction loss** (penalizes differences between input and reconstruction)

### Undercomplete Autoencoders
- Latent space dimensionality < input dimensionality
- Cannot trivially copy input → output
- Forced to **compress** data and learn **most important features** (drops unimportant ones)

**Goal**: Dimensionality reduction while preserving essential information.

The following code builds a simple linear autoencoder that takes a 3D input, projects it down to 2D, then projects it back up to 3D. Since we will train the model using targets equal to the inputs, gradient descent will have to find the 2D plane that lies closest to the training data, just like PCA would. 
```python
import torch 
import torch.nn as nn 
import torchmetrics
from torch.utils.data import DataLoader, TensorDataset

torch.manual_seed(42) 

encoder = nn.Linear(3, 2) 
decoder = nn.Linear(2, 3) 

autoencoder = nn.Sequential(encoder, decoder).to(device) 

X_train = [...] # generate a 3D dataset, like in Chapter 7 
train_set = TensorDataset(X_train, X_train) # the inputs are also the targets
train_loader = DataLoader(train_set, batch_size=32, shuffle=True)

optimizer = torch.optim.NAdam(autoencoder.parameters(), lr=0.2) 
mse = nn.MSELoss() 
rmse = torchmetrics.MeanSquaredError(squared=False).to(device) 

train(autoencoder, optimizer, mse, train_loader, n_epochs=20)
```

```python
codings = encoder(X_train.to(device))
```

This code is really not very different from all the MLPs we built in past chapters, but there are a few things to note: We organized the autoencoder into two subcomponents: the encoder and the decoder, each composed of a single Linear layer in this example, and the autoencoder is a Sequential model containing the encoder followed by the decoder. The autoencoder’s number of outputs is equal to the number of inputs (i.e., 3). To perform PCA, we do not use any activation function (i.e., all neurons are linear), and the cost function is the MSE. That’s because PCA is a linear transformation. We will see more complex and nonlinear autoencoders shortly.