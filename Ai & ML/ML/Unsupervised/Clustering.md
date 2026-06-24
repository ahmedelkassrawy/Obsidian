```python
from sklearn.cluster import KMeans

distortions = []

for k in range(1,11):
  kmeans = KMeans(n_clusters=k,
                  max_iter = 100,
                  random_state = 42)
                  
  kmeans.fit(df)
  distortions.append(kmeans.inertia_ / df.shape[0])
```

```python
plt.figure(figsize=(8,6))

plt.plot(range(1,11),
         distortions,
         marker='o',
         linestyle='-')

plt.xlabel("NUMBER OF CLUSTERS K")
plt.ylabel("DISTORTIONS")
plt.title("Elbow  Method for optimal k")

plt.grid()
plt.show()
```

```python
from sklearn.decomposition import PCA

optimal_k = 2
kmeans = KMeans(n_clusters = optimal_k,
                max_iter = 100,
                random_state = 42)
                
cluster_labels = kmeans.fit_predict(df) 
```

```python
pca = PCA(n_components = None)
df_scaled = pca.fit_transform(df)
```

```python
plt.figure(figsize=(10, 6))
plt.plot(range(1,len(pca.explained_variance_ratio_) + 1),
         pca.explained_variance_ratio_ , 'o-')

plt.xlabel('Number of Components')
plt.ylabel('Explained Variance Ratio')
plt.title('Choosing the Right Component Number for PCA')

plt.grid()
plt.show()
```

```python
plt.figure(figsize = (10,8))

plt.scatter(
    df_scaled[:,0],
    df_scaled[:,1],
    c = cluster_labels,
    cmap = 'viridis'
)

plt.colorbar()
plt.show()
```

```python
from sklearn.metrics import silhouette_score

labels = kmeans.labels_
score = silhouette_score(df, labels)
print("Silhouette Score:", score)
```

```python
from sklearn.cluster import MiniBatchKMeans

kmeans = MiniBatchKMeans(n_clusters = 2,
                         random_state = 42,
                         batch_size = 300,
                         max_iter = 10)

centroid_history = []

for i in range(10):
  kmeans.partial_fit(df)
  centroid_history.append(kmeans.cluster_centers_.copy())
```

```python
plt.scatter(df_scaled[:, 0], df_scaled[:, 1], c='lightgray', s=30, label='Data')

# Plot centroid movement
colors = ['red', 'blue']
for cluster_id in range(2):
    x = [c[cluster_id][0] for c in centroid_history]
    y = [c[cluster_id][1] for c in centroid_history]
    plt.plot(x, y, marker='x', color=colors[cluster_id], label=f'Centroid {cluster_id}')
    plt.scatter(x, y, s=80, marker='x',c=colors[cluster_id], alpha=0.6)

plt.title("Centroid Movement (2 Clusters)")
plt.legend()
plt.grid(True)
plt.show()
```