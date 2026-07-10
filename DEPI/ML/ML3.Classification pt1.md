#### Logistic regression 
Logistic Regression is a supervised learning classification algorithm used to predict the probability of a categorical target variable. 
It deals with discrete classes like Yes or No, 0 or 1, True or False

S-curve
This sigmoid curve maps the outputs to probabilities between 0 and 1

Logistic regression uses the same linear hypothesis but transforms the output using the sigmoid function to convert the values into probabilities.
![[Pasted image 20260228212401.png]]

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

lr = LogisticRegression(max_iter = 1000)
lr.fit(X_train, y_train)

y_pred = lr.predict(X_test)

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test,y_pred)
sns.heatmap(cm,annot = True,fmt = "d")

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()
```
---
Classifcation metrics
1. Confusion Matrix 
- The confusion matrix is the foundation of most **classification** metrics. 
- It is a 2x2 table (for **binary classification**) that shows the actual vs predicted values in four categories: 
	- True Positives (TP): Correctly predicted positive classes. 
	- True Negatives (TN): Correctly predicted negative classes. 
	- False Positives (FP): Incorrectly predicted positive classes (also called Type I Error). 
	- False Negatives (FN): Incorrectly predicted negative classes (also called Type II Error)

1. Accuracy Accuracy is the most intuitive and simple classification metric. 
	- Accuracy is a good metric when the data is balanced
	- However, for imbalanced datasets, accuracy can be misleading because the model could simply predict the majority class and achieve high accuracy
	- TP + TN / TP + TN + FP + Fn

Precision
It tells us how many of the predicted positives are actually correct
	Key Insight:
	-  Precision is important in situations where false positives are costly, such as in email spam classification (false spam predictions are problematic)

Recall (Sensitivity or True Positive Rate)
Of all the actual positives, how many did we correctly identify?
	Key Insight: 
	- Recall is crucial in situations where false negatives are costly, such as disease detection. Missing a positive case (false negative) is more harmful than incorrectly predicting one

F1 score
- It’s particularly useful when you want to balance both precision and recall
- It’s especially useful in imbalanced datasets where accuracy can be misleading

ROC Curve and AUC (Area Under the Curve)
- The Receiver Operating Characteristic (ROC) curve is a graphical representation that **shows the performance of a binary classifier** as the discrimination threshold is varied.
- The ROC curve plots the TPR against the FPR at different threshold levels. 
- The closer the curve is to the top-left corner, the better the model

AUC (Area Under the Curve) 
The AUC value represents the degree of separability. 
Higher AUC means the model is **better at distinguishing between positive and negative classes.**

AUC ranges from 0 to 1 
- 1 = Perfect classifier 
- 0.5 = Random guess 
- 0 = Completely wrong classification

Key Insight:
	- ROC-AUC is ideal when you care about the ranking of predictions rather than the exact predicted class. 
	- It helps to understand how well the model distinguishes between classes across all thresholds

```python
from sklearn.metrics import classification_report,confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns

y_prob = logistic_reg.predict_proba(X_test)[:,1]
fpr,tpr,_ = roc_curve(y_test,y_prob)

plt.plot(fpr,tpr,marker = ".")
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.show()
```

```python
auc_score = roc_auc_score(y_test, y_prob)
print(f"AUC Score: {auc_score}")
```