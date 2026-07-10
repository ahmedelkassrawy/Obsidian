#### Decision Trees
- Used for both regression and classification
- The key idea is to split the dataset into smaller subsets based on feature values
- This process continues until a stopping condition is met (for example, no further splitting is possible, or maximum depth is reached).

The result is a tree structure:
- **Nodes** = represent tests on features
- **Branches** = represent the outcome of those tests
- **Leaves** = represent class labels (for classification tasks) or continuous values (for regression tasks)

![[Pasted image 20260306141943.png]]
##### Key Concepts: 
- **Root Node** = topmost node in a tree , initial decision
- **Leaf nodes** = terminal nodes that hold the output class labels or values
- **Splitting** = process of dividing nodes into sub-nodes based on a feature
- **Pruning** = Reduce the size of the tree to prevent overfitting by trimming branches

**How to determine the best split?**
Using a **node impurity measure** - an indicator of how well data at a node is classified or how "pure" a node is.

---
## Decision Trees: Gini Index (Gini Impurity)
- The **Gini Index** (or Gini Impurity) is a metric used in decision trees to evaluate the quality of a split. 
- It measures the probability that a randomly chosen sample from a node would be misclassified if it were randomly assigned a label according to the distribution of classes in that node.

### The Formula
To calculate the Gini Impurity for a node, use the following formula:

$$Gini = 1 - \sum_{i=1}^{C} p_i^2$$

- $C$ represents the total number of classes.    
- $p_i$ is the probability of an instance belonging to class $i$ at that specific node.
### Interpreting the Gini Index
The goal of a decision tree is to **minimize impurity**, meaning it wants to create leaf nodes where all samples belong to exactly one class.

- **Perfectly Pure (Low Impurity):** A Gini Index of $0.0$ means the node is perfectly pure (e.g., 100% of the samples belong to Class A). A heavily skewed distribution, such as 90% Class A and 10% Class B, will yield a very low Gini Impurity.
    
- **High Impurity:** A Gini Index of $0.5$ is the maximum possible impurity for a binary classification problem. This happens when the classes are perfectly balanced (e.g., 50% Class A and 50% Class B), making it the most unpredictable state.
---
### Step-by-Step Example Calculation
Let's look at the example provided in your slides for a single node containing 100 samples divided into two classes:
- **Class A:** 70 samples
- **Class B:** 30 samples

**Step 1: Calculate the probabilities ($p_i$) for each class.**
- Probability of Class A ($p_A$): $70 / 100 = 0.7$
- Probability of Class B ($p_B$): $30 / 100 = 0.3$
    
**Step 2: Apply the Gini formula.**
$$Gini = 1 - (p_A^2 + p_B^2)$$
$$Gini = 1 - (0.7^2 + 0.3^2)$$
$$Gini = 1 - (0.49 + 0.09)$$
$$Gini = 1 - 0.58 = 0.42$$
**Conclusion:** The Gini Index of this node is **$0.42$**, which indicates a moderate level of impurity.

---
### How Decision Trees Use Gini Impurity

When a decision tree is building its branches, it **evaluates multiple potential features to split the data** (like Age, Income, Student status, or Credit Rating).

The algorithm calculates the weighted average of the Gini Impurity for the child nodes created by each possible split. It then selects the feature that results in the **lowest** overall Gini Impurity, as this represents the "Best" split that organizes the data into the purest possible groups.

---
## Decision Tree: Entropy (Information Gain)
**Entropy** measures the uncertainty or disorder in a node. The more mixed the classes are at a node, the higher the entropy.

### The Formula

$$Entropy(p) = -\sum_{i=1}^{n} p_i \log_2(p_i)$$
_Where $p_i$ is the probability of an instance belonging to class $i$._
### Interpreting Entropy Values
Entropy typically ranges from 0 to 1 (for binary classification):

- **0** is considered a **pure** sub-tree (all samples belong to a single class).
- **1** is considered the **most impure** sub-tree (an exactly even split of classes).

|**Impurity Level**|**Class A**|**Class B**|
|---|---|---|
|**High Entropy ($\approx 1$)**|50%|50%|
|**Low Entropy ($\approx 0$)**|100%|0%|

---
### Example 1: Basic Node Calculation
Let’s consider a node that contains 100 samples. These samples belong to two classes:
- 70 samples of Class A
- 30 samples of Class B
    
**1. Calculate the probabilities:**
- Probability of Class A ($p_A$): $70 / 100 = 0.7$
- Probability of Class B ($p_B$): $30 / 100 = 0.3$

**2. Calculate the Entropy:**
$$Entropy = -(0.7 \log_2(0.7) + 0.3 \log_2(0.3))$$
$$Entropy = -(0.7 \times -0.5146 + 0.3 \times -1.736)$$
$$Entropy = 0.88$$
**Conclusion:** The entropy of this node is **0.88**, which is closer to 1, indicating higher impurity. If this node successfully split the classes completely (e.g., separating all 70 Class A and all 30 Class B into their own child nodes), the resulting child nodes would both have an entropy of **0.0**.

---
### Example 2: Calculating Sub-tree Entropy
Consider a Root Node (Node A) containing **7 "Yes"** and **5 "No"** samples. It splits into two child nodes:

**Node B (2 Yes, 4 No):**
To find the entropy of Node B, we use the fractions of the total samples in that specific node ($2+4=6$ total samples).

$$Entropy(B) = -\frac{2}{6} \log_2\left(\frac{2}{6}\right) - \frac{4}{6} \log_2\left(\frac{4}{6}\right)$$

$$Entropy(B) = 0.92 \text{ bits}$$

**Node C (5 Yes, 1 No):**
Doing the same for Node C ($5+1=6$ total samples).
$$Entropy(C) = -\frac{5}{6} \log_2\left(\frac{5}{6}\right) - \frac{1}{6} \log_2\left(\frac{1}{6}\right)$$
$$Entropy(C) = 0.65 \text{ bits}$$
**Conclusion:** Node B ($0.92$) is much more impure/mixed than Node C ($0.65$). The decision tree uses these entropy values to calculate Information Gain and determine if this split was the best possible choice.

---

| **Feature**                           | **Gini Index (Gini Impurity)**                                                 | **Entropy**                                                           |
| ------------------------------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------- |
| **Core Concept**                      | Measures the probability that a randomly chosen sample would be misclassified. | Measures the level of uncertainty, disorder, or "surprise" in a node. |
| **Formula**                           | $1 - \sum_{i=1}^{C} p_i^2$                                                     | $-\sum_{i=1}^{C} p_i \log_2(p_i)$                                     |
| **Max Value (Binary Classification)** | **0.5** (when the node is exactly 50/50 split)                                 | **1.0** (when the node is exactly 50/50 split)                        |
| **Min Value (Pure Node)**             | **0.0** (all samples belong to one class)                                      | **0.0** (all samples belong to one class)                             |
| **Computational Speed**               | **Faster**                                                                     | **Slower**.                                                           |
| **Behavior with Splits**              | Tends to isolate the most frequent class in its own branch.                    | Tends to produce slightly more balanced trees.                        |

- Gini Index -> Measures the prob of misclassification
- Entropy -> Measures the level of uncertainty
- Misclassification Error -> Proportion of samples that are misclassified
---
#### Naive Bayes
It's called "naive" because it assumes that all features are independent of each other

Types of Naive Bayes Classifiers:
1. **Gaussian Naive Bayes**: Assumes that the continuous features follow a normal (Gaussian) distribution. 
2. **Multinomial Naive Bayes**: Used for discrete counts, such as in **text classification.** 
3. **Bernoulli Naive Bayes**: Suitable for **binary/boolean** features.

Advantages and Disadvantages of Naive Bayes 
	Advantages of Naive Bayes 
		1. **Works Well on Small Datasets**: Naive Bayes can perform well even with small amounts of training data. 
		2. **Handles Irrelevant Features**: Since Naive Bayes assumes that features are independent, it can effectively ignore irrelevant features, meaning their presence doesn't negatively impact the model's performance

Disadvantages of Naive Bayes
	1. **Assumes Feature Independence**: In the real world, features are often correlated, which violates the independence assumption made by Naive Bayes. This can lead to suboptimal performance in situations where feature interactions are important. 
	2. **Not Generalized for Complex Data**: The model may fail to generalize well if the data structure is complex and the relationships between features are not truly independent.

```python
# Step 3: Create a Gaussian Naive Bayes classifier
gnb = GaussianNB()

gnb.fit(X_train, y_train)
y_pred = gnb.predict(X_test)

accuracy = metrics.accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

conf_matrix = metrics.confusion_matrix(y_test, y_pred)
class_report = metrics.classification_report(y_test, y_pred)
```