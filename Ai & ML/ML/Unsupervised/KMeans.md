![[Pasted image 20240901195858.png]]

```python
# Import KMeans
from sklearn.cluster import KMeans
 
# Create a KMeans instance with 3 clusters: model
model = KMeans(n_clusters = 3)
  
# Fit model to points
model.fit(points)

# Determine the cluster labels of new_points: labels
labels = model.predict(new_points)

# Print cluster labels of new_points
print(labels)
```

Since the idea is already to put labels for the dataset we have so the predictions here are called labels.
```python
# Perform the necessary imports
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
  
# Create scaler: scaler
scaler = StandardScaler()  

# Create KMeans instance: kmeans
kmeans = KMeans(n_clusters = 4)  

# Create pipeline: pipeline
pipeline = make_pipeline(scaler,kmeans)
```
```python
# Import pandas
import pandas as pd


# Fit the pipeline to samples
pipeline.fit(samples)

  
# Calculate the cluster labels: labels
labels = pipeline.predict(samples)
  
# Create a DataFrame with labels and species as columns: df
df = pd.DataFrame({'labels': labels, 'species': species})  
# Create crosstab: ct
ct = pd.crosstab(df["labels"],df["species"])

# Display ct
print(ct)
```

Data points nearest to centroid grouped together
Higher k = smaller clusters with greater detail
Lower k = larger clusters with less detail

Algorithm:
1. Intialize the algo:
	- Select the number of clusters,k
	- Randomly select k centroids
2. Interativly assign points to clusters and update centroids:
	- Compute distance matrix
	- Assign each point to cluster with nearest centroid
	- Update cluster centroids as the mean position
3. Repeat your centroids

### 🌟 What is K-Means?

K-Means is an **unsupervised learning algorithm** used for **clustering**.  
That means: instead of predicting labels, it **groups similar data points together** based on their features.

---
### ⚙️ How does it work? (Intuition)

Imagine you scatter points on a 2D graph. K-Means tries to:
1. Pick **K cluster centers** (centroids) at random.
2. Assign each point to the _nearest_ centroid.
3. Recalculate the centroids as the “average” of all points in that cluster.
4. Repeat steps 2–3 until the centroids stop moving much (convergence).
Result: each point belongs to one of **K clusters**.
---
### 🎯 Example

Suppose a shop wants to group customers by purchase patterns. They don’t know the groups beforehand. K-Means could cluster customers into, say, 3 segments:
- Budget shoppers
- Regular buyers
- Premium spenders
---
### 🔑 Key parameters
- **K (number of clusters)** → You must choose it!
- **Centroids** → The average point of each cluster.
- **Distance metric** → Usually Euclidean distance.
---
### ⚖️ Pros & Cons
✅ Simple & fast  
✅ Works well when clusters are spherical & balanced  
❌ Sensitive to choice of K  
❌ Can get stuck in “local minima” (random start matters)  
❌ Doesn’t handle irregular shapes well

---
