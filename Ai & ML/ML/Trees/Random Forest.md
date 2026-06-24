## Overview
A Random Forest is an **ensemble learning method** consisting of multiple decision trees. Each tree is trained on a random subset of the data and features, and the final prediction is made by aggregating the predictions of all trees (majority voting for classification, averaging for regression).
## Key Mechanisms
### Bagging in Random Forests
- Random Forests are typically trained using **bagging** (bootstrap aggregating)
- Each tree is trained on a random sample of the training data (with replacement)
- By default, each tree uses the entire training set size (`max_samples` = training set size)

### Extra Randomness
Random Forests introduce additional randomness beyond simple bagging:

- **Feature Subsampling**: At each node, only a **random subset of features** is considered for splitting
  - Default: √n features are randomly selected (where n = total number of features)
  - This increases tree diversity and reduces correlation between trees

This combination of bootstrap sampling and feature subsampling is what distinguishes Random Forests from simple bagging ensembles.

## Comparison with Other Methods

| Method                          | Key Characteristics                                                       |
| ------------------------------- | ------------------------------------------------------------------------- |
| **Single Decision Tree**        | Searches for the globally optimal feature and threshold at each split     |
| **Bagging with Decision Trees** | Bootstrap sampling of data, but full feature set considered at each split |
| **Random Forest**               | Bootstrap sampling + random subset of features at each split              |
| **Extra-Trees**                 | Random Forest + random thresholds (instead of optimal thresholds)         |
## Implementation

### RandomForestClassifier
```python
from sklearn.ensemble import RandomForestClassifier

# Key parameters:
rnd_clf = RandomForestClassifier(
    n_estimators=500,        # Number of trees in the forest
    max_leaf_nodes=16,      # Maximum number of leaf nodes per tree
    n_jobs=-1,             # Use all available CPU cores
    random_state=42       # Random seed for reproducibility
)

rnd_clf.fit(X_train, y_train)
y_pred = rnd_clf.predict(X_test)
```

### Equivalent Bagging Implementation
```python
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

bag_clf = BaggingClassifier(
    DecisionTreeClassifier(max_features="sqrt", max_leaf_nodes=16),
    n_estimators=500,
    n_jobs=-1,
    random_state=42
)
```

## Extra-Trees (Extremely Randomized Trees)

Extra-Trees extend the randomization in Random Forests by:
- Using **random thresholds** for each feature instead of searching for optimal thresholds
- Setting `splitter="random"` in DecisionTreeClassifier

**Advantages**:
- Faster training due to reduced computational cost of finding thresholds
- Often performs better when overfitting is a problem, especially with noisy or high-dimensional data

**Implementation**:
```python
from sklearn.ensemble import ExtraTreesClassifier
extra_clf = ExtraTreesClassifier(n_estimators=500, random_state=42)
```

## Feature Importance

Random Forests provide a built-in measure of **feature importance**:
- **Calculation**: Importance is determined by how much each feature reduces impurity (weighted by the number of samples reaching each node) across all trees
- **Access**: Available through the `feature_importances_` attribute
- **Normalization**: Sum of all feature importances equals 1

**Example**:
```python
from sklearn.datasets import load_iris

iris = load_iris(as_frame=True)
rnd_clf = RandomForestClassifier(n_estimators=500, random_state=42)
rnd_clf.fit(iris.data, iris.target)

for score, name in zip(rnd_clf.feature_importances_, iris.data.columns):
    print(f"{round(score, 2)} {name}")
```

## Advantages and Trade-offs

| Aspect                 | Benefit                                                                                  |
| ---------------------- | ---------------------------------------------------------------------------------------- |
| **Variance Reduction** | Multiple trees with diverse training samples reduce overfitting compared to single trees |
| **Robustness**         | Less sensitive to noise and outliers due to averaging/voting mechanism                   |
| **Feature Handling**   | Can handle mixed feature types and automatically performs feature selection              |

| Limitation       | Description                                                              |
| ---------------- | ------------------------------------------------------------------------ |
| Interpretability | Less interpretable than single decision trees due to ensemble complexity |
| Prediction Time  | Prediction time increases with number of trees (n_estimators)            |
| Memory Usage     | Requires more memory to store multiple trees                             |

## Key Hyperparameters

| Parameter         | Purpose                                                                                         |
| ----------------- | ----------------------------------------------------------------------------------------------- |
| n_estimators      | Number of trees in the forest (more trees = more stable predictions, but increased computation) |
| max_features      | Number of features considered for splitting at each node ("sqrt", "log2", or fraction)          |
| max_depth         | Maximum depth of individual trees                                                               |
| max_leaf_nodes    | Maximum number of leaf nodes per tree (alternative to max_depth)                                |
| min_samples_split | Minimum samples required to split an internal node                                              |
| min_samples_leaf  | Minimum samples required in a leaf node                                                         |

