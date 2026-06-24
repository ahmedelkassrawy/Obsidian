## 🔗 Elastic Net Regression
### 1. Intuition
Elastic Net is like saying:  
👉 “I want the **feature selection power of Lasso** _and_ the **stability of Ridge**.”

It combines both penalties:
- L1 (absolute values, like Lasso)
- L2 (squared values, like Ridge)
So it can drop some coefficients to **zero** (like Lasso), while also shrinking others (like Ridge).
---
### 2. Formula
The cost function looks like:

Loss=∑(yi−y^i)2+λ1∑∣wj∣+λ2∑wj2\text{Loss} = \sum (y_i - \hat{y}_i)^2 + \lambda_1 \sum |w_j| + \lambda_2 \sum w_j^2

Or in scikit-learn style:

Loss=MSE+α(l1_ratio⋅∥w∥1+(1−l1_ratio)⋅∥w∥22)\text{Loss} = \text{MSE} + \alpha \big( l1\_ratio \cdot \|w\|_1 + (1-l1\_ratio)\cdot \|w\|_2^2 \big)

- `alpha` = overall regularization strength.
- `l1_ratio` = balance between Lasso and Ridge (0 = pure Ridge, 1 = pure Lasso).
---
### 3. When to use
- When you have **lots of features**, some of which are irrelevant.
- When features are **highly correlated**.
- If you’re not sure whether to choose Ridge or Lasso → Elastic Net is often a safer middle ground.
---
### 4. Quick Code (scikit-learn)

```python
from sklearn.linear_model import ElasticNet
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

# Load example dataset
X, y = load_diabetes(return_X_y=True)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Elastic Net
elastic = ElasticNet(alpha=0.1, l1_ratio=0.5)  # 0.5 = equal mix of L1 & L2
elastic.fit(X_train, y_train)

print("Coefficients:", elastic.coef_)
print("Score:", elastic.score(X_test, y_test))
```

---
### 5. Pros & Cons
✅ Combines feature selection + shrinkage  
✅ More robust than Lasso if features are correlated  
✅ Can adapt between Ridge and Lasso  
❌ Needs tuning of two parameters (alpha and l1_ratio)  
❌ Less interpretable than pure Lasso or Ridge

---
