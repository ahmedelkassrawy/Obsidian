##### Ensemble Methods
- Techniques that create multiple models and then combine them to produce improved results.
- The key idea is that a group of models working together (an ensemble) can outperform an individual model. 
- These methods can be divided into two main categories: **Bagging and Boosting**
#### Bagging
- an ensemble technique where multiple versions of a model are trained on different subsets of the training data.
- The predictions from these models are then combined to improve the overall performance.
- Bagging works particularly well with high-variance models, like decision trees, as it helps reduce overfitting

- Involves creating multiple subsets of data from the original dataset **using**
**sampling with replacement** (each subset can have repeated samples).
- Each subset is used to train **different models** (e.g., Decision Trees, SVM,
etc.), and their predictions are **aggregated.**
- For regression problems, predictions are **averaged (mean),** 
- while for classification problems, the majority vote is **taken (voting).**
- Goal: **Reduces overfitting,** increases model robustness, and improves
accuracy by averaging multiple models rather than relying on a single
one

##### Random Forest
- An extension of Bagging specifically for Decision Trees.
- Constructs multiple decision trees during training and outputs the mode of the classes (classification) or mean prediction (regression).
- Each tree votes for the class and the final prediction is made based on the
majority vote.
- Helps handle overfitting and variance by using many weak learners (decision
trees) to create a strong ensemble model

Voting 
- For classification, we use **majority voting**. 
- There is hard voting, where each model's prediction is considered **equal**
- soft voting, where each model’s predicted probabilities are **averaged**

![[Pasted image 20260316215755.png]]

Trade-offs and Performance
At increasing the number of estimators (trees in Random Forests)
- Pro: Improves performance and reduces overfitting by increasing model variance.
- Con: Increasing estimators comes with a trade-off in computational cost and time. After a certain point, adding more estimators does not provide a significant performance boost.

---
#### Boosting
- Boosting is an ensemble technique that focuses on training weak learners sequentially, with each learner improving upon the mistakes made by the previous one.
- The final output is a weighted combination of the weak learners. Boosting algorithms aim to **reduce bias and improve the overall performance of a model**

AdaBoost (Adaptive Boosting)
- AdaBoost is one of the simplest and most popular boosting algorithms. The main idea behind
- AdaBoost is to combine multiple weak learners (usually decision trees with a single split, known as "decision stumps") to form a strong classifier
![[Pasted image 20260316221005.png]]

How it works ?
Step 1
- It starts by assigning equal weights to all the training data points.
Step 2
- A weak learner (like a shallow decision tree) is trained on the data. After training, misclassified samples are given higher weights, meaning the next model will focus more on these difficult cases
Step 3
- Another weak learner is trained with these updated weights, emphasizing the misclassified data from the previous learner.
Step 4
- This process repeats for a certain number of iterations or until no significant improvements are made
Step 5
- In the final prediction, each weak learner gets a weight based on its performance, and the results of all learners are combined (usually by a weighted majority vote)

Advantages
- Focuses on difficult-to-classify samples.
- Simple to implement and works well with many weak learners.
Disadvantages
- Can be sensitive to noise in the data (as noisy data may
get higher weights, causing the model to overfit)

Gradient Boosting
- Gradient Boosting takes a different approach than AdaBoost. 
- Instead of adjusting weights for misclassified data, Gradient Boosting builds new learners to predict the residual errors made by the previous learners. 
- It uses a technique called gradient descent to minimize errors

Step 1
- A model (usually a weak learner like a decision tree) is trained on the dataset.
Step 2
- After the first learner makes predictions, we calculate the errors (residuals) between the true labels and the predicted labelsgradient descent to minimize errors
Step 3 
- The next learner is trained to predict these residuals, focusing on the mistakes made by the previous model. 
Step 4 
- This process continues, with each new learner reducing the errors of the previous one, making the model improve step by step.
Step 5
Finally, all learners' predictions are combined to make a final prediction

Advantages 
- Very powerful and flexible, works well with a variety of data types.
- Minimizes both bias and variance if tuned properly.  
Disadvantages 
- Slow training process compared to AdaBoost. 
- More complex to implement

XGBoost (Extreme Gradient Boosting)
- XGBoost is an advanced implementation of Gradient Boosting. 
- It's designed to be fast, efficient, and highly scalable. 
- XGBoost introduces various improvements, making it one of the best performing and widely used algorithms in machine learning competitions like Kaggle.

How it works ? 
Optimized Gradient Boosting: Just like Gradient Boosting, XGBoost works by sequentially adding models to predict residuals, but with several optimizations

Key Improvements 
1. Regularization 
XGBoost applies L1 (Lasso) and L2 (Ridge) regularization to reduce overfitting

2. Parallelized Training 
- It uses parallel and distributed computing, which makes it faster than traditional gradient boosting

3. Tree Pruning 
XGBoost uses advanced tree pruning techniques to prevent overly complex models that overfit the training data

4. Handling Missing Data 
XGBoost has in-built methods to handle missing data, making it more robust

5. Weighted Voting 
Instead of just adding models, XGBoost calculates the optimal weight for each learner, further improving the overall performance

6. Learning Rate 
XGBoost applies a learning rate (shrinkage) after each step to control how much each new model influences the overall prediction, preventing overfitting

Advantages 
- Fast and efficient due to its optimizations. 
- Handles large datasets with many features efficiently. 
- Great at reducing overfitting due to its regularization techniques. 
 
Disadvantages 
- Requires tuning a larger number of hyperparameters compared to simpler models. 
- Can be complex to understand for beginners

![[Pasted image 20260316222135.png]]

Practical Use Cases 
- AdaBoost: Best used when you need a simple yet effective boosting technique, particularly when noise in the dataset is minimal. 
- Gradient Boosting: Great for tabular data, where you need a highly powerful model with flexibility. Works well for both classification and regression problems. 
- XGBoost: Preferred for large datasets and in competitions like Kaggle where speed and accuracy matter the most. It's particularly useful when overfitting is a concern due to its regularization features

![[Pasted image 20260316222208.png]]

---
#### Bagging with Decision Trees

```python
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Step 3: Initialize a Decision Tree Classifier
dtree = DecisionTreeClassifier()

# Step 4: Create a BaggingClassifier using the Decision Tree as the base estimator
bagging_clf = BaggingClassifier(estimator=dtree, 
							n_estimators=50, 
							random_state=42)
							
# Step 5: Train the BaggingClassifier on the training data
bagging_clf.fit(X_train, y_train)

# Step 6: Make predictions on the test data
y_pred = bagging_clf.predict(X_test)

# Step 7: Evaluate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy of Bagging with Decision Tree: {accuracy:.2f}")

# Step 8: Feature Importance from one Decision Tree in the Bagging Classifier (You can't use bagging_clf directly)

dtree_fitted = bagging_clf.estimators_[0]  # Access the first fitted DecisionTree from the bagging ensemble
feature_importances = dtree_fitted.feature_importances_
```

#### Bagging with KNN
```python
# Import necessary libraries
from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Step 3: Initialize a K-Nearest Neighbors Classifier
knn = KNeighborsClassifier(n_neighbors=5)

# Step 4: Create a BaggingClassifier using the KNN as the base estimator
bagging_clf_knn = BaggingClassifier(estimator=knn, n_estimators=50, random_state=42)

# Step 5: Train the BaggingClassifier on the training data
bagging_clf_knn.fit(X_train, y_train)

# Step 6: Make predictions on the test data
y_pred_knn = bagging_clf_knn.predict(X_test)

# Step 7: Evaluate the accuracy of the model
accuracy_knn = accuracy_score(y_test, y_pred_knn)
print(f"Accuracy of Bagging with KNN: {accuracy_knn:.2f}")

# Step 8: Visualize the accuracy of different numbers of estimators
import matplotlib.pyplot as plt
n_estimators_range = range(10, 100, 10)
accuracy_values = []

# Try different numbers of estimators to visualize performance
for n in n_estimators_range:
    bagging_clf_knn = BaggingClassifier(estimator=knn, n_estimators=n, random_state=42)
    bagging_clf_knn.fit(X_train, y_train)
    y_pred_knn = bagging_clf_knn.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred_knn)
    accuracy_values.append(accuracy)
    
# Plotting the accuracy vs number of estimators
plt.plot(n_estimators_range, accuracy_values, marker='o')
plt.title("Accuracy for Different Numbers of Estimators (KNN Bagging)")
plt.xlabel("Number of Estimators")
plt.ylabel("Accuracy")
plt.show()
```
---
#### Boosting
Adaboost
```python
# Initialize the AdaBoost classifier
ada_clf = AdaBoostClassifier(n_estimators=50, learning_rate=1.0, random_state=42)

# Train the AdaBoost model
ada_clf.fit(X_train_scaled, y_train)

# Predict on the test set
y_pred_ada = ada_clf.predict(X_test_scaled)

# Evaluate AdaBoost model performance
print("AdaBoost Model Performance:")
print("Accuracy:", accuracy_score(y_test, y_pred_ada))
print("Classification Report:\n", classification_report(y_test, y_pred_ada))

# Plot Confusion Matrix
plt.figure(figsize=(5, 4))
sns.heatmap(confusion_matrix(y_test, y_pred_ada), annot=True, fmt='d', cmap='Blues')
plt.title('AdaBoost Confusion Matrix')
plt.show()
```

Gradient Boosting
```python
# Initialize the Gradient Boosting classifier
gb_clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)

# Train the Gradient Boosting model
gb_clf.fit(X_train_scaled, y_train)

# Predict on the test set
y_pred_gb = gb_clf.predict(X_test_scaled)

# Evaluate Gradient Boosting model performance
print("Gradient Boosting Model Performance:")
print("Accuracy:", accuracy_score(y_test, y_pred_gb))
print("Classification Report:\n", classification_report(y_test, y_pred_gb))

# Plot Confusion Matrix
plt.figure(figsize=(5, 4))
sns.heatmap(confusion_matrix(y_test, y_pred_gb), annot=True, fmt='d', cmap='Oranges')
plt.title('Gradient Boosting Confusion Matrix')
plt.show()
```

XGBoost
```python
# Initialize the XGBoost classifier
xgb_clf = XGBClassifier(n_estimators=100, learning_rate=0.1, random_state=42)

# Train the XGBoost model
xgb_clf.fit(X_train_scaled, y_train)

# Predict on the test set
y_pred_xgb = xgb_clf.predict(X_test_scaled)

# Evaluate XGBoost model performance
print("XGBoost Model Performance:")
print("Accuracy:", accuracy_score(y_test, y_pred_xgb))
print("Classification Report:\n", classification_report(y_test, y_pred_xgb))

# Plot Confusion Matrix
plt.figure(figsize=(5, 4))
sns.heatmap(confusion_matrix(y_test, y_pred_xgb), annot=True, fmt='d', cmap='Greens')
plt.title('XGBoost Confusion Matrix')
plt.show()
```

Comparing the models
```python
# Compare the accuracy of all models
models = ['AdaBoost', 'Gradient Boosting', 'XGBoost']
accuracies = [accuracy_score(y_test, y_pred_ada),
              accuracy_score(y_test, y_pred_gb),
              accuracy_score(y_test, y_pred_xgb)]

plt.figure(figsize=(8, 5))
plt.bar(models, accuracies, color=['blue', 'orange', 'green'])
plt.title('Comparison of Model Accuracies')
plt.ylabel('Accuracy')
plt.show()
```