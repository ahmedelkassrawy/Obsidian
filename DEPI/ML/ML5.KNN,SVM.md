K-Nearest Neighbors (KNN) is a 
- non-parametric
- lazy learning algorithm that is used for both classification and regression

How KNN Works ? 
	1.Choose K (the number of neighbors). 
	2.Calculate the distance between the test point and all training points (commonly using Euclidean distance). 
	3.Identify the K closest points. 
	4.Vote: Classify the test point based on the majority class of its K neighbors.

Selecting the Best Value for 𝑘 in KNN 
Here are two common methods used to find the optimal 𝑘:
- Grid Search is an exhaustive search method to try different 𝑘 values. 
- The Elbow Method is a visual technique to find the optimal 𝑘 based on error or accuracy plots

Pros and Cons of KNN 
Advantages 
1. Easy to Implement
2. Effective for Small Datasets
3. Non-parametric: No assumptions about data distribution

Disadvantages 
1. Computationally Expensive: Requires calculating the distance for every test point against all training points.
2. Sensitive to Irrelevant Features: KNN’s performance can degrade if irrelevant or redundant features are included. 
3. Sensitive to Scaling: Features with larger ranges will dominate unless the data is normalized. 
4. Memory Intensive: Since KNN stores all data points, it can be memory-intensive with large datasets. 
5. Handling Missing Data: KNN doesn’t handle missing values well. 
6. Sensitive to Outliers: Outliers can have a disproportionate influence on the classification

```python

```
---
### SVM
- Used for classification and regression

How SVM works 
- by finding a hyperplane that best separates the data into different classes. 
- The goal is to find the optimal hyperplane with the **maximum margin** between the closest points of the two classes (called support vectors)

![[Pasted image 20260304232320.png]]

How SVM Works ? 
1. **Linear Separation**: If the data is <mark style="background:#40a9ff">linearly separable</mark>, SVM finds the optimal line (in 2D) or hyperplane (in higher dimensions) that divides the classes with the **maximum margin.** 
2. **Support Vectors**: The data points that are closest to the hyperplane are called **support vectors**, and they influence the position and orientation of the hyperplane. 
3. **Non-Linear Data**: If the data is <mark style="background:#40a9ff">not linearly separable,</mark> SVM uses the **kernel** trick to transform the data into a higher-dimensional space where it becomes separable by a hyperplane

Example of SVM 
1. **Linear SVM** 
	- Imagine two classes, red and blue, that can be separated by a straight line. 
	- The support vectors are the points closest to the hyperplane. 
	- The optimal hyperplane is the one that **maximizes** the margin between the two classes
2. Non Linear SVM with Kernel Trick
	- When the data is not linearly separable
	- SVM applies the kernel trick to transform the data into a higher-dimensional space where it becomes linearly separable

![[Pasted image 20260304232757.png]]

Advantages of SVM 
- **Effective in High-Dimensional Spaces**: SVM is well-suited for problems with a large number of features. 
- **Works with Both Linear and Non-Linear Data**: By applying kernel functions (e.g., radial basis function, polynomial), SVM can handle non-linear relationships. 
- **Robust to Overfitting**: Especially in high-dimensional feature spaces, SVM can perform well

Disadvantages of SVM 
- **Computationally Expensive**: SVM can be slow for very large datasets. 
- **Choosing the Right Kernel**: The performance of SVM is highly dependent on the choice of kernel, which may not always be straightforward

![[Pasted image 20260304232945.png]]

