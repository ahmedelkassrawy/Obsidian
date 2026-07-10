# Linear Regression 

## Overview

Linear regression aims to find the best-fitting line (or hyperplane in higher dimensions) by determining optimal values for parameters (e.g., slope ( m ) and intercept ( b )) that minimize prediction errors.

- **Goal**: Find values for ( m ) (slope) and ( b ) (intercept) to produce accurate predictions.
- **Process**: Iterative, starting with assumed ( m ) and ( b ), adjusting until convergence.

## Ordinary Least Squares (OLS) Regression

- **Definition**: The most common technique for fitting a line to data points.
- **How it Works**:
    1. Calculate the vertical (y-direction) distance between each point and the regression line.
    2. Square each distance to prevent negative distances from offsetting positive ones.
    3. Sum the squared distances and divide by the number of points to compute the **Mean Squared Error (MSE)**.
    4. Adjust ( m ) and ( b ) iteratively to minimize MSE.
- **Convergence**: Typically converges in a dozen or fewer iterations.
- **Adjustment Mechanism**: Uses partial derivatives of the MSE function to determine how to adjust ( m ) and ( b ) (involves calculus, not detailed here).

## Handling Outliers

- **Outliers**: Can bias the model or reduce accuracy.
- **Regularization Techniques**:
    - **Ridge Regression**: Adds a penalty to reduce the impact of outliers by shrinking coefficients.
    - **Lasso Regression**:
        - Also mitigates outliers by penalizing large coefficients.
        - **Secondary Benefit**: Handles **multicollinearity** (when input variables are linearly correlated) by effectively ignoring redundant data.

## Types of Linear Regression

- **Simple Linear Regression**:
    - Involves one independent variable (( x )).
    - Equation: ( y = mx + b ).
- **Multiple Linear Regression**:
    - Involves two or more independent variables (( x_1, x_2, x_3, \ldots )).
    - Equation: ( y = b + m_1x_1 + m_2x_2 + \cdots + m_nx_n ).

## Visualizing High-Dimensional Data

- Linear regression works in any number of dimensions, but visualizing high-dimensional datasets (4+ dimensions) is challenging.
- **Techniques for Visualization**:
    - **Principal Component Analysis (PCA)**: Reduces dimensions to 2 or 3 for plotting.
    - **t-distributed Stochastic Neighbor Embedding (t-SNE)**: Another dimensionality reduction technique for visualization.
    - **Pair Plots**: For datasets with a small number of dimensions, plots pairs of dimensions in 2D scatter charts to assess relationships.

## Parametric vs. Nonparametric Algorithms

- **Parametric Algorithms** (e.g., Linear Regression):
    - Fit data to an equation with parameters (e.g., ( m ), ( b )).
    - Require **normalized data** to ensure accuracy and convergence.
    - **Why Normalize?** Unnormalized data (e.g., one feature ranging 0–1, another 0–1,000,000) can skew results or prevent convergence.
- **Nonparametric Algorithms** (e.g., k-Nearest Neighbors):
    - Do not fit data to an equation.
    - Still benefit from normalization due to internal distance-based calculations.

## Key Considerations

- **Normalization**:
    - Essential for parametric models like linear regression, support vector machines, and neural networks.
    - Ensures features are on similar scales to improve model performance.
- **Applications**:
    - Linear regression is versatile for both 2D and high-dimensional datasets.
    - Useful when data relationships are approximately linear.
- **Limitations**:
    - Sensitive to outliers without regularization.
    - Assumes linear relationships between variables.
    - Multicollinearity can affect standard linear regression (mitigated by Lasso).

## Summary

- Linear regression uses OLS to minimize MSE and fit a line/hyperplane.
- Regularization (Ridge, Lasso) handles outliers and multicollinearity.
- Visualization of high-dimensional data requires techniques like PCA, t-SNE, or pair plots.
- Normalization is critical for parametric models to ensure accuracy and convergence.

----
# Decision Trees

## Overview

A **decision tree** is a tree structure used in machine learning to predict outcomes by answering a series of questions, typically in a binary (yes/no) format. It can be applied to both regression and classification tasks.

- **Structure**: Most decision trees are binary trees, where each node represents a question, and branches represent answers leading to further nodes or outcomes.
- **Example**: Predicting a programmer’s salary based on years of experience involves traversing the tree through yes/no decisions to reach a leaf node (e.g., ~$100K for 10 years of experience).

## Types of Decision Trees

- **Decision Tree Regressor**:
    - **Leaf Nodes**: Represent numerical values (e.g., predicted salary).
    - **Output**: Discrete, limited to values assigned to leaf nodes (not continuous like linear regression).
- **Decision Tree Classifier**:
    - **Leaf Nodes**: Represent classes (e.g., categories like "positive" or "negative").
    - **Output**: Discrete class labels.

## How Decision Trees Are Built

- **Process**: Recursively split the training data into subsets based on feature values.
- **Key Decisions at Each Node**:
    1. **Which feature (column) to split on**: Choose the feature that best separates the data.
    2. **What value to split on**: Select a threshold that minimizes impurity (classification) or variance (regression).
- **Splitting Criteria**:
    - **Classification**: Use an impurity measure like **Gini**, which quantifies the percentage of misclassified samples for a given split.
    - **Regression**: Minimize the sum of squared errors or absolute errors (difference between split value and data points).
- **Growth**:
    - Starts at the root node and recursively splits until:
        - All data is perfectly separated (fully leafed out).
        - External constraints (e.g., maximum depth) stop growth.

## Key Parameters

- **`max_depth`**: Limits the maximum depth of the tree to prevent overfitting.
- **`min_samples_split`**: Minimum number of samples required to split a node.
- **`min_samples_leaf`**: Minimum number of samples required at a leaf node.
- **Example Code**:
    
    ```python
    from sklearn.tree import DecisionTreeRegressor
    model = DecisionTreeRegressor()
    model.fit(x, y)
    ```
    
    - Default parameters allow simple tree construction, but tuning `max_depth`, `min_samples_split`, and `min_samples_leaf` can control complexity.

## Characteristics

- **Nonparametric**:
    - Does not fit an equation to the data (unlike linear regression).
    - Builds a binary tree structure, so **normalization is not required**.
- **Versatility**:
    - Works equally well with **linear** and **nonlinear data**.
    - Unaffected by the shape of the data distribution.

## Advantages

- Simple to understand and interpret.
- Handles both regression and classification tasks.
- Robust to nonlinear relationships in data.

## Disadvantages: Overfitting

- **Problem**: Decision trees are highly prone to **overfitting**, especially if allowed to grow too large.
    - A large tree can "memorize" the training data, leading to poor generalization on new data.
    - Overfit models may seem accurate on training data but perform poorly on unseen data.
- **Why It Matters**: Overfitting is a critical issue in machine learning, as it creates models that appear accurate but fail in real-world applications.

## Mitigating Overfitting

- **Constrain Tree Growth**:
    - Use parameters like `max_depth`, `min_samples_split`, or `min_samples_leaf` to limit tree complexity.
- **Random Forests**:
    - Use ensembles of decision trees to reduce overfitting by averaging predictions from multiple trees.

## Summary

- Decision trees predict outcomes by traversing a series of yes/no questions in a binary tree structure.
- Used for both regression (discrete numerical outputs) and classification (class labels).
- Built by recursively splitting data based on features and thresholds that minimize impurity (Gini for classification) or variance (for regression).
- Nonparametric, so no normalization is needed, and they handle nonlinear data well.
- Prone to overfitting, which can be mitigated by constraining growth or using random forests.
- Key parameters (`max_depth`, `min_samples_split`, `min_samples_leaf`) control tree complexity.
-----
# Random Forests
A random forest is a collection of decision trees (often hundreds of them), each trained differently on the same data,
Typically, each tree is trained on randomly selected rows in the dataset, and branching is based on columns that are randomly selected at every split. The model can’t fit too tightly to the training data because every tree trains on a different subset of the data. The trees are built independently, and when the model makes a prediction, it runs the input through all the decision trees and averages the result. Because the trees are constructed independently, training can be parallelized on hardware that supports it.
![[Pasted image 20251016140300.png]]

It’s a simple concept, and one that works well in practice. Random forests can be used for both regression and classification, and Scikit provides classes such as RandomFores t Regressor and RandomForestClassifier to help out. They feature a number of tunable parameters, including n_estimators, which specifies the number of trees in the random forest (default = 100); max_depth, which limits the depth of each tree; and max_samples, which specifies the fraction of the rows in the training data used to build individual trees.
how RandomForestRegressor fits to the income-versus-experience dataset with max_depth=3 75 and max_samples=0.5, meaning no tree sees more than 50% of the rows in the dataset.
Because decision trees are nonparametric, random forests are nonparametric also. And even though Figure 2-7 shows how a random forest fits a linear dataset, random forests are perfectly capable of modeling nonlinear datasets too.

----
# Gradient-Boosting Machines
- **Concept**: Gradient boosting is another ensemble modeling technique that builds **dependent decision trees** sequentially to improve predictions iteratively.
    
- **How It Works**:
    - Unlike random forests, GBDTs train trees sequentially, with each tree modeling the **errors (residuals)** of the previous trees.
        
    - **Process**:
        1. Start with the **mean** of the target values as a baseline prediction.
        2. Compute **residuals** (difference between actual and predicted values).
        3. Train a decision tree (often a **decision tree stump** with depth 1) to predict the residuals.
        4. Add the tree’s predictions (scaled by a **learning rate**) to the previous predictions.
        5. Repeat for ( n ) trees (typically 100 or more), generating new residuals each time.
            
    - **Prediction**: Run input through all trees and sum their outputs (termed **additive modeling**).
        
- **Key Characteristics**:
    - **Nonparametric**: Like random forests, no data normalization is required.
    - **Weak Learners**: Uses shallow trees (e.g., stumps with depth 1) to ensure each tree contributes minimally to the final prediction.
    - **Learning Rate**: A parameter (e.g., 0.1) that scales each tree’s contribution to prevent overfitting and control model learning speed.
    - **Applications**: Used for both **regression** and **classification**.
    - **Performance**: GBDTs are highly effective for complex datasets, often outperforming other models except neural networks and support vector machines.
## Mitigating Overfitting in GBDTs

- **Susceptibility**: Unlike random forests, GBDTs are prone to **overfitting** if not properly tuned.
    
- **Strategies**:
    - **Subsample Parameter**: Limits the fraction of the dataset each tree sees (similar to max_samples in random forests).
    - **Learning Rate**: Lowering the learning rate (e.g., from default 0.1 to a smaller value) reduces the influence of individual trees, improving generalization.
    - **Other Parameters**: Control tree complexity (e.g., max_depth, min_samples_split) to prevent overfitting.
## Comparison

- **Random Forests**:
    - Build independent trees in parallel.
    - Less prone to overfitting.
    - Simpler to tune.
        
- **GBDTs**:
    - Build dependent trees sequentially.
    - More powerful but susceptible to overfitting.
    - Require careful tuning of parameters like learning_rate and subsample.
## Summary

- **Random Forests**: Combine weak decision trees using random subsets of data/features, averaging predictions to create robust models with low overfitting risk.
- **Gradient Boosting (GBDTs)**: Sequentially build trees to model residuals, summing outputs for high accuracy but requiring careful tuning to avoid overfitting.
- Both are **nonparametric**, making them versatile for complex, nonlinear datasets.
- Key parameters (max_samples for random forests, learning_rate and subsample for GBDTs) help control model complexity and generalization.

![[Pasted image 20251016140605.png]]

```python
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

# Set up the GradientBoostingRegressor with parameters matching your setup
gbr = GradientBoostingRegressor(
    n_estimators=100,        # Number of trees (n_trees)
    learning_rate=0.1,       # Learning rate (le)
    max_depth=1,             # Depth of each tree
    random_state=0           # For reproducibility
)

# Fit the model
gbr.fit(x, y)

# Predict for x=10
x_test = np.array([[10.0]])
y_pred = gbr.predict(x_test)

# Output the prediction
print(y_pred[0])
```

---
