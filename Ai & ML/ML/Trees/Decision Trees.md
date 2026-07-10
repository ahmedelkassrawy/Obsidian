
---
- Start with a seed node and labeled training data
- Find the feature that best splits the data
- Each split partitions the node's input data
- Repeat the process for each new node
### Tree Pruning
Stop growing the trees when :
- Max tree depth is reached.
- Min number of data points in a node has been exceeded
- Min number of samples in a leaf has been exceeded
- Decision tree has reached max number of leaf nodes
## Decision Tree Classifier Regularization
Decision trees are powerful but prone to **overfitting**, where they fit the training data too closely. Regularization hyperparameters help control complexity and improve generalization.

### Regularization Hyperparameters

|**Hyperparameter**|**Description**|**Effect**|
|---|---|---|
|**max_depth**|Maximum depth of the tree.|Reducing limits complexity, reduces overfitting.|
|**max_features**|Maximum number of features considered for splitting at each node.|Introduces randomness, reduces overfitting.|
|**max_leaf_nodes**|Maximum number of leaf nodes in the tree.|Caps tree growth, promotes simplicity.|
|**min_samples_split**|Minimum samples required to split a node.|Higher values prevent specific splits.|
|**min_samples_leaf**|Minimum samples required at a leaf node.|Higher values ensure robust leaves.|
|**min_weight_fraction_leaf**|Minimum fraction of total weighted samples at a leaf node.|Similar to `min_samples_leaf`, for weighted data.|

> [!tip] Regularization Rule
> 
> - **Increase** `min_*` parameters (`min_samples_split`, `min_samples_leaf`, `min_weight_fraction_leaf`) to restrict tree growth.
> - **Reduce** `max_*` parameters (`max_depth`, `max_features`, `max_leaf_nodes`) to simplify the model and reduce overfitting.

### Code Example: Regularized Decision Tree

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_moons

# Sample data
X, y = make_moons(n_samples=100, noise=0.15, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Regularized decision tree
dt_clf = DecisionTreeClassifier(max_depth=5, min_samples_leaf=5, max_features=0.8, random_state=42)
dt_clf.fit(X_train, y_train)

# Evaluate
print(f"Test accuracy: {dt_clf.score(X_test, y_test):.3f}")
```

---
## Overfitting in Decision Trees

Decision trees are highly flexible, which makes them **susceptible to overfitting**. Without regularization, they can create complex models that memorize training data, leading to poor generalization.

### Causes of Overfitting

- **Unrestricted growth**: Deep trees capture noise in the data.
- **Small sample splits**: Nodes with few samples create overly specific rules.
- **High variance**: Small changes in data or hyperparameters lead to different trees.

> [!warning] High Variance  
> Decision trees exhibit **high variance**, meaning small changes in training data or hyperparameters can result in significantly different models. Use regularization and validation (e.g., cross-validation) to ensure robustness.

---
## Regularization Parameters

Decision Trees are highly prone to overfitting. Regularization is controlled primarily through hyperparameters that restrict the tree's growth.
### Key Regularization Hyperparameters

**max_depth** : Maximum depth of the tree. Default is None (unlimited). Reducing max_depth is one of the most effective ways to regularize the model.
**max_features** : Maximum number of features evaluated for splitting at each node. Reduces the feature search space.
**max_leaf_nodes** : Maximum number of leaf nodes in the tree. Limits overall tree size.
**min_samples_split** : Minimum number of samples required in a node before it can be split.
**min_samples_leaf** : Minimum number of samples required in a leaf node. **Important regularization parameter**.
**min_weight_fraction_leaf** :Minimum weighted fraction of total samples required in a leaf node.
**min_impurity_decrease** : Minimum impurity decrease required for a split to be considered.

### Recommended Regularization Approach

- **Primary parameter**: `max_depth` - provides effective regularization while keeping the tree interpretable
- **Secondary parameter**: `min_samples_leaf` - particularly useful for smaller datasets
- **Additional consideration**: `max_features` - beneficial when working with high-dimensional datasets
## Decision Tree Characteristics
### High Variance Problem
Decision Trees exhibit **high variance**:
- Small changes in hyperparameters or training data can produce substantially different tree structures
- Even retraining the same tree on identical data can produce different results due to the stochastic nature of feature selection at each node

**Solution**: Setting the `random_state` hyperparameter ensures reproducible results.

## Handling Missing Values

Both `DecisionTreeClassifier` and `DecisionTreeRegressor` **natively support missing values**. No imputation is required before training.

## Reducing Overfitting in Practice

### Example Approach
Setting `min_samples_leaf=10` significantly reduces overfitting while maintaining reasonable predictive performance.

## Dimensionality Reduction with Decision Trees
Decision Trees can struggle with high-dimensional datasets. One approach is to:
1. Scale the data using StandardScaler
2. Apply Principal Component Analysis (PCA)
3. Train the decision tree on the transformed data

```python
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

pca_pipeline = make_pipeline(StandardScaler(), PCA())
X_transformed = pca_pipeline.fit_transform(X)
tree_clf = DecisionTreeClassifier(max_depth=2, random_state=42)
tree_clf.fit(X_transformed, y)
```

## Key Takeaways
- Decision Trees require explicit regularization to prevent overfitting
- **Most effective regularization parameters**: `max_depth` and `min_samples_leaf`
- Trees exhibit high variance: small input changes can produce substantially different models
- Native support for missing values eliminates the need for imputation
- For high-dimensional data, preprocessing with scaling and PCA can improve performance
## Regularization Strategy Summary

|Scenario|Recommended Parameters|
|---|---|
|**General purpose**|Start with max_depth and min_samples_leaf|
|**Small datasets**|Emphasize min_samples_leaf (higher values)|
|**High-dimensional datasets**|Use max_features in addition to standard regularization|
|**Reproducibility**|Always set random_state to ensure consistent results|
## Important Considerations
- Decision Trees are sensitive to hyperparameter choices and exhibit high variance
- Regularization should be applied during training to prevent overfitting
- Unlike other algorithms, decision trees do not require feature scaling
- The combination of scaling + PCA can be beneficial for high-dimensional problems despite trees being scale-invariant
