1. **Mention the difference between the classification and Clustering.**
- **Classification** is a form of **supervised learning**. 
	- In classification, the training data includes both the input features and  class labels, typically represented as pairs like $(x^{(i)}, y^{(i)})$. The goal is to learn a decision boundary such as the margin-based boundaries created by Support Vector Machines (SVMs) that can separate the known classes and predict the label of new data.
	
- **Clustering** is a form of **unsupervised learning**.
	- In clustering, the training data consists _only_ of the input features without any  labels or target values  The goal is to automatically discover hidden patterns or group the data, such as using the K-means algorithm to group similar points around cluster centroids.

**What is Elbow method?**
The **Elbow method** is a  technique used in K-means clustering to help determine the right **number of clusters ($K$)** to use for a dataset.

We plot the **Cost function $J$** (distortion) on the y-axis against different values of **$K$ (the number of clusters)** on the x-axis. 
When we increase the number of clusters, the cost function typically decreases.

When looking at the resulting graph, you search for the "**Elbow**" a specific point where the graph bends sharply and the cost function's  flattens .


**Can PCA be used to prevent overfitting?  why?**
No, PCA can't be used to prevent overfitting 

While you can technically use PCA to reduce the number of features (from $n$ down to a smaller number $k$) with the assumption that having fewer features makes a model less likely to overfit, it is not a good way to actually address the problem. Instead, the recommended approach to handle overfitting is to use **regularization**.