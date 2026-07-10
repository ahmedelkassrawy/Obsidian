- The Curse of dimensionality -> occurring when dealing with datasets that have a large number of features.
- As dimensions of data increase , several problems arise.

**Key Problems of high dimensionality:**
- Inc computational resources
- Sparsity of data
In high dimensions , available data becomes sparse meaning that data points become more spread out.
This makes it difficult for algos , specially those who use measures like KNN to mace accurate predictions
- overfitting
- redundant and irrelevant features
- difficult visualizations
- Distance and similarity issues -> Algorithms that rely on measuring distances between data points (e.g., KNN, SVM) become less effective because, in high-dimensional spaces, distances between points tend to converge. This reduces the usefulness of distance-based learning algorithms.
- Storage concerns

![[Pasted image 20260314215254.png]]

**1-D Space:** Imagine you have a single feature (like age) divided into 4 segments or "bins." You have 10 data points (the dots). Because the space is small, the points are crowded together.
Density = Number of Data Points / Total number of bins (volume)
Density in 1D: 10 /4 = 2.5 points per bin

**2-D Space:** Now you add a second feature (like income). The space is now a grid of 4x4 = 16 bins. Those exact same 10 points are now scattered across a much larger area.
Density in 2D: 10 /16 = 0.625 points per bin

**3-D Space:** Add a third feature, and the space becomes a cube with 4x4x4 = 64 bins. The 10 points are now incredibly isolated from one another.
Density in 3D: 10/64 = 0.156 points per bin.

Density acts as a metric to show how "close" or "informative" your data points are relative to each other.

### Part B: The Exponential Drop
The graph on the right (labeled **b**) plots this relationship mathematically.

- The x-axis ($d$) is the number of dimensions.
- The y-axis is the Density.

Because the "volume" of the space grows exponentially as you add dimensions, the density of your data drops exponentially toward zero. This is the "curse."

To maintain the same density (and thus the same predictive power) as you move from 1D to 100D, you don't just need a little more data; you need an exponentially massive amount of data, which is rarely feasible in the real world. In high-dimensional vector spaces, every data point basically becomes an outlier, making concepts like "nearest neighbor" distance calculations almost meaningless.

---
**How Dimensionality Reduction Helps ?**
**Dimensionality Reduction** techniques address the curse of dimensionality by reducing the number of features (or dimensions) while retaining as much relevant information as possible

1. Feature Selection
This technique involves selecting the most relevant features from the original data and discarding irrelevant or redundant ones

![[Pasted image 20260314220529.png]]

Techniques
- **Wrapper Methods**: These methods evaluate feature subsets based on
model performance (e.g., Forward and Backward Selection).

Wrapper methods treat feature selection as a search problem where various combinations of features are evaluated, and the model with the best performance is selected.

- **Filter Methods**: These methods select features based on their statistical
relationship with the target (e.g., correlation, mutual information).
	- Pearson’s correlation helps measure linear relationships between continuous features and the target. 
	- Chi-Square Test helps assess the dependence between categorical variables

- **Embedded Methods**: Feature selection is integrated within model training
(e.g., using decision trees, Lasso, or Ridge regression)

- Embedded methods perform feature selection during the model training process itself. The learning algorithm decides which features contribute most to the model’s accuracy. 
- These methods combine the advantages of both filter and wrapper methods. 
- They are more efficient than wrapper methods and more robust than filter methods because they are integrated with model training.

2. Feature Extraction / Projection Techniques 
Purpose: This method creates new features by combining the original features, often transforming them into a smaller set of more meaningful variables

Key Point: Unlike feature selection, feature extraction transforms the features, meaning the final set of features is different from the original input features.

![[Pasted image 20260314220942.png]]

Linear Methods: PCA
Non linear Methods: t-SNE , Kernel PCA,UMAP

Standard deviation -> In simpler terms, it gives an idea of how "spread out" the data points are.
Variance -> helps detect extreme outliers
Variance is more sensitive to outliers because of the squared differences

Why Variance Matters in PCA
- In Principal Component Analysis (PCA), the goal is to reduce the dimensionality of data while **retaining the most informative features.**
- PCA **identifies the directions** (principal components) where the data has the **highest variance**
assuming that directions with higher variance are **more informative**

Linear Transformation 
A linear transformation is a function that maps a vector space into another vector space while preserving the operations of vector addition and scalar multiplication
PCA uses linear transformations to project high dimensional data into a lower-dimensional space

Eigenvalues and Eigenvectors
Eigenvectors are special vectors that do not change direction during a transformation. When a matrix is multiplied by one of its eigenvectors, the result is the same eigenvector scaled by a corresponding eigenvalue.

Eigenvectors in PCA represent the directions (or axes) in which the data is projected. 
Eigenvalues correspond to the magnitude of the variance in those directions.
The larger the eigenvalue, the more significant that component is in explaining the variance in the data

Pre-conditions to apply PCA
Features should be scaled (preferably standardized)
- This is because PCA relies on variance, and if the features are not standardized.
- the features with the largest scale will dominate the principal components due to their larger variance. 
- This would bias the PCA results toward the features with higher variance due to their scale rather than the true structure of the data

PCA applies to numerical data
- It doesn’t handle categorical data directly.
- If you have categorical data, it should be transformed into numerical format

Steps to perform PCA
1. Standardize the PCA 
2. Calculate covariance matrix 
The covariance matrix represents the relationships (covariances) between the features. It helps identify the directions of **maximum variance** in the data
3. Calculate Eigenvectors and eigenvalues
4. Select the top K eigenvectors
5. Multiply the original data by the selected eigenvectors

How to choose the number of components K
>[!tip]
>Tip: If you are not reducing dimensionality for visualization but for data analysis, retaining components that explain around 95% of the variance is generally a good rule of thumb.

Reducing for Visualization -> k = 2 or 3
Elbow Method 

---
#### t-SNE
- t-SNE is used for visualization process
- t-SNE is a non-linear dimensionality reduction technique that is highly effective in projecting high-dimensional data down to two or three dimensions for visualization.

How t-SNE Works
- High-dimensional Space: In high dimensions, t-SNE tries to preserve the distance between points. Points that are close to each other in high-dimensional space remainclose in lower dimensions. Similarly, points that are far apart remain distant.
- Attraction and Repulsion: During the projection process, t-SNE attracts points that are nearby and repels points that are farther away in the original high-dimensional space.
- Clusters and Visual Interpretation: After projection, the points form clusters that reveal underlying patterns and groupings in the data

---
Handling Text Features
- If the dataset contains text data, then encoding (like one-hot encoding or labelencoding) will be needed before any selection process, especially if you're using methods like Chi-square that depend on categorical features.
- For numeric values, encoding is irrelevant, but this step becomes necessary for textual data

Order of Operations
- It's important to keep the right order: Feature selection should happen before splitting the data into training and testing sets (train-test split). This ensures that the selected features are consistent across both the training and testing data.
- Scaling (like StandardScaler or MinMaxScaler) should be done after the feature selection process
```python
# Step 3: Standardize the data (PCA works best when data is normalized)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

```python
# Step 4: Perform PCA
pca = PCA(n_components=2)  # Reduce to 2 dimensions for visualization
X_pca = pca.fit_transform(X_scaled)
```

```python
# Step 5: Visualize the transformed data in 2D

plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis', edgecolor='k', s=100)
plt.xlabel('First Principal Component')
plt.ylabel('Second Principal Component')
plt.title('PCA of Iris Dataset')
plt.colorbar(label='Class Labels')
plt.show()
```