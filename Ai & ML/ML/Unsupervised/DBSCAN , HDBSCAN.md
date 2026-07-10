## 🌟 DBSCAN (Density-Based Spatial Clustering of Applications with Noise)

**Core idea:**  
Instead of forcing clusters to be round like K-Means, DBSCAN groups points that are **densely packed together**. Points in low-density areas are treated as **noise (outliers)**.

**Key parameters:**
- **ε (epsilon)**: the radius around a point.
- **minPts**: minimum number of points needed within ε to form a dense region.

**How it works (intuition):**
1. Pick a point.
2. If at least `minPts` neighbors lie within distance ε → it’s a **core point**.
3. Expand the cluster by including reachable points.
4. Continue until no more points can be added.
5. Points that don’t fit → marked as **noise**.

**Strengths:**  
✅ Finds clusters of _any shape_ (not just circles).  
✅ Detects noise automatically.  
❌ Sensitive to parameters (ε and minPts).

---
## 🌟 HDBSCAN (Hierarchical DBSCAN)

This is an **improved version of DBSCAN**.

- DBSCAN struggles with **varying density** (some clusters tight, some spread out).
- HDBSCAN solves this by building a **hierarchy of clusters** and then selecting the best clusters using stability scores.

**Advantages over DBSCAN:**  
✅ Handles varying density much better.  
✅ Removes the need to guess ε (less parameter tuning).  
✅ Produces a hierarchy, so you can see clusters at different density levels.

---
### 🎯 Example

Imagine mapping customers by purchase behavior:
- **DBSCAN** might group “bargain hunters” and “luxury buyers” if they’re dense, but might miss “occasional buyers” if they’re too spread out.
- **HDBSCAN** can detect both dense and spread-out groups by adapting.
---
#### DBSCAN
```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.cluster import DBSCAN

# Generate some non-linear data
X, _ = make_moons(n_samples=300, noise=0.05, random_state=42)

# Apply DBSCAN
dbscan = DBSCAN(eps=0.2, min_samples=5)  # tune eps & min_samples
labels = dbscan.fit_predict(X)

# Plot clusters
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap="viridis", s=50)
plt.title("DBSCAN Clustering")
plt.show()
```
Here, `labels = -1` means **noise points**.

#### HDBSCAN
```python
import hdbscan

# Apply HDBSCAN
hdb = hdbscan.HDBSCAN(min_cluster_size=5)  # only need this param
hdb_labels = hdb.fit_predict(X)

# Plot clusters
plt.scatter(X[:, 0], X[:, 1], c=hdb_labels, cmap="plasma", s=50)
plt.title("HDBSCAN Clustering")
plt.show()

```
💡 HDBSCAN automatically handles varying densities, so fewer parameters to tune.

![[Pasted image 20250826171247.png]]