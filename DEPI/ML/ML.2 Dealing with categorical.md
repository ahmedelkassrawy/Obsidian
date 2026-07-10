Encoding:
Encoding refers to the process of converting categorical data into a numerical format that can be used by machine learning algorithms

Dimensionality Management 
Encoding helps structure the data in a way that the model can handle efficiently. 
- One-Hot Encoding increases the "dimensions" (columns) of your data to keep things fair. 
- Label Encoding keeps the data compact in a single column when order matters. 

Label Encoding 
- Each category is assigned a unique integer value 
- Example: “Tall" = 0, “Medium" = 1, “Short" = 2. 
- Used when the categories have a meaningful order. 
- The model will understand that category with higher label is more important so assigning the labels in order matters.

One-Hot Encoding 
- Creates a new binary column for each category 
- Example: "Red" = [1, 0, 0], "Green" = [0, 1, 0], "Blue" = [0, 0, 1] 
- Used when there is no ordinal relationship between categories.

Label Encoding: For ordinal features, such as education level (High School, Bachelor's, Master's, etc.), where the order matters.
One-Hot Encoding: For nominal features, such as colors or product categories, where there is no inherent order. 

---
Scaling
Scaling is the process of transforming features so that they are on the same scale

Why Scaling is Important? 
- Without scaling, features with larger values may dominate the model, leading to biased predictions. 
- Scaling ensures that all features contribute equally to the model during training.

Min-Max Scaling (Normalization)
Transforms features to a fixed range, usually between 0 and 1

Standardization (Z-Score Scaling) 
Transforms features so that they have a mean of 0 and standard deviation of 1

When to Use Scaling
- Normalization: When you need your features to be in a bounded range (e.g., in neural networks). 
- Standardization: When the algorithm expects normally distributed data (e.g., linear regression, logistic regression, etc.).

|**Feature**|**Normalization**|**Standardization**|
|---|---|---|
|**The Concept**|Scales everything to a specific range (usually between 0 and 1).|Measures how far a data point is from the mean (average).|
|**Scientific Name**|**Min-Max Scaling**|**Z-Score Scaling**|
|**When to use it?**|When the data does not have a clear distribution (non-Gaussian) or the distribution is unknown.|When your data follows a "Bell Curve" (Normal Distribution).|
|**Sensitivity**|Highly sensitive to **Outliers** (an extreme value will skew the range significantly).|More robust; it is less affected by outliers ("Has a tough heart" / handles extreme numbers better).|

## **1. Normalization (Min-Max Scaling)**

Normalization transforms all feature values into a fixed range, typically **between 0 and 1**
- **Result:** The size and age of the house are moved onto a common scale without changing the relative differences between data points.
    
- **Best For:** Algorithms that do not assume a specific data distribution, such as **Neural Networks** or **KNN**, where keeping a bounded range is critical.
## **2. Standardization (Z-Score Scaling)**
Standardization scales data so that it has a **mean of 0** and a **standard deviation of 1**.

- **Result:** Unlike normalization, the values are not confined to a 0–1 range. Instead, they are centered around zero based on the dataset’s variance.
    
- **Best For:** Algorithms that assume a Gaussian (normal) distribution, such as **Logistic Regression**, **Support Vector Machines (SVM)**, and **Principal Component Analysis (PCA)**.

![[Pasted image 20260215175901.png]]

Ways to Reduce High Bias
- Add more features: This helps the model learn better from the data. 
- Decrease regularization: Too much regularization forces the model to be simple, leading to underfitting. 
- Use more complex models, like polynomial regression, to capture more patterns in the data.

Ways to Reduce High Variance 
- Reduce the number of features or parameters: Simplifying the model reduces overfitting. 
- Avoid overly complex models. 
- Increase the training data size: More data helps the model generalize better.
- Increase regularization: This helps prevent overfitting by keeping the model simpler

Techniques to Reduce Underfitting 
- increase model complexity: Add more features 
- Increase the number of features or use feature engineering to capture more useful information from the data. 
- Remove noise: Clean up the data to avoid irrelevant patterns

Techniques to Reduce Overfitting 
- Increase training data: More data helps the model generalize better 
- Reduce model complexity: Simpler models have less variance and generalize better.
- Regularization : L1 (Lasso) and L2 (Ridge) regularization add penalties to the model to reduce complexity

Regularization Parameter 
	Regularization Parameter (Lambda) 
		-  Lambda (λ) is the regularization parameter that controls the strength of the regularization applied. A higher lambda increases the penalty on large coefficients, effectively reducing overfitting but potentially causing underfitting if λ is too large. 
		- If λ is small, the model will behave more like a traditional regression model (e.g., without regularization), potentially overfitting the data. 
- Effect of Increasing Lambda Increasing lambda results in less overfitting but at the cost of higher bias. This is often referred to as the bias-variance tradeoff.

Types of Regularization (L1 & L2)
1. L2 Regularization (Ridge) 
- In L2 regularization, a squared penalty is added to the sum of the squared coefficients. It helps in shrinking all coefficients, leading to a simpler model with smaller weights. 
- This method reduces the impact of irrelevant features but doesn't force the coefficients of less important features to exactly zero

1. L1 Regularization (Lasso) 
- L1 regularization adds a penalty equal to the absolute value of the magnitude of the coefficients. This has the effect of shrinking some coefficients to zero, which can result in a sparse model (i.e., feature selection)