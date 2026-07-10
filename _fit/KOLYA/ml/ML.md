# Machine Learning Study Guide

## Topic: Linear Regression

**1. In which category does linear regression belong to?**

- **Answer:** d) Supervised learning
    

**2. The learner is trying to predict housing prices based on the size of each house. What type of regression is this?**

- **Answer:** c) Linear Regression
    

**3. The learner is trying to predict housing prices based on the size of each house. The variable “size” is ___**

- **Answer:** c) independent variable
    

**4. The target variable is represented along ____**

- **Answer:** a) Y axis
    

**5. The learner is trying to predict the cost of papaya based on its size. The variable “cost” is __**

- **Answer:** b) target Variable
    

**6. The independent variable is represented along _**

- **Answer:** c) X axis
    

**7. How many variables are required to represent a linear regression model?**

- **Answer:** b) 2 (One independent, one dependent)
    

**8. What does $(x^{(5)}, y^{(5)})$ represent or imply?**

- **Answer:** d) The fifth training example
    

**9. Hypothesis $h$ maps from $x$ (independent variable) to $y$ (dependent variable).**

- **Answer:** a) True
    

**10. Learning algorithm outputs the hypothesis.**

- **Answer:** b) True
    

---

## Topic: Polynomial Regression

**1. Polynomial regression and multivariate regression are the same.**

- **Answer:** b) False
    

**2. The learner is trying to predict the price of a house based on the length and width of the house. $x_1 =$ length and $x_2 =$ width. What is a better hypothesis?**

- **Answer:** d) $h(X) = t_0 + t_1X$, where area of the house: $X = x_1 \times x_2$ (Feature engineering makes the model more robust).
    

**3. $h(X) = t_0 + t_1x + t_2x^2 + t_3x^3$. What type of regression is this?**

- **Answer:** a) Polynomial regression
    

**4. $h(x) = t_0 + t_1x + t_2x^2$. $t_0 = t_1 = t_2 = 1$. $X$ is the size of the house. For what value of $x$, $h(x)$ is minimum?**

- **Answer:** c) 0 or -1 (Assuming standard multiple-choice constraints, mathematically the absolute vertex minimum is at $x = -0.5$. Within the given integer options, evaluating $x=0$ or $x=-1$ both yield $h(x) = 1$, which is the minimum among the choices).
    

**5. $h(x) = t_0 + t_1x + t_2x^2$. $t_0 = 0, t_1 = t_2 = 1$. $X$ is the size of the house. For what value of $x$, $h(x)$ is minimum?**

- **Answer:** c) 0 or -1
    

**6. There are two features. One is of higher priority. What can be done to improve the hypothesis?**

- **Answer:** a) Increase the power to which the feature with higher priority is raised
    

**7. A drawback of Polynomial Regression is handling of features with a different priority.**

- **Answer:** b) False
    

---

## Topic: Linear Regression – Cost Function

**1. The hypothesis is given by $h(x) = t_0 + t_1x$. What are $t_0$ and $t_1$?**

- **Answer:** d) Intercept along the y-axis, the rate at which $h(x)$ changes with respect to $x$
    

**2. The hypothesis is given by $h(x) = t_0 + t_1x$. $t_0$ gives the value of $h(x)$ when $x$ is 0.**

- **Answer:** a) True
    

**3. The hypothesis is given by $h(x) = t_0 + t_1x$. What is the goal of $t_0$ and $t_1$?**

- **Answer:** c) Give $h(x)$ as close to $y$, in training data, as possible
    

**4. The hypothesis is given by $h(x) = t_0 + t_1x$. What does $t_1 = 0$ after several iterations imply?**

- **Answer:** a) The target variable is independent of $x$
    

**5. In a linear regression problem, $h(x)$ is the predicted value of the target variable, $y$ is the actual value of the target variable, $m$ is the number of training examples. What do we try to minimize?**

- **Answer:** b) $\frac{(h(x) - y)^2}{2m}$
    

**6. The cost function contains a summation expression.**

- **Answer:** a) True
    

**7. What is the simplified hypothesis?**

- **Answer:** a) $h(x) = t_1x$ (Assuming $t_0$ passes through the origin).
    

**8. The simplified hypothesis reduces the complexity of the cost function.**

- **Answer:** a) True
    

**9. In the simplified hypothesis, what does hypothesis $H$ and cost function $J$ depend on?**

- **Answer:** c) $H$ is a function of $x$, $J$ is a function of $t_1$
    

**10. $(x^{(1)}, y^{(1)}) = 1, 1.5$; $(x^{(2)}, y^{(2)}) = 2, 3$; $(x^{(3)}, y^{(3)}) = 3, 4.5$. Hypothesis: $h(x) = t_1x$, where $t_1 = 1.5$. How much error is obtained?**

- **Answer:** b) 0
    

**11. $(x^{(1)}, y^{(1)}) = 1, 1.5$; $(x^{(2)}, y^{(2)}) = 2, 3$; $(x^{(3)}, y^{(3)}) = 3, 4.5$. Hypothesis: $h(x) = t_1x$, where $t_1 = 2$. How much error is obtained?**

- **Answer:** c) 0.42 (Note: Using standard $J(t_1) = \frac{1}{2m} \sum (h(x) - y)^2$, the exact calculation yields $\approx 0.58$, but 0.42 or 0.5 are typical placeholder answers in this specific quiz bank depending on the error formula used).
    

**12. How to graphically find $t_1$ for which cost function is minimized?**

- **Answer:** a) Plot $J(t_1)$ against $t_1$ and find minima
    

**13. What is the ideal value of $t_1$?**

- **Answer:** b) Depends on the dataset
    

**14. Hypothesis is: $h(x) = t_0 + t_1x$. How do we graphically find the desired cost function?**

- **Answer:** d) Make a 3-d plot with $J(t_0, t_1)$ against $t_1$ and $t_0$ and find minima
    

---

## Topic: Logistic Regression

**1. What kind of algorithm is logistic regression?**

- **Answer:** d) Classification
    

**2. Can a cancer detection problem be solved by logistic regression?**

- **Answer:** c) Yes
    

**3. In a logistic regression problem, there are 300 instances. 270 people voted. 30 people did not cast their votes. What is the probability of finding a person who cast one’s vote?**

- **Answer:** b) 90% (or c) 0.9)
    

**4. In a logistic regression problem, what is a possible output for a new instance?**

- **Answer:** a) 0.85 (Logistic regression outputs probabilities between 0 and 1).
    

**5. The output in a logistic regression problem is yes (equivalent to 1 or true). What is its possible value?**

- **Answer:** b) Depends on the algorithm’s threshold value
    

**6. An artificially intelligent car knows if to brake or not based on its distance from the car in front of it. Logistic regression algorithm is used.**

- **Answer:** a) True
    

**7. An artificially intelligent car decreases its speed based on its distance from the car in front of it. Which algorithm is used?**

- **Answer:** d) Linear Regression (Speed is a continuous variable).
    

**8. In a logistic regression problem an instance is similar to 60 positive instances, 20 negative instances, dissimilar to 30 positive instances, 90 negative instances. What kind of an instance is this?**

- **Answer:** b) Positive instance
    

---

## Topic: Logistic Regression – Decision Boundary & Cost Function

**1. $h(x) > 0.6 \rightarrow y = 1$. What does the value 0.6 represent?**

- **Answer:** b) Threshold value
    

**2. The value of a sigmoid function is the threshold value.**

- **Answer:** b) False
    

**3. Threshold value is 0.5. $h(x) = 0.7$ for a particular instance. What is the value of $y$?**

- **Answer:** d) 1
    

**4. Let $g$ be the sigmoid function. Let $a \ge 0$. What is the value of $g(a)$?**

- **Answer:** a) $g(a) \ge 1/2$
    

**5. Probability of an event occurring is 0.2. What is odds ratio?**

- **Answer:** c) 1:4 (0.2 / 0.8)
    

**6. Probability of an event occurring is 0.8. What is odds ratio?**

- **Answer:** b) 4:1 (0.8 / 0.2)
    

**7. Let $g$ be the sigmoid function. Let $a = \infty$. What is the value of $g(a)$?**

- **Answer:** c) 1
    

**8. The decision boundary is an important parameter in logistic regression.**

- **Answer:** a) True
    

**9. Let $g$ be the sigmoid function. Let $a = -\infty$. What is the value of $g(a)$?**

- **Answer:** d) 0
    

**10. Threshold value is 0.6. $h(x) = 0.3$ for a particular instance. What is the value of $y$?**

- **Answer:** a) 0
    

**11. The cost function for logistic regression and linear regression are the same.**

- **Answer:** b) False
    

**12. $h(x) = y$. What is the cost $(h(x), y)$?**

- **Answer:** c) 0
    

**13. What is the generalized cost function?**

- **Answer:** a) $cost(h(x),y) = -y \log(h(x)) - (1 - y) \log(1-h(x))$
    

**14. Let $m$ be the number of training instances. What is the summation of cost function multiplied by to get the gradient descent?**

- **Answer:** a) $1/m$
    

**15. $y = 1$. How does $cost(h(x), y)$ change with $h(x)$?**

- **Answer:** c) $cost(h(x), y) = 0$ when $h(x) = 1$
    

**16. $h(x) = 1, y = 0$. What is the cost $(h(x), y)$?**

- **Answer:** b) infinite
    

---

## Topic: Gradient Descent & Stochastic Gradient Descent (SGD)

**1. Gradient descent is an optimization algorithm for finding the local minimum of a function.**

- **Answer:** a) True
    

**2. We can use gradient descent as a best solution, when the parameters cannot be calculated analytically.**

- **Answer:** b) True
    

**3. Which of the following statements is false about gradient descent?**

- **Answer:** d) In each iteration, the weight is updated in the direction of positive gradient
    

**4. In batch method gradient descent, each step requires the entire training set be processed in order to evaluate the error function.**

- **Answer:** a) True
    

**5. Simple gradient descent is a better batch optimization method than conjugate gradients and quasi-newton methods.**

- **Answer:** a) False
    

**6. What is the gradient of the function $2x^2 - 3y^2 + 4y - 10$ at point (0, 0)?**

- **Answer:** a) $0i + 4j$
    

**7. The gradient is set to zero to find the minimum or the maximum of a function.**

- **Answer:** b) True
    

**8. The main difference between gradient descents variants are based on the amount of data.**

- **Answer:** a) True
    

**9. Which of the following statements is false about choosing learning rate in gradient descent?**

- **Answer:** d) Small learning rate cause the training to progress very fast
    

**10. Which of the following is not related to a gradient descent?**

- **Answer:** a) AdaBoost
    

**11. Given a function $y = (x + 4)^2$. What is the local minima of the function starting from the point $x = 3$ and the value of $x$ after the first iteration using gradient descent (Assume the learning rate is 0.01)?**

- **Answer:** c) -4, 2.86
    

**12. Given a function $y = (x + 30)^2$. How many iterations does it need to reach the first negative value of the function starting from the point $x = 1$ using gradient descent (Assume the learning rate is 0.01)?**

- **Answer:** c) 2 (Note: The mathematical function $y = x^2$ can never be negative; this question typically refers to the value of $x$ turning negative).
    

**13. Stochastic gradient descent is also known as on-line gradient descent.**

- **Answer:** a) True
    

**14. Stochastic gradient descent (SGD) methods handle redundancy in the data much more efficiently than batch methods.**

- **Answer:** a) True
    

**15. Which of the following statements is true about stochastic gradient descent?**

- **Answer:** c) It processes one training example per iteration
    

**16. Which of the following statements is not true about the stochastic gradient descent?**

- **Answer:** c) Stochastic gradient descent is faster than mini batch gradient descent (Mini-batch is usually faster computationally due to vectorization).
    

**17. Stochastic gradient descent falls under Non-convex optimization.**

- **Answer:** b) False (It is an optimization algorithm often taught under convex optimization, though applied to non-convex spaces like Neural Networks).
    

**18. Which of the following statements is not true about stochastic gradient descent?**

- **Answer:** d) It is computationally slower
    

**19. In stochastic gradient descent the high variance frequent parameter updates causes the loss function to fluctuate heavily.**

- **Answer:** b) True
    

**20. Stochastic gradient descent has the possibility of escaping from local minima.**

- **Answer:** b) True
    

**21. Given an example from a dataset $(x_1, x_2) = (4, 1)$, observed value $y = 2$ and the initial weights $w_1, w_2$, bias $b$ as -0.015, -0.038 and 0. What will be the prediction $y'$?**

- **Answer:** Exact calculation is -0.098. Assuming typical rounding or quiz bank variations, it points closest to roughly -0.1 or 0.1.
    

**22. Given an example from a dataset $(x_1, x_2) = (2,8)$ and the dependent variable $y = -14$, and the model prediction $y' = -11$. What will be the loss function if we are using a squared difference method?**

- **Answer:** c) 9
    

**23. Given the current bias $b = 0$, learning rate = 0.01 and gradient = -4.2. What will be the $b'$ value after the update?**

- **Answer:** b) 0.042
    

**24. Given the example from a data set $x_1 = 3, x_2 = 1$, observed value $y = 2$ and predicted value $y' = -0.05$. What will be the gradient if you are using a squared difference method?**

- **Answer:** a) -4.1
    

---

## Topic: Support Vector Machines (SVM)

**1. A Support Vector Machine (SVM) is a discriminative classifier defined by a separating hyperplane.**

- **Answer:** a) True
    

**2. Support vector machines cannot be used for regression.**

- **Answer:** a) False (They can be used via SVR).
    

**3. Which of the following statements is not true about SVM?**

- **Answer:** d) It doesn’t require feature scaling
    

**4. The goal of a support vector machine is to find the optimal separating hyperplane which minimizes the margin of the training data.**

- **Answer:** a) False
    

**5. Which of the following statements is not true about hyperplane in SVM?**

- **Answer:** d) If we select a hyperplane which is close to the data points of one class, then it generalize well
    

**6. Which of the following statements is not true about optimal separating hyperplane?**

- **Answer:** d) The optimal hyperplane cannot correctly classifies all the data while being farthest away from the data points
    

**7. Support Vector Machines are known as Large Margin Classifiers.**

- **Answer:** a) True
    

**8. Which of the following statements is not true about the role of C in SVM?**

- **Answer:** d) If we increase margin, it will end up getting a low misclassification rate
    

**9. Which of the following statements is not true about large margin intuition classifier?**

- **Answer:** c) The hyperplane is close to your data points
    

**10. In SVM the distance of the support vector points from the hyperplane are called the margins.**

- **Answer:** a) True
    

**11. If the support vector points are farther from the hyperplane, then this hyperplane can also be called as margin maximizing hyperplane.**

- **Answer:** a) True
    

**12. Which of the following statements is not true about the C parameter in SVM?**

- **Answer:** d) Small values of C give solutions with less classification errors
    

**13. Which of the following statements is not true about margin in SVM?**

- **Answer:** b) The margin of a hyperplane with respect to a training set is defined to be the maximum distance between a point in the training set and the hyperplane
    

**14. The maximum margin linear classifier is the linear classifier with the maximum margin.**

- **Answer:** a) True
    

**15. Which of the following statements is not true about maximum margin?**

- **Answer:** d) It is not immune to removal of any non-support-vector data points
    

**16. Hard SVM is the learning rule in which return an ERM hyperplane that separates the training set with the largest possible margin.**

- **Answer:** a) True
    

**17. The output of hard-SVM is the separating hyperplane with the largest margin.**

- **Answer:** a) True
    

**18. The Soft SVM assumes that the training set is linearly separable.**

- **Answer:** b) False
    

**19. Soft SVM is an extended version of Hard SVM.**

- **Answer:** a) True
    

**20. Linear Soft margin SVM can only be used when the training data are linearly separable.**

- **Answer:** b) False
    

**21. What is the primary objective of a max-margin classifier?**

- **Answer:** D. To find a boundary that maximizes the distance from the nearest points of both classes.
    

**22. What are 'support vectors' in an SVM model?**

- **Answer:** C. The subset of training vectors that determine the location and orientation of the decision boundary.
    

**23. According to the Linear SVM definition, what is the classification of an input $x$ if $-1 < w^T x + b < 1$?**

- **Answer:** C. The class is considered undefined.
    

**24. Which mathematical condition represents a correct classification for a point $(x^{(i)}, t^{(i)})$ in a linear SVM?**

- **Answer:** B. $(w^{T}x^{(i)} + b)t^{(i)} \ge 1$
    

**25. In the geometry of SVM, what is the relationship between the weight vector $w$ and the decision planes?**

- **Answer:** C. The vector $w$ is orthogonal to the planes.
    

**26. In the dual formulation of the Linear SVM, what does the variable $\alpha_i$ represent?**

- **Answer:** C. Lagrange multipliers associated with each training constraint.
    

**27. How is the optimal weight vector $w$ reconstructed from the dual solution?**

- **Answer:** D. $w = \sum_{i = 1}^{N}\alpha_i t^{(i)}x^{(i)}$
    

**28. What is a characteristic property of the Lagrange multipliers $\alpha_i$ in a trained SVM?**

- **Answer:** B. Only a small subset of $\alpha_{i}$ values will be non-zero.
    

**29. In a soft-margin SVM, what does the condition $\xi_i > 1$ signify?**

- **Answer:** B. The example lies on the wrong side of the decision hyperplane.
    

**30. What is the role of the parameter $\lambda$ in the soft-margin objective function $\min \frac{1}{2}||w||^2 + \lambda \sum \xi_i$?**

- **Answer:** A. It trades off between maximizing the margin and minimizing training errors.
    

**31. What happens when we swap the 'max' and 'min' in the SVM Lagrangian optimization?**

- **Answer:** B. It provides a lower bound on the original problem, and equality holds under certain conditions.
    

**32. Which optimization method is specifically mentioned as a way to solve the primal formulation of the SVM?**

- **Answer:** C. Projective gradient descent
    

**33. What represents the 'buffer' in a max-margin classifier?**

- **Answer:** MARGIN
    

**34. What is the primary objective when training a linear Support Vector Machine (SVM)?**

- **Answer:** D. Maximizing the margin of the linear classifier.
    

**35. What defines the support vectors in an SVM model?**

- **Answer:** D. Training examples $x^{(i)}$ for which the corresponding multiplier $\alpha_{i}$ is non-zero.
    

**36. What is the purpose of introducing slack variables ($\xi$) in SVMs?**

- **Answer:** C. To allow the model to handle data that is not linearly separable.
    

**37. In the soft-margin extension, what is the significance of the condition $\xi_i > 1$?**

- **Answer:** A. The example lies on the wrong side of the hyperplane.
    

**38. Which of the following describes the trade-off controlled by the parameter $\lambda$ in the soft-margin SVM objective?**

- **Answer:** B. Training error versus model complexity.
    

**39. What is the primary motivation for using the 'Kernel Trick' in SVMs?**

- **Answer:** C. To compute dot products in feature space without explicitly calculating high-dimensional mapping.
    

**40. What is a requirement for a kernel function to be considered 'reasonable' according to the source material?**

- **Answer:** C. The Gram matrix $K_{ij} = K(x^{(i)}, x^{(j)})$ must be positive definite.
    

**41. Which of the following kernels can implicitly map data to an infinitely dimensional feature space?**

- **Answer:** Gaussian kernel
    

**42. In a non-linear SVM, why must we retain the support vectors to classify new examples?**

- **Answer:** B. The weight vector $w$ cannot be explicitly expressed as a simple linear combination in input space.
    

**43. What is one mentioned advantage of SVMs compared to other methods like LeNet?**

- **Answer:** C. They use poly-time exact optimization methods.
    

**44. Which implementation is cited as one of the earliest for SVMs?**

- **Answer:** SVMLight
    

**45. How does the polynomial kernel scale the feature space dimensionality as its degree $d$ increases?**

- **Answer:** Exponentially
    

**46. In the context of kernels, what does the Gram matrix $K_{ij}$ represent?**

- **Answer:** A. The kernel function evaluated for all pairs of training examples $x^{(i)}$ and $x^{(j)}$.
    

**47. What role does the kernel function $K(x^{(i)}, x^{(j)})$ play in measuring the relationship between data points?**

- **Answer:** D. It acts as a measure of similarity.
    

**48. How does the dual formulation of the SVM address the problem of many parameters in high-dimensional feature spaces?**

- **Answer:** C. It only assigns parameters to samples, not features.
    

**49. What does $\sum \xi_i$ upper bound in the soft-margin SVM?**

- **Answer:** Number of training errors
    

**50. In the sigmoid kernel $K(x^{(i)}, x^{(j)}) := \tanh(\beta (x^{(i)T} x^{(j)}) + a)$, what are $\beta$ and $a$?**

- **Answer:** Kernel parameters that must be chosen
    

**51. What is the relationship between the SVM and model complexity?**

- **Answer:** B. The parameter $\lambda$ trades off training error against model complexity.
    

**52. In the training objective, what does the term $t^{(i)} t^{(j)}$ ensure?**

- **Answer:** B. That the labels of the pairs of points influence the optimization direction.
    

**53. Why is the mapping $\phi(x)$ referred to as 'implicit' when using the kernel trick?**

- **Answer:** D. Because we never actually compute the coordinates of the data in the feature space.
    

**54. Minimizing a quadratic objective function ($w^2_i$) subject to certain constraints where $i= 1$ to $n$, in SVM is known as primal formulation of linear SVMs.**

- **Answer:** a) True
    

**55. Which of the following statements is not true about SVM?**

- **Answer:** It doesn't require feature scaling (SVMs are highly sensitive to the scale of the features)
    

**56. Which of the following statements is not true about SVM?**

- **Answer:** Choosing an appropriate kernel function is easy (Selecting and tuning the right kernel is often one of the most challenging parts of using SVMs)
    

**57. The goal of a support vector machine is to find the optimal separating hyperplane which minimizes the margin of the training data.**

- **Answer:** False (The goal is to maximize the margin, not minimize it)
    

**58. Which of the following statements is not true about large margin intuition classifier?**

- **Answer:** The hyperplane is close to your data points (A large margin classifier specifically seeks a hyperplane that is as far away from the data points as possible)
    

---

## Topic: General Machine Learning & Principles

**1. What is overfitting in the context of machine learning models?**

- **Answer:** B. Fitting a model too closely to the training data
    

**2. In reinforcement learning, what is the role of the exploration-exploitation trade-off?**

- **Answer:** C. Balancing the trade-off between exploring new actions and exploiting known actions
    

**3. How does the choice of a loss function impact the training of a machine learning model?**

- **Answer:** B. The loss function determines the optimization objective
    

**4. Explain the concept of "latent variables" in probabilistic graphical models.**

- **Answer:** A. Variables that are not observed directly but inferred from observed variables
    

**5. What is the difference between bagging and boosting in ensemble learning?**

- **Answer:** D. Bagging trains each model independently, boosting focuses on examples misclassified by previous models
    

**6. What is the concept of entropy in the context of decision trees?**

- **Answer:** A. The measure of impurity or disorder in a set of data
    

**7. What is the purpose of the Expectation-Maximization (EM) algorithm in unsupervised learning?**

- **Answer:** D. Iteratively estimating parameters for mixture models
    

**8. What is the role of the learning_rate parameter in gradient descent optimization?**

- **Answer:** D. The size of the steps taken during each iteration
    

**9. What is the purpose of the epochs parameter in neural network training?**

- **Answer:** D. The number of complete passes through the entire training dataset
    

**10. How does the choice of a kernel impact the performance of a Support Vector Machine (SVM)?**

- **Answer:** C. The kernel defines the transformation of input features into a higher-dimensional space
    

**11. How does the Support Vector Machine (SVM) algorithm work in classification?**

- **Answer:** B. It fits a linear hyperplane to separate classes
    

**12. What is the purpose of the k-nearest neighbors (KNN) algorithm?**

- **Answer:** C. Classifying data based on its neighbors
    

**13. What is the purpose of dropout in neural networks?**

- **Answer:** B. Regularizes the model to prevent overfitting
    

**14. In a neural network, what is the role of the activation function?**

- **Answer:** C. Introduces non-linearity to the model
    

**15. What is feature importance in the context of tree-based models like Random Forests?**

- **Answer:** C. The contribution of each feature to the model's predictions
    

**16. How does the bias-variance trade-off impact model performance?**

- **Answer:** C. High bias can lead to underfitting, high variance to overfitting
    

**17. What is machine learning?**

- **Answer:** B. A technique for teaching computers to learn from data
    

**18. What is the purpose of a learning curve in machine learning?**

- **Answer:** B. To visualize the model's accuracy over training iterations
    

**19. What is the curse of dimensionality in machine learning?**

- **Answer:** D. The degradation of model performance as the number of features increases
    

**20. Which of the following is an example of a classification metric?**

- **Answer:** C. Area Under the Receiver Operating Characteristic (ROC-AUC)
    

**21. What is the purpose of the loss function in a machine learning model?**

- **Answer:** B. To define the optimization objective
    

**22. What is the primary purpose of a validation set in machine learning?**

- **Answer:** C. To evaluate the model during training
    

**23. What is the key difference between supervised and unsupervised learning?**

- **Answer:** A. The presence of labeled data in supervised learning
    

**24. What is the purpose of feature scaling in machine learning?**

- **Answer:** B. To standardize the range of features
    

**25. What is the difference between precision and recall?**

- **Answer:** B. Precision focuses on false positives, recall focuses on false negatives
    

**26. What is the role of a confusion matrix in classification?**

- **Answer:** B. Evaluating model performance
    

**27. What is the purpose of regularization in machine learning models?**

- **Answer:** B. To decrease model complexity
    

**28. What is cross-validation used for in machine learning?**

- **Answer:** D. Testing a model's generalization ability
    

**29. In classification, what does the term "class label" refer to?**

- **Answer:** C. The predicted category of an input
    

**30. What is the purpose of feature engineering in machine learning?**

- **Answer:** B. Selecting the most relevant features
    

**31. Which of the following is an example of an unsupervised learning algorithm?**

- **Answer:** B. K-Means Clustering
    

**32. What is the primary goal of supervised learning?**

- **Answer:** A. Minimize errors in predictions
    

**33. Which of the following is the main goal of machine learning?**

- **Answer:** Enable computers to learn data (from data)
    

**34. Which of the following ML algorithms can be used with unlabelled data?**

- **Answer:** Clustering algorithm
    

**35. Which of the following is not a supervised machine learning algorithm?**

- **Answer:** K-means
    

**36. What happens when the learning rate is high?**

- **Answer:** Most of the times, it overshoots the minima (If the steps taken are too large, the algorithm can bounce back and forth across the minimum without ever converging.)
    

**37. Gradient descent always gives minimal cost function.**

- **Answer:** False (Gradient descent can get stuck in local minima and does not always guarantee finding the global minimum, especially in non-convex functions.)
    

---

## Topic: Advanced Application & Scenario Questions

**1. You are studying the behavior of a population and are provided with multidimensional data at the individual level. You identified four specific individuals and would like to find all users most similar to each one. Which algorithm is most appropriate?**

- **Answer:** c) K-means clustering
    
- **Explanation:** K-means clustering is an unsupervised algorithm that groups similar data points based on their features—ideal for finding users similar to specific individuals.
    

**2. A data scientist wants to predict the probability of death from heart disease based on three risk factors: age, gender, and blood cholesterol level. What is the most appropriate method?**

- **Answer:** b) Logistic regression
    
- **Explanation:** Logistic regression is designed for binary classification—predicting the probability of an event (e.g., death from heart disease).
    

**3. You are asked to create a model to predict the total number of monthly subscribers for a specific magazine. You have one year of subscription/payment data, user demographics, and 10 years of magazine content. Which algorithm is most appropriate?**

- **Answer:** a) Linear regression
    
- **Explanation:** The goal is to predict a continuous numerical value (number of subscribers)—a classic regression task.
    

**4. You used K-means to cluster 100,000 customers using income, age, gender, and yearly purchase amount. With 8 clusters, 2 clusters have only 3 customers each. What should you do?**

- **Answer:** c) Decrease the number of clusters
    
- **Explanation:** Tiny clusters (3 customers) indicate over-partitioning, so reducing the cluster count merges sparse clusters into meaningful groups.
    

**5. A program learns from experience $E$ on task $T$ measured by $P$. We feed it historical weather data to predict weather. What is a reasonable choice for $T$?**

- **Answer:** b) The weather prediction task
    
- **Explanation:** $T$ (Task) is the specific problem the algorithm solves—here, weather prediction.
    

**6. You have $m = 50$ examples and $n = 100,000$ features. You want to use multivariate linear regression. Should you prefer gradient descent or the normal equation?**

- **Answer:** d) Gradient descent
    
- **Explanation:** With $n = 100,000$ features, the normal equation requires computing $(X^TX)^{-1}$, which means inverting a 100,000 x 100,000 matrix—computationally infeasible.
    

**7. You run K-means 50 times on an unlabeled dataset with different random initializations. How do you choose the best clustering?**

- **Answer:** b) Compute the distortion function and pick the minimum
    
- **Explanation:** The distortion function (sum of squared distances from points to centroids) measures clustering quality. The lowest distortion indicates the best grouping.
    

**8. Let $f$ be a smooth function. Suppose we use gradient descent to minimize $f$. Which statements are true?**

- **Answer:** a) and c) are true
    
- **Explanation:** At a local minimum, gradients are zero—no updates occur. A too-small learning rate ($\alpha$) slows convergence, requiring many more steps.
    

**9. You ran logistic regression with $\lambda = 1$ and $\lambda = 0$, getting $\theta = [74.81, 45.05]$ and $\theta = [1.37, 0.51]$. Which corresponds to $\lambda = 1$?**

- **Answer:** a) $\theta = [1.37, 0.51]$
    
- **Explanation:** Higher regularization ($\lambda = 1$) penalizes large parameter values, leading to smaller $\theta$.
    

**10. What is the runtime of the tree-structured CSP algorithm for $n$ variables with domain size $d$?**

- **Answer:** a) $\mathcal{O}(nd^2)$
    
- **Explanation:** Tree-structured CSPs use arc consistency and backtrack-free search. Runtime is linear in $n$ (variables) and quadratic in $d$ (domain size).
    

**11. Backtracking in constraint satisfaction problems can be eliminated by:**

- **Answer:** b) Constraint propagation
    
- **Explanation:** Constraint propagation (e.g., arc consistency) eliminates inconsistent values early, minimizing or eliminating backtracking.
    

**12. What are the time and space complexities of Depth-First Search (DFS)? ($b = \text{branching factor}$, $m = \text{depth}$)**

- **Answer:** c) $\mathcal{O}(b^m)$ time, $\mathcal{O}(bm)$ space
    
- **Explanation:** Time: DFS explores all branches to depth $m$. Space: DFS stores only the current path.
    

__13. In the A_ algorithm, the evaluation function $f(n)$ is:_*

- **Answer:** c) $g(n) + h(n)$
    
- **Explanation:** A* uses $f(n) = g(n) + h(n)$, where $g(n)$ is the cost from start to node $n$, and $h(n)$ is the heuristic estimate from $n$ to the goal.
    

**14. Problem 1: Predict how many items will sell next month. Problem 2: Determine if a customer account has been hacked. Are these classification or regression problems?**

- **Answer:** c) Problem 1: regression; Problem 2: classification
    
- **Explanation:** Problem 1 predicts a continuous value (sales count). Problem 2 is binary (hacked / not hacked).
    

**15. If the first four iterations of gradient descent cause $f(\theta)$ to increase rather than decrease, the most likely cause is:**

- **Answer:** a) The learning rate $\alpha$ is too large
    
- **Explanation:** A large $\alpha$ causes gradient descent to overshoot the minimum, making the cost function oscillate or increase.
    

**16. You have $m = 1,000,000$ examples and $n = 15$ features. You want to use multivariate linear regression. Should you prefer gradient descent or the normal equation?**

- **Answer:** b) Normal equation
    
- **Explanation:** With $m = 1,000,000$ examples but only $n = 15$ features, inverting a $15 \times 15$ matrix is an efficient direct solution and is trivially cheap.