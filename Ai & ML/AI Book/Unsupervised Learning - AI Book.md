Unsupervised learning frequently employs a technique called clustering . The purpose of clustering is to group data by similarity. The most popular clustering algorithm is k-means clustering, which takes n data samples and groups them into m clusters, where m is a number you specify. Grouping is performed using an iterative process that computes a centroid for each cluster and assigns samples to clusters based on their proximity to the cluster centroids. If the distance from a particular sample to the centroid of cluster 1 is 2.0 and the distance from the same sample to the 34 center of cluster 2 is 3.0, then the sample is assigned to cluster 1. In Figure 1-6, 200 samples are loosely arranged in three clusters. The diagram on the left shows the raw, ungrouped samples. The diagram on the right shows the cluster centroids (the red dots) with the samples colored by cluster.
![[Pasted image 20251016131205.png]]

```python
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters = 4, random_state = 0)
kmeans.fit(points)

predicted_cluster_idx = kmeans.predict(points)
```

- - During fit, the algorithm:
        1. Randomly initializes 4 centroids (based on n_clusters=4 and random_state=0).
        2. Assigns each point to the nearest centroid.
        3. Updates centroids by computing the mean of all points assigned to each cluster.
        4. Repeats steps 2–3 until convergence (centroids stabilize or max_iter is reached).

- The predict method assigns each data point in points to one of the 4 clusters based on the trained model.
- predicted_cluster_idx: A 1D array (shape: [n_samples]) where each element is an integer (0, 1, 2, or 3) indicating the cluster index for the corresponding point in points.

```python
plt.scatter(x, y,
            c=predicted_cluster_idx,
            s=50,
            alpha=0.7,
            cmap="viridis")
```

Parameters:

- **x, y**: The x and y coordinates of the data points. These are likely the two features of points (e.g., x = points[:, 0], y = points[:, 1]).
- **c=predicted_cluster_idx**: The color of each point is determined by its cluster index (0, 1, 2, or 3). Each cluster gets a different color.
- **s=50**: Sets the size of the scatter points (50 is the area of each point in points^2).
- **alpha=0.7**: Sets the transparency of the points (0 = fully transparent, 1 = fully opaque). A value of 0.7 makes overlapping points slightly see-through.
- **cmap="viridis"**: Specifies the colormap for mapping cluster indices to colors. "viridis" is a perceptually uniform colormap with distinct colors (yellow, green, blue, purple) for the 4 clusters.

##### Extracting the cluster centers
```python
centers = kmeans.cluster_centers_
```
A NumPy array (shape: [n_clusters, n_features]) containing the coordinates of the 4 cluster centroids

**Plotting the Cluster Centers**:
```python
plt.scatter(centers[:, 0],
            centers[:, 1],
            c="red",
            s=100)
```

- This creates a scatter plot of the cluster centroids on the same plot as the data points.
- Parameters:
    - **centers[:, 0]**: The x-coordinates of the centroids (first column of centers).
    - **centers[:, 1]**: The y-coordinates of the centroids (second column of centers).
    - **c="red"**: All centroids are colored red to distinguish them from the data points.
    - **s=100**: Sets the size of the centroid markers (larger than the data points’ s=50 for visibility).

Try setting n_clusters to other values, such as 3 and 5, to see how the points are grouped with different cluster counts. Which begs the question: how do you know what the right number of clusters is? The answer isn’t always obvious from looking at a plot, and if the data has more than three dimensions, you can’t plot it anyway.

One way to pick the right number is with the elbow method, which plots inertias (the sum of the squared distances of the data points to the closest cluster center) obtained from KMeans.inertia_ as a function of cluster counts. Plot inertias this way and look for the sharpest elbow in the curve:
```python
inertias = []

for i in range(1,10):
  kmeans = KMeans(n_clusters = i,random_state=0)
  kmeans.fit(points)
  inertias.append(kmeans.inertia_)

plt.plot(range(1,10),inertias)
plt.xlabel("Number of clusters")
plt.ylabel("Interias")
```
![[Pasted image 20251016133331.png]]