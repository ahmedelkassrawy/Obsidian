- Clustering (KMeans,DBSCAN)
- Dimensionality Reduction (PCA,t-SNE)

#### Clustering 
- type of unsupervised learning where data points are grouped based on similarities in their characteristics. 
- Points in the same cluster are likely to be closer to each other in the feature space compared to points in different clusters

**Types of Clustering**
1. Hard Clustering
Each data point is strictly assigned to one cluster, meaning that a point can only belong to one cluster and not to multiple clusters.

2. Soft Clustering
Each data point can belong to multiple clusters with a probability, indicating how likely a data point is to belong to different clusters. This allows for overlapping between clusters, which may share common features

![[Pasted image 20260404145420.png]]

#### KMeans
- K-Means is a **centroid-based clustering** algorithm where data points are assigned to clusters based on the **closest centroid.** 
- The algorithm **operates iteratively, improving the position** of the centroids over time until a local optimal clustering is reached

**Key Points**
1. Centroid-based Clustering
- Each data point is assigned to the cluster whose centroid (central point) is closest.
- The algorithm continues to refine the position of these centroids to minimize the total distance between data points and their respective centroids.

**Example Explanation**
Imagine organizing books into three shelves based on their similarities. This is analogous to how K-Means organizes data points into clusters

**Steps in K-Means**
1. Choose the number of clusters 𝐾
2. Initialize the centroids by randomly picking points from the data.
3. Assignment step
Assign each point to the nearest centroid.
4. Update step
Recalculate the centroid for each cluster by finding the mean of all points in the cluster
5. Repeat
Repeat steps 3 and 4 until the centroids no longer move significantly or until a stopping criterion is met
6. Convergence
The algorithm converges when the total distance between points and centroids can’t be improved further. At this point, the centroids will remain fixed

### **1. Distance and Similarity Metrics**

- **Euclidean Distance:** K-Means uses Euclidean distance to measure the straight-line distance between two points, helping determine the similarity or dissimilarity between data points.
    
- **Formula:** The distance between point A $(x_{1},y_{1})$ and point B $(x_{2},y_{2})$ is calculated as $\sqrt{(x_{1}-x_{2})^{2}+(y_{1}-y_{2})^{2}}$.
    

### **2. Centroids**

- **Definition:** The centroid is the central point and key component of a cluster. It is the calculated mean (average) of all the data points located within that cluster on a 2D X-Y plane.
    
- **Calculation:** For a dataset with $n$ points, the centroid is updated using the formula $Centroid=(\frac{X_{1}+X_{2}+...+X_{n}}{n},\frac{Y_{1}+Y_{2}+...+Y_{n}}{n})$.
    
- **Role:** The centroid is continually updated as the algorithm iterates, which refines the grouping of the clusters.
    

### **3. The K-Means Iterative Process**

The overall goal of the algorithm is to divide $n$ data points into $k$ desired clusters based on their distance to the centroids. This is done through a continuous loop:

- **Step 1: Assignment Step:** The Euclidean distance between each data point and the initial centroids is calculated. Points are then assigned to the nearest centroid to form the initial clusters.
    
- **Step 2: Optimization Step:** The algorithm computes new optimal centroids by calculating the mean of the points within each freshly formed cluster.
    
- **Iteration:** After optimization, the process loops back to Step 1. Points are reassigned based on the new centroids, and the distance calculation and reassignment cycle repeats.
### **4. Stopping Criteria**

The K-Means algorithm runs in a continuous loop until it meets one of four conditions:

- **Cluster Stability:** Data points stop switching from one cluster to another.
    
- **Centroid Stability:** The centroids stop moving and their positions remain fixed.
    
- **Distance Threshold:** The distance between the data points and their respective centroids falls below a predefined limit.
    
- **Maximum Iterations:** The algorithm hits a hard cap on the number of allowed iterations (useful if it struggles to converge naturally).
    

### **5. Updating Centroids**

During the update step, the algorithm calculates the new position of a cluster's centroid by finding the **mean (average) value** of all the data points currently assigned to it. This is done feature-by-feature to ensure the new centroid accurately represents the center of that specific group.

### **6. Evaluating Performance & Choosing $K$**

- **Inertia:** This is a performance metric defined as the sum of the squared distances between each data point and its assigned centroid. **Lower inertia** indicates better clustering, as it means the points are tightly packed around their center.
    
- **The Elbow Method:** Because you have to guess the number of clusters ($K$) beforehand, the Elbow Method helps find the optimal number. By plotting inertia against different values of $K$, you look for the "elbow"—the point on the graph where the decrease in inertia slows down significantly, indicating that adding more clusters provides diminishing returns.
    

### **7. Advantages vs. Disadvantages**

**Advantages:**
- Simple to understand, implement, and apply.
- Highly computationally efficient.
- Scales incredibly well for massive datasets with millions of points.

**Disadvantages:**
- You must pre-define the number of clusters ($K$) before running the algorithm.
- It is strictly limited to numerical data (categorical data must be converted first).
- It is highly sensitive to the initial placement of centroids, outliers in the data, and feature scaling (requiring data to be normalized/standardized beforehand).
----
### DBSCAN
Unlike K-Means, DBSCAN does not require you to specify the number of clusters beforehand, making it highly useful for datasets with arbitrary shapes or varying densities.
### **1. The Three Types of Data Points**

DBSCAN categorizes every data point into one of three classifications:

- **Core Points:** A point is considered "core" if it has at least `min_samples` of data points (including itself) located within a specific radius, called $\epsilon$ (epsilon). These sit in high-density areas and act as the centers of clusters.
    
- **Border Points:** These fall within the $\epsilon$ neighborhood of a core point but don't have enough neighbors of their own to be classified as core points. They are included in the cluster but sit on the edges rather than the center.
    
- **Noise Points (Outliers):** If a point isn't a core point and isn't close enough to be a border point, it is considered noise and does not belong to any cluster.

### **2. Required Parameters**

To run the algorithm, you must define two key inputs:

- **Epsilon ($\epsilon$):** The maximum distance between two points for them to be considered neighbors.
    
- **`min_samples`:** The absolute minimum number of points required in an area to officially form a dense region or cluster.

### **3. How the Algorithm Works**

The algorithm builds clusters through a step-by-step recursive process:

1. It selects an arbitrary data point to start.
    
2. It looks at the neighborhood within the $\epsilon$ distance.
    
3. If there are enough neighbors (meeting the `min_samples` threshold), a cluster is born, and the point becomes a core point.
    
4. All neighbors are sucked into this new cluster.
    
5. The algorithm then expands the cluster by looking at the neighbors of those newly added points to see if _they_ are core points, repeating the process.
    
6. If a point does not have enough neighbors, it is marked as noise.
    
7. This loops until every single point in the dataset has been processed.
### **4. Advantages of DBSCAN**

- **Automatic Cluster Detection:** Unlike K-Means, you don't have to guess the number of clusters beforehand; DBSCAN finds them naturally based on data density.
    
- **Arbitrary Shapes:** Because it tracks density rather than relying on central points (centroids), it can map out complex, irregularly shaped clusters rather than just spheres.
    
- **Excellent Outlier Handling:** It natively detects and ignores noise, keeping clusters clean.
### **5. Disadvantages of DBSCAN**

- **Parameter Sensitivity:** The algorithm's success heavily relies on you choosing the perfect $\epsilon$ and `min_samples`; poor choices ruin the results.
    
- **Struggles with High Dimensions:** It suffers from the "curse of dimensionality". In datasets with many features, distance gets skewed, making it incredibly difficult to define a meaningful $\epsilon$.