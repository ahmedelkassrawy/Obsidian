# Principal Component Analysis (PCA)

## Overview

PCA identifies the hyperplane closest to the data and projects the data onto it. The goal is to select the axis that preserves the maximum amount of variance to minimize information loss.

- **Key Idea**: Choose the axis that minimizes the mean squared distance between the original dataset and its projection.
- PCA identifies the axis accounting for the largest amount of variance in the training set.
- **Assumption**: The dataset is centered around the origin. Scikit-Learn’s PCA classes handle data centering automatically.

## 1. **PCA (Principal Component Analysis)**

**What it does:**
- A **linear** method.
- Finds new axes (principal components) that maximize the variance in the data.
- First axis = direction with max variance, second axis = orthogonal to the first with next max variance, etc.
- You can project data into 2D or 3D while keeping as much variance as possible.

**When to use PCA:**
- Data compression, noise reduction.
- Preprocessing before applying another algorithm.
- Works best when relationships are linear.
## Implementation in Scikit-Learn

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# Plot
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='tab10', s=15)
plt.title("PCA on Digits Dataset")
plt.show()
```

## Explained Variance Ratio

The `explained_variance_ratio_` attribute shows the proportion of the dataset’s variance along each principal component (PC).

Example:

```python
pca.explained_variance_ratio_
# Output: array([0.7578477, 0.15186921])
```

- Interpretation: ~76% of variance lies along the first PC, ~15% along the second PC, leaving ~9% for the third PC, which likely carries little information.

## Choosing the Right Number of Dimensions

Instead of arbitrarily choosing the number of dimensions, select dimensions that preserve a sufficiently large portion of the variance (e.g., 95%).

Example:

```python
pca = PCA(n_components=0.95)
X_reduced = pca.fit_transform(X_train)
```

The actual number of components is determined during training and stored in `n_components_`:

```python
pca.n_components_
# Output: 154
```

## Other Dimensionality Reduction Techniques

### t-SNE (t-distributed Stochastic Neighbor Embedding)

- **Purpose**: Reduces dimensionality while keeping similar instances close and dissimilar instances apart.
- **Use Case**: Primarily for visualization, e.g., visualizing clusters of high-dimensional data like MNIST images in 2D.
- **Scikit-Learn**: `sklearn.manifold.TSNE`

## 2. **t-SNE (t-distributed Stochastic Neighbor Embedding)**

**What it does:**
- A **nonlinear** method.
- Focuses on preserving **local structure** (neighbors).
- Works by converting pairwise distances into probabilities and minimizing divergence between high-d and low-d distributions.
- Very effective for visualization but **computationally heavy**.

**When to use t-SNE:**
- Visualization of embeddings (like word2vec, image features, LLM embeddings).
- Not for preprocessing — only for **visualization**.
- Works great for small to medium datasets (<50k samples).

```python
from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, random_state=42, perplexity=30)
X_tsne = tsne.fit_transform(X)

plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=y, cmap='tab10', s=15)
plt.title("t-SNE on Digits Dataset")
plt.show()
```

## 3. **UMAP (Uniform Manifold Approximation and Projection)**

**What it does:**
- Also **nonlinear**.
- Builds a graph of nearest neighbors and optimizes layout in low dimensions.
- Preserves both **local and global structure** better than t-SNE.
- **Much faster** and scalable to large datasets.

**When to use UMAP:**
- Visualization **and** preprocessing (unlike t-SNE).
- Very popular in NLP (sentence embeddings), biology (single-cell RNA-seq), etc.
- Better than t-SNE for large datasets.

```python
import umap

umap_model = umap.UMAP(n_components=2, random_state=42)
X_umap = umap_model.fit_transform(X)

plt.scatter(X_umap[:, 0], X_umap[:, 1], c=y, cmap='tab10', s=15)
plt.title("UMAP on Digits Dataset")
plt.show()
```

## ⚡ Quick Comparison

| Method | Linear/Nonlinear | Speed | Preserves           | Best For                                  |
| ------ | ---------------- | ----- | ------------------- | ----------------------------------------- |
| PCA    | Linear           | Fast  | Global variance     | Compression, preprocessing                |
| t-SNE  | Nonlinear        | Slow  | Local neighborhoods | Visualization of small datasets           |
| UMAP   | Nonlinear        | Fast  | Local + some global | Visualization + preprocessing, large data |
### Linear Discriminant Analysis (LDA)

- **Purpose**: A linear classification algorithm that learns the most discriminative axes between classes during training.
- **Projection**: Projects data onto a hyperplane to maximize class separation.
- **Use Case**: Reduces dimensionality before applying another classification algorithm (if LDA alone is insufficient).
- **Scikit-Learn**: `sklearn.discriminant_analysis.LinearDiscriminantAnalysis`

