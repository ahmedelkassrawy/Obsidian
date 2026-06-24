```python
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import matplotlib.pyplot as plt

X = churn_df[["total_day_charge","total_eve_charge"]].values #each column is a feature and each row a different observation
y = churn_df["churn"].values #.values to convert X and y into numpy arrays

knn = KNeighborsClassifier(n_neighbors=15)
knn.fit(X,y)

X_new=np.array([[56.8,17.5],
                [24.4,24.1],
                [50.1,10.9]])

predictions = knn.predict(X_new)

#measruing perfermonce and accuracy of model # Import the module
from sklearn.model_selection import train_test_split

X = churn_df.drop("churn", axis=1).values
y = churn_df["churn"].values
  
# Split into training and test sets
X_train, X_test, y_train, y_test = 
train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

knn = KNeighborsClassifier(n_neighbors=5)

# Fit the classifier to the training data
knn.fit(X_train,y_train)

# Print the accuracy
print(knn.score(X_test, y_test))  

#experminting different values of k to get the best accuracy available
# Create neighbors
neighbors = np.arange(1, 13)
train_accuracies = {}
test_accuracies = {}
  
for neighbor in neighbors:
    # Set up a KNN Classifier
    knn = KNeighborsClassifier(n_neighbors=neighbor)
    # Fit the model
    knn.fit(X_train, y_train)
    # Compute accuracy
    train_accuracies[neighbor] = knn.score(X_train, y_train)
    test_accuracies[neighbor] = knn.score(X_test, y_test)
print(neighbors, '\n', train_accuracies, '\n', test_accuracies)

#plotting the results to choose the k value wisely
# Add a title
plt.title("KNN: Varying Number of Neighbors")

# Plot training accuracies
plt.plot(neighbors, train_accuracies.values(), label="Training Accuracy")
# Plot test accuracies
plt.plot(neighbors, test_accuracies.values(), label="Testing Accuracy")

plt.legend()
plt.xlabel("Number of Neighbors")
plt.ylabel("Accuracy")
# Display the plot
plt.show()
```
### 1. Intuition (the “big picture”)

KNN is a **lazy learning algorithm**. Instead of learning an explicit model (like linear regression does), it just _stores the training data_.  
When it sees a new data point, it asks:  
👉 “Who are my closest neighbors?”

- If it’s a **classification problem**, it picks the majority vote of those neighbors.
- If it’s a **regression problem**, it averages their values.

So it’s like: if you move to a new city, your personality might be guessed by the people living closest to you.

💡 Question for you: imagine we have points on a 2D plane representing students, labeled “likes football” ⚽ or “likes chess” ♟️. If we add a new student, how do you think KNN decides their label?

---
### 2. Mechanics (step by step)

For classification:
1. Choose a number **k** (say k=3).
2. Measure distance (usually **Euclidean**) between the new point and all training points.
3. Pick the **k closest points**.
4. Take the majority label among them → that’s the prediction.
For regression, same idea but instead of voting, it takes the **mean of neighbors’ values**.
---
### 3. Using it in ML

- **Good for:** small datasets, when decision boundaries are irregular.
- **Not good for:** huge datasets (because you must compare against _all_ training points each time).
- **Feature scaling matters!** Because KNN uses distance, features should usually be normalized (e.g., StandardScaler or MinMaxScaler).

---
### 4. Pros & Cons
✅ Simple & intuitive  
✅ No training time (just stores data)  
❌ Slow at prediction time for large datasets  
❌ Sensitive to irrelevant features and scaling  
❌ Choice of k can change results a lot

---
### 5. Tuning
- **k**: small k → more flexible but noisy; large k → smoother but may miss local patterns.
- **Distance metric**: Euclidean, Manhattan, Minkowski, cosine similarity, etc.
- **Weighting neighbors**: sometimes closer neighbors are weighted more heavily.
---
### 6. Quick Code (with scikit-learn)

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Load data
X, y = load_iris(return_X_y=True)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train KNN
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

# Predict
y_pred = knn.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
```

---
What is the primary purpose of scaling features before applying k-NN?
- To ensure all features contribute equally to the distance measure
- Scaling ensures that no single feature unfairly influences the distance metric.