---
description: "Explains Lasso regression: how the L1 penalty shrinks some coefficients to exactly zero, giving regularization and feature selection at once, with scikit-learn code."
domain: ml
type: concept
status: digested
tags:
  - domain/ml
  - type/concept
  - status/digested
  - topic/regression
  - topic/regularization-and-overfitting
aliases:
  - "Lasso"
  - "L1 penalty"
  - "feature selection"
hubs:
  - "[[Regression]]"
  - "[[Regularization & Overfitting]]"
---
## 📌 1. Intuition

Ordinary Linear Regression tries to fit a line (or hyperplane) that minimizes the sum of squared errors.  
But sometimes:
- Too many features → overfitting.
- Some features aren’t useful.
👉 **Lasso Regression** helps by adding a **penalty term** that can **shrink coefficients** — and even force some to become **exactly zero**.  
This way, it does both **regularization** (preventing overfitting) and **feature selection**.

---
## 📐 2. The Formula

The cost function for Lasso is:
Loss=∑(yi−y^i)2  +  λ∑∣wj∣\text{Loss} = \sum (y_i - \hat{y}_i)^2 \; + \; \lambda \sum |w_j|
- First part = regular squared error.
- Second part = **L1 penalty** (absolute value of coefficients).
- λ\lambda controls how strong the penalty is:
    - λ=0\lambda = 0 → same as linear regression.
    - Large λ\lambda → more shrinkage, more coefficients pushed to 0.
---

## ⚖️ 3. Why it’s useful

- Helps when we have **many features** and only some are important.
- Good for **interpretability** → zero coefficients = irrelevant features dropped.
---
## ✅ 4. Pros & Cons

✅ Reduces overfitting  
✅ Automatically selects features (some weights become zero)  
✅ Works well when only a few features are actually useful  
❌ If features are highly correlated, it might arbitrarily pick one and ignore the rest  
❌ Doesn’t handle situations well where _all_ features matter

---
## 🛠️ 5. Quick Code (scikit-learn)

```python
from sklearn.linear_model import Lasso
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

# Load example dataset
X, y = load_diabetes(return_X_y=True)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Lasso regression
lasso = Lasso(alpha=0.1)  # alpha = λ
lasso.fit(X_train, y_train)

print("Coefficients:", lasso.coef_)
print("Score:", lasso.score(X_test, y_test))
```

---
If λ\lambda (alpha) is set **very high** in Lasso, what do you think happens to most of the coefficients?

When λ\lambda (or `alpha` in sklearn) is **very high** in Lasso:
- The penalty term dominates.
- Most coefficients get **shrunk heavily toward 0**.
- Some become **exactly 0** → meaning those features are completely dropped.
So the model becomes very simple — maybe even underfitting, because it’s ignoring too many features.
---
👉 Quick recap trick:
- **Small λ → behaves like Linear Regression (keeps all features).**
- **Medium λ → shrinks some, drops others (feature selection).**
- **Huge λ → almost all coefficients = 0 (very simple/underfit model).**
---