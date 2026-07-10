## 📌 1. Intuition
- **Lasso (L1 penalty):** shrinks coefficients, can set some to **exactly zero** → does **feature selection**.
- **Ridge (L2 penalty):** shrinks coefficients, but they almost never reach exactly zero → keeps **all features**, but makes their impact smaller.
So Ridge is more like “every feature gets to play, but none of you can be too extreme.”
---
## 📐 2. Formula

The Ridge loss function:
Loss=∑(yi−y^i)2  +  λ∑wj2\text{Loss} = \sum (y_i - \hat{y}_i)^2 \; + \; \lambda \sum w_j^2
- First part = normal squared error.
- Second part = **L2 penalty** (squares of coefficients).
Notice the difference:
- Lasso → ∣w∣|w|
- Ridge → w2w^2
---
## ⚖️ 3. When to use which

- **Ridge:** When you think all features matter, but you want to prevent overfitting. Works well if features are correlated.
- **Lasso:** When you suspect only a few features are truly important (sparse solution).
- **Elastic Net:** A mix of both (balances L1 and L2).
---
## ✅ 4. Pros & Cons

**Ridge**  
✅ Good at reducing variance (overfitting)  
✅ Handles multicollinearity better (when features are correlated)  
❌ Doesn’t do feature selection (keeps all features)

---
## 💻 5. Quick Code (scikit-learn)

```python
from sklearn.linear_model import Ridge
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

# Load example dataset
X, y = load_diabetes(return_X_y=True)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Ridge regression
ridge = Ridge(alpha=1.0)  # alpha = λ
ridge.fit(X_train, y_train)

print("Coefficients:", ridge.coef_)
print("Score:", ridge.score(X_test, y_test))
```

---
