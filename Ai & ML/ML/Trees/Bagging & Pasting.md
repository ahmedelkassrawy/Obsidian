Bagging** (Bootstrap Aggregating) and **pasting** are ensemble methods that train multiple models (e.g., decision trees) on random subsets of the training data.

- **Bagging**: Sampling **with replacement** (some samples may appear multiple times).
- **Pasting**: Sampling without replacement (each sample appears at most once).

> [!note] 
> Both **bagging** and **pasting** allow training instances to be sampled several times across multiple predictors, 
> but only **bagging** allows training instances to be sampled several times for the same predictor.

> [!note] Bagging and Soft Voting  
> A `BaggingClassifier` with decision trees automatically uses **soft voting** if the base classifier supports `predict_proba()` (like decision trees).

Prefer bagging when your dataset is noisy or your model is prone to overfitting (e.g., deep decision tree). Otherwise, prefer pasting as it avoids redundancy during training, making it a bit more computationaly efficient.
#### Code Example: Bagging Classifier

```python
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

# Bagging with decision trees
bag_clf = BaggingClassifier(
    DecisionTreeClassifier(random_state=42),
    n_estimators=500,
    max_samples=1.0,
    bootstrap=True,  # Bagging (True) vs. Pasting (False)
    random_state=42
)
bag_clf.fit(X_train, y_train)
print(f"Bagging accuracy: {bag_clf.score(X_test, y_test):.3f}")
```
---
##### Bagging
- Mitigate Overfitting
- High variance,low bias
- Parrallel on bootstrapped data
- Reduced Variance
##### Boosting
- Migitate Underfiitng
- Low variance,high bias
- Builds on previous result
- Reduced Bias

Both models performed very well. Most of their predictions fall within a standard deviation of the target. Interestingly, random forest "respects" the upper bound (the maximum value) present in the target by staying within its limits, while XGBoost "overshoots", or exceeds this limit.
WHY??

---
### 🌲 Random Forest
- **How it works**: Builds **many decision trees in parallel**, each on a random subset of data + features. Then it averages their predictions (for regression) or takes a majority vote (for classification).
    
- **Behavior**:
    - Since it’s an **average**, predictions are _smoothed_.
    - It rarely predicts outside the range of the training target values (that’s why you saw it "respect" the upper bound).
    - Tends to be more **conservative**.
---
### ⚡ XGBoost (Extreme Gradient Boosting)
- **How it works**: Builds trees **sequentially**, each one trying to fix the errors of the previous ones (boosting).
    
- **Behavior**:
    - Can capture more complex patterns.
    - Because it’s aggressively trying to minimize errors, it sometimes **overshoots** beyond the target range.
    - Tends to be more **flexible** (but riskier if not regularized properly).
---
### ✅ Key differences in your case:

- **Random Forest** → safer, bounded, lower risk of extreme predictions.
- **XGBoost** → can give sharper predictions, sometimes beyond training limits (great if your test data has values beyond what you trained on, but risky otherwise).
---
**Why Random Forest makes sense here:**
- It generalizes better when you want **safe, bounded predictions**.
- Less prone to overfitting than boosting methods (unless you have _tons_ of data and careful tuning).
- Works really well as a strong baseline model in many tasks.

That said, **XGBoost** can outperform Random Forest if:
- You carefully tune hyperparameters (learning rate, max depth, regularization).
- You _expect_ values beyond your training range (so "overshooting" is actually a good thing).

- **Random Forest → Bagging**  
    → Many trees trained _independently_ on random subsets of data + features, then averaged together.
    
- **XGBoost → Boosting**  
    → Trees are trained _sequentially_, each new one correcting mistakes of the previous.