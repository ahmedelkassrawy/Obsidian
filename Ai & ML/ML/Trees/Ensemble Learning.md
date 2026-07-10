As an example of an ensemble method, you can train a group of decision tree classifiers, each on a different random subset of the training set. You can then obtain the predictions of all the individual trees, and the class that gets the most votes is the ensemble’s prediction
Such an ensemble of decision trees is called a random forest, and despite its simplicity, this is one of the most powerful machine learning algorithms available today

There are some downsides, however: ensemble learning requires much more computing resources than using a single model (both for training and for inference), it can be more complex to deploy and manage, and the predictions are harder to interpret. But the pros often outweigh the cons

This majority-vote classifier is called a hard voting classifier
Somewhat surprisingly, this voting classifier often achieves a higher accuracy than the
 best classifier in the ensemble. In fact, even if each classifier is a weak learner (meaning
 it does only slightly better than random guessing), the ensemble can still be a strong
 learner (achieving high accuracy), provided there are a sufficient number of weak
 learners in the ensemble and they are sufficiently diverse (i.e., if they focus on different
 aspects of the data and make different kinds of errors).

 Ensemble methods work best when the predictors are as independent from one another as possible. One
 way to get diverse classifiers is to train them using very different algorithms. This increases the chance that
 they wil make very different types of errors, improving the ensemble’s accuracy. You can also play with
 the model hyperparameters to get diverse models, or train the models on different subsets of the data, as
 we wil see.

---
## Ensemble Methods
Ensemble methods combine multiple models to improve performance, reduce variance, and enhance generalization. Two common approaches are **voting classifiers** and **bagging**.

### Voting Classifiers
A **voting classifier** aggregates predictions from multiple classifiers (e.g., logistic regression, random forest, SVM) and selects the class with the most votes (**hard voting**) or the highest average probability (**soft voting**).

- **Hard Voting**: Predicts the class with the most votes from individual classifiers.
- **Soft Voting**: Predicts the class with the highest average probability across classifiers, often outperforming hard voting by weighting confident predictions.

> [!note] Soft Voting Requirement  
> All classifiers must have a `predict_proba()` method. For SVC, set `probability=True` (uses cross-validation, slower training).

#### Code Example: Voting Classifier

```python
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_moons

# Sample data
X, y = make_moons(n_samples=100, noise=0.15, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Voting classifier
voting_clf = VotingClassifier(
    estimators=[
        ('lr', LogisticRegression(random_state=42)),
        ('rf', RandomForestClassifier(random_state=42)),
        ('svc', SVC(random_state=42))
    ],
    voting='hard'
)
voting_clf.fit(X_train, y_train)

# Evaluate individual classifiers
for name, clf in voting_clf.named_estimators_.items():
    print(f"{name} accuracy: {clf.score(X_test, y_test):.3f}")

# Hard voting accuracy
print(f"Hard voting accuracy: {voting_clf.score(X_test, y_test):.3f}")

# Switch to soft voting
voting_clf.voting = 'soft'
voting_clf.named_estimators['svc'].probability = True
voting_clf.fit(X_train, y_train)
print(f"Soft voting accuracy: {voting_clf.score(X_test, y_test):.3f}")
```

#### Output Example

```
lr accuracy: 0.864
rf accuracy: 0.896
svc accuracy: 0.896
Hard voting accuracy: 0.912
Soft voting accuracy: 0.920
```

> [!info] Why Voting Works  
> Combining diverse classifiers reduces errors, as they make uncorrelated mistakes. Soft voting often outperforms hard voting by leveraging probability confidence.
