### 2. **Tackling a Regression Problem (Workflow)**

1. **Data Exploration (EDA)**
    - Check distributions, correlations, missing values
    - Visualize features vs target.
2. **Preprocessing**
    - Handle missing values.
    - Scale/normalize if models need it (e.g. Linear Regression, KNN, Neural Nets).
    - Encode categoricals (OneHot, Target Encoding).
3. **Baseline Model**
    - Start simple (e.g. mean predictor or Linear Regression) to have a benchmark.
4. **Model Selection (see below)**
    - Try multiple families of models and compare.
5. **Evaluation**
    - Use metrics like **MSE, RMSE, MAE, R²** depending on the problem.
    - Cross-validation to avoid overfitting.
6. **Model Improvement**
    - Feature engineering, regularization, ensembles.

```python
df
df.isna().sum(0
df.info()
df.describe()
df.duplicated()
df.duplicated().value_counts()
df.drop_duplicates(inplace = True)
df.drop(["ids","flag","date","user"],axis=1,inplace = True)
df.rename(columns = {0:"target"},inplace = True)
```

### 3. **Which Models and When**
Here’s a mental map:
#### 🔹 **Linear Models**
- **Linear Regression**: when relationship looks roughly linear.
- **Ridge / Lasso / ElasticNet**: when you want regularization or have many correlated features.
    - Lasso = feature selection.
    - Ridge = keeps all features but shrinks weights.
#### 🔹 **Tree-based Models**
- **Decision Trees**: interpretable, but can overfit.
- **Random Forests**: strong baseline, robust, handles non-linearities.
- **Gradient Boosting (XGBoost, LightGBM, CatBoost)**: usually best performance on tabular data.
    - Works well with mixed feature types, handles missing values.
#### 🔹 **Non-parametric / Instance-based**
- **KNN Regression**: simple, but not great with high dimensions. Useful for small datasets.
#### 🔹 **Neural Networks**
- **MLPs**: only if you have _lots_ of data and non-linear relationships.
- Not always better than boosting on structured/tabular data.
#### 🔹 **Specialized**
- **Support Vector Regression (SVR)**: good for small datasets, but not scalable.
- **Polynomial Regression**: if relationship is nonlinear but can be expressed as polynomial.
---
### 4. **Rule of Thumb**
- **Start simple → go complex only if needed.**
- **Small data (<10k rows)** → Linear + Ridge/Lasso, SVR, simple trees.
- **Medium/Large tabular data** → Random Forest, Gradient Boosting (XGBoost/LightGBM).
- **Huge dataset + complex patterns** → Neural Nets.

## 🔹 Why Scale at All?

Some models **look at distances** or **assume features are on similar ranges**.  
Others (like trees) **don’t care at all** about scaling.

So the rule is: _scale only when the algorithm is sensitive to feature magnitude_.

---

## 🔹 The Main Methods

1. **Standardization (Z-score)**  
    Formula:
    
    x′=x−μσx' = \frac{x - \mu}{\sigma}x′=σx−μ​
    
    → Mean = 0, Std Dev = 1.
    
    ✅ Best when data looks roughly Gaussian.  
    ✅ Used in **Linear Regression, Logistic Regression, SVM, Neural Nets, PCA**.
    

---

2. **Min-Max Scaling (Normalization)**  
    Formula:
    
    x′=x−min⁡(x)max⁡(x)−min⁡(x)x' = \frac{x - \min(x)}{\max(x) - \min(x)}x′=max(x)−min(x)x−min(x)​
    
    → Values between [0, 1].
    
    ✅ Good when you need bounded inputs.  
    ✅ Used in **KNN, Neural Nets, Distance-based models**.  
    ❌ Sensitive to outliers (they squash everything).
    

---

3. **Robust Scaler**  
    Formula:
    
    x′=x−medianIQRx' = \frac{x - \text{median}}{IQR}x′=IQRx−median​
    
    → Based on median and interquartile range.
    
    ✅ Best when data has **outliers**.  
    ✅ Works in the same places as StandardScaler, but safer.
    

---

4. **Log Transform / Power Transform**  
    ✅ For highly skewed features (e.g. incomes, sales amounts).  
    ✅ Often used **before** applying StandardScaler or MinMax.
    

---

## 🔹 Which Models Need Scaling?

- **Need scaling (distance/gradient based)**
    
    - KNN, K-means, SVM, Logistic/Linear Regression, Neural Nets, PCA
        
- **Don’t care about scaling**
    
    - Decision Trees, Random Forest, Gradient Boosting (XGBoost, LightGBM, CatBoost)
        

---

## 🔹 Quick Rules of Thumb

- If using **trees** → don’t bother scaling.
    
- If using **linear models / SVM / neural nets** → StandardScaler (default).
    
- If using **distance-based models (KNN, K-means)** → MinMaxScaler (or StandardScaler).
    
- If data has **outliers** → RobustScaler.