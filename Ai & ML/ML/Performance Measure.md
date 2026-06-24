![[Pasted image 20250420212753.png]]

This model is **underfitting**. To see why, first let’s look at the **training error**. As new instances are added to the training set, it becomes impossible for the model to fit the training data perfectly, both because the data is noisy and because it is not linear at all. So the error on the training data goes up until it reaches a plateau, at which point adding new instances to the training set doesn’t make the average error much better or worse.
Now let’s look at the **validation error.** When the model is trained on very few training instances, it is incapable of generalizing properly, which is why the validation error is initially quite large. Then, as the model is shown more training examples, it learns, and thus the validation error slowly goes down.

![[Pasted image 20250420213243.png]]

There are two very important differences:
- The error on the training data is much lower than before. 
- There is a gap between the curves. This means that the model performs significantly better on the training data than on the validation data, 
- Which is the hallmark of an overfitting model. If you used a much larger training set, however, the two curves would continue to get closer.

**Bias** -> Underfiiting
**Variance** -> Overfitting
Increasing a **model’s complexity** -> increase its **variance** and reduce its **bias**.

# Regularized Models

## Overview
- **Purpose**: Reduce **overfitting** by regularizing the model.
- **Mechanism**: Limit the model's degrees of freedom to prevent overfitting.
- **Simplest Approach**: Reduce the number of polynomial degrees in the model.

## Regularization in Linear Models

- **Method**: Constrain the model's weights.
- **Key Techniques**:
    1. **Ridge Regression**:
        - **Goal**: Keep model weights as small as possible.
        - **Implementation**: Add a regularization term to the cost function during training only.
        - **Evaluation**: Use RMSE to assess model performance after training.
    2. **Lasso Regression**:
        - **Goal**: Eliminate weights of least important features (sets them to zero).
        - **Outcome**: Performs feature selection, resulting in a sparse model with few non-zero feature weights.
    3. **Elastic Net**:
        - **Combination**: Includes an ℓ₁ penalty (like Lasso) and an ℓ₂ penalty (like Ridge).
        - **Use Case**: Preferred when features are numerous or strongly correlated.

## Choosing a Regularization Technique

- **Ridge Regression**:
    - **When to Use**: Default choice for regularization when many features are relevant.
- **Lasso Regression**:
    - **When to Use**: Preferred when only a few features are suspected to be useful, as it reduces weights of irrelevant features to zero.
    - **Caution**: May behave erratically with highly correlated features or when features outnumber training instances.
- **Elastic Net**:
    - **When to Use**: Preferred over Lasso when the number of features exceeds training instances or when features are strongly correlated.
    - **Advantage**: Balances Lasso and Ridge properties for more robust performance.

## Q&A

**Validation Error Increasing with Batch Gradient Descent**:
- **What’s Happening**: The model is likely **overfitting** or the learning rate is too high.
**Fix**:

- Reduce the learning rate to ensure stable convergence.
- Use **early stopping** to halt training when validation error stops decreasing.
- Apply **regularization** (e.g., Ridge, Lasso) to reduce overfitting.
- Collect more training data or simplify the model to improve generalization.

**Stopping Mini-batch Gradient Descent on Validation Error Increase**: It is **not a good idea** to stop mini-batch gradient descent immediately when the validation error goes up.

**Polynomial Regression with Large Gap in Learning Curves**:
- **What’s Happening**: A large gap between low training error and high validation error indicates **overfitting** (high variance). The model is too complex, fitting the training data well but failing to generalize.
**Three Solutions**:
- **Reduce Model Complexity**: Use a lower-degree polynomial or fewer features.
- **Apply Regularization**: Use Ridge, Lasso, or Elastic Net to penalize large coefficients and reduce overfitting.
- **Increase Training Data**: More data can help the model generalize better.

