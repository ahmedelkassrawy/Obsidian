## Clustering

Clustering groups similar instances into clusters, serving as a powerful tool for various applications:

- **Customer Segmentation**: Cluster customers based on purchases and website activity, useful for recommender systems to suggest content enjoyed by others in the same cluster.
- **Data Analysis**: Analyze new datasets by grouping similar instances.
- **Dimensionality Reduction**: After clustering into ( k ) clusters, each instance can be represented by a ( k )-dimensional vector, typically lower-dimensional than the original feature vector.
- **Feature Engineering**: Clusters can be used as extra features.
- **Semi-Supervised Learning**: Leverage clusters to improve learning with limited labeled data.
- **Search Engines**: Group similar search results.
- **Image Segmentation**: Partition images into meaningful regions.

## Anomaly Detection (Outlier Detection)

Anomaly detection learns the characteristics of "normal" data and uses this to identify abnormal instances.

## Clustering Algorithms

### K-Means

K-Means clusters data by assigning instances to the nearest centroid.

#### Implementation

```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

X, y = make_blobs([...])  # Generate blobs; y contains cluster IDs (not used for prediction)
k = 5
kmeans = KMeans(n_clusters=k, random_state=42)
y_pred = kmeans.fit_predict(X)
```

#### Output

```python
y_pred
>> Output: array([4, 0, 1, ..., 2, 1, 0], dtype=int32)

y_pred is kmeans.labels_
>> Output: True
```

#### Concept

1. Randomly place ( k ) centroids (e.g., by selecting ( k ) instances from the dataset).
2. Label instances based on the nearest centroid.
3. Update centroids to the mean of assigned instances.
4. Repeat until centroids stop moving.
5. The algorithm converges as the mean squared distance between instances and their closest centroids decreases, guaranteed to stop as it cannot be negative.

![[Pasted image 20250626220959.png]]

#### Tips

- **Feature Scaling**: Scale input features before running K-Means to avoid stretched clusters, as K-Means relies on distance to centroids.
- Scaling improves performance but does not guarantee spherical clusters.

#### Limitations of K-Means

- Requires specifying the number of clusters ( k ), which may not be obvious.
- Performs poorly when clusters have different sizes, densities, or non-spherical shapes, as it only considers distance to centroids.
- Hard clustering assigns each instance to a single cluster, which may not suit cases where soft clustering (scores per cluster) is preferred.

### DBSCAN (Density-Based Spatial Clustering of Applications with Noise)

DBSCAN identifies clusters based on density, counting instances within a small distance ( \epsilon ) (epsilon) from each instance, called the ( \epsilon )-neighborhood.

#### Implementation

```python
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons

X, y = make_moons(n_samples=1000, noise=0.05)
dbscan = DBSCAN(eps=0.05, min_samples=5)
dbscan.fit(X)
```

#### Output

```python
dbscan.labels_
>> Output: array([ 0, 2, -1, -1, 1, 0, 0, 0, 2, 5, [...], 3, 3, 4, 2, 6, 3])
```

- Instances with a cluster index of (-1) are considered anomalies (outliers).

#### Tuning

- Adjusting ( \epsilon ) (e.g., increasing to 0.2) can improve clustering for complex shapes, like the moons dataset.

![[Pasted image 20250626224216.png]]

#### Key Attributes

- `core_sample_indices_`: Indices of core instances (instances with at least `min_samples` neighbors within ( \epsilon )).
- `components_`: Core instances themselves.

```python
dbscan.core_sample_indices_
>> Output: array([ 0, 4, 5, 6, 7, 8, 10, 11, [...], 993, 995, 997, 998, 999])

dbscan.components_
>> Output: array([[-0.02137124, 0.40618608], [-0.84192557, 0.53058695], [...], [ 0.79419406, 0.60777171]])
```

#### Notes

- DBSCAN does not have a `predict()` method, only `fit_predict()`. It cannot directly assign new instances to existing clusters.
- **Advantages**:
    - Identifies clusters of any shape.
    - Robust to outliers.
    - Only two hyperparameters: ( \epsilon ) (eps) and `min_samples`.
- **Use Case**: Effective for datasets with complex, non-spherical clusters or when outliers need to be identified.