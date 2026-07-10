**1. In which category does linear regression belong to?**
**Answer:** d) Supervised learning

**2. The learner is trying to predict housing prices based on the size of each house. What type of regression is this?**
**Answer:** c) Linear Regression

**3. The learner is trying to predict housing prices based on the size of each house. The variable “size” is ___________**
**Answer:** c) independent variable

**4. The target variable is represented along ____________**
**Answer:** a) Y axis

**5. The learner is trying to predict the cost of papaya based on its size. The variable “cost” is __________**
**Answer:** b) target Variable

**6. The independent variable is represented along _________**
**Answer:** c) X axis

**7. How many variables are required to represent a linear regression model?**
**Answer:** b) 2 

**8. What does (x(5), y(5)) represent or imply?**
**Answer:** d) The fifth training example

**9. Hypothesis h maps from x (independent variable) to y (dependent variable).**
**Answer:** a) True

**10. Learning algorithm outputs the hypothesis.**
**Answer:** b) True

---
**1. The hypothesis is given by h(x) = t0 + t1x. What are t0 and t1?**
**Answer:** d) Intercept along the y-axis, the rate at which h(x) changes with respect to x

**2. The hypothesis is given by h(x) = t0 + t1x. t0 gives the value of h(x) when x is 0.**
**Answer:** a) True

**3. The hypothesis is given by h(x) = t0 + t1x. What is the goal of t0 and t1?**
**Answer:** c) Give h(x) as close to y, in training data, as possible

**4. The hypothesis is given by h(x) = t0 + t1x. What does t1 = 0 after several iterations imply?**
**Answer:** a) The target variable is independent of x

**5. In a linear regression problem, h(x) is the predicted value of the target variable, y is the actual value of the target variable, m is the number of training examples. What do we try to minimize?**
**Answer:** b) (h(x) – y)² / 2*m

**6. The cost function contains a summation expression.**
**Answer:** a) True

**7. What is the simplified hypothesis?**
**Answer:** a) h(x) = t1x

**8. The simplified hypothesis reduces the complexity of the cost function.**
**Answer:** a) True

**9. In the simplified hypothesis, what does hypothesis H and cost function J depend on?**
**Answer:** c) H is a function of x, J is a function of t1

**10. (x(1), y(1)) = 1, 1.5, (x(2), y(2)) = 2, 3, (x(3), y(3)) = 3, 4.5. Hypothesis: h(x) = t1x, where t1 = 1.5. How much error is obtained?**
**Answer:** b) 0

**12. How to graphically find t1 for which cost function is minimized?**
**Answer:** a) Plot J(t1) against t1 and find minima

**13. What is the ideal value of t1?**
**Answer:** b) Depends on the dataset

**14. Hypothesis is: h(x) = t0 + t1x. How do we graphically find the desired cost function?**
**Answer:** d) Make a 3-d plot with J(t0, t1) against t1 and t0 and find minima

---

**1. What is the goal of gradient descent?**
**Answer:** d) Minimize cost function

**2. Gradient descent always gives minimal cost function.**
**Answer:** b) False *(Note: It can get stuck in a local minimum or diverge if the learning rate is not set correctly).*

**3. What happens when the learning rate is high?**
**Answer:** c) Most of the times, it overshoots the minima

**4. What is the correct way to update t0 and t1?**
**Answer:** a) Calculate t0 and t1 and then update t0 and t1 *(Note: This refers to simultaneous updates, which is required for gradient descent).*

**5. The cost function contains a squared term and is divided by 2*m where m is the number of training examples. What is in the denominator of gradient descent function?**
**Answer:** b) m

**6. Cost function has a squared term, but gradient descent does not. Why?**
**Answer:** c) Differentiation of cost function

**7. What is the output of gradient descent after each iteration?**
**Answer:** a) Updated t0, t1

**8. Who invented gradient descent?**
**Answer:** d) Augustin-Louis Cauchy

**9. h(x) = t0 + t1x. Alpha value (learning rate) is 0.1. Initial theta values are 0, 0. X = [1, 2, 3] and Y = [1, 3, 5]. What is the value of cost function after 1st iteration?**
**Answer:** c) 1.2953

**10. h(x) = t0 + t1x. Alpha value (learning rate) is 0.1. Initial theta values are 0.3, 0.73. X = [1, 2, 3] and Y = [1, 3, 5]. What is the value of t0 after 1st iteration?**
**Answer:** b) 0.425

**11. What is the generalized goal of gradient descent?**
**Answer:** b) Minimize J(t0, t1, t1, …, tn) *(Note: There is a slight typo in the original option text repeating t1, but it correctly represents minimizing the multivariate cost function).*

---
**1. Multivariate linear regression belongs to which category?** **Answer:** c) Supervised learning

**2. The learner is trying to predict housing prices based on the size of each house and number of bedrooms. What type of regression is this?** **Answer:** d) Multivariate Linear Regression

**3. What does xn(i) represent?** **Answer:** c) Value of nth variable in the ith training example

**4. How is the hypothesis represented in multivariate regression? Transpose of matrix a is represented as aT.** **Answer:** a) h(X) = tTX

**5. Let there be n features. What is the dimension of the X vector in hypothesis h(X) = tTX?** **Answer:** b) (n + 1) x 1 _(Note: This accounts for the n features plus the x0 intercept term which is set to 1)._

**6. What does X(I) represent?** **Answer:** c) A feature vector denoting the independent variables in the ith example

**7. What is the minimum number of variables required to represent a linear regression model?** **Answer:** b) 2 _(Note: One independent variable and one dependent variable)._

**8. What does (x1(4), x2(4), y(4)) represent or imply?** **Answer:** c) The fourth training example and there are two independent variables

**9. There is no upper bound on the number of the independent variable(s).** **Answer:** a) True

**10. There is no upper bound on the number of the target variable(s).** **Answer:** b) False _(Note: Standard multivariate linear regression, as taught in introductory ML courses, predicts a single target variable y)._

---
### **Polynomial and Multivariate Regression**

**1. Polynomial regression and multivariate regression are the same.**
**Answer:** b) False

**2. The learner is trying to predict the price of a house based on the length and width of the house. x1 = length and x2 = width. What is a better hypothesis?**
**Answer:** d) h(X) = t0 + t1X, where area of the house: X = x1 * x2

**3. h(X) = t0 + t1x + t2x2 + t3x3. What type of regression is this?**
*(Note: Question numbers in your prompt skipped to 4)*
**Answer:** a) Polynomial regression

**4. h(x) = t0 + t1x + t2x2. t0 = t1 = t2 = 1. X is the size of the house. For what value of x, h(x) is minimum?**
**Answer:** c) 0 or -1

**5. h(x) = t0 + t1x + t2x2. t0 = 0, t1 = t2 = 1. X is the size of the house. For what value of x, h(x) is minimum?**
**Answer:** c) 0 or -1

**6. There are two features. One is of higher priority. What can be done to improve the hypothesis?**
**Answer:** a) Increase the power to which the feature with higher priority is raised

**7. A drawback of Polynomial Regression is handling of features with a different priority.**
**Answer:** b) False

---
### **Gradient Descent**

**1. The cost function is minimized by __________**
**Answer:** d) Gradient descent

**2. What is the minimum number of parameters of the gradient descent algorithm?**
**Answer:** b) 2

**3. What happens when the learning rate is low?**
**Answer:** b) It reaches the minima very slowly

**5. Gradient descent tries to _____________**
**Answer:** b) minimize the cost function

**6. Feature scaling can be used to simplify gradient descent for multivariate linear regression.**
**Answer:** a) True

**7. x1’s range is 0 to 300. x2’s range is 0 to 1000. What are the suitable ranges of x1 and x2 after mean normalization?**
**Answer:** a) x1 = (x1 – 150)/300, x2 = (x2-500)/1000

**8. x1’s range is 0 to 300. x2’s range is 0 to 1000. What are the suitable ranges of x1 and x2 after feature scaling?**
**Answer:** d) x1 = x1/300, x2 = x2/1000

**9. On which factor is the updating of each parameter dependent on?**
**Answer:** c) The learning rate and the target variable

**10. What is updated by gradient descent after each iteration?**
**Answer:** b) Independent variables *(Note: in this context, it refers to the parameters/weights)*

**12. Mean normalization can be used to simplify gradient descent for multivariate linear regression.**
**Answer:** a) True

---
### **Logistic Regression (Part 1)**

**1. What kind of algorithm is logistic regression?**
**Answer:** d) Classification

**2. Can a cancer detection problem be solved by logistic regression?**
**Answer:** c) Yes

**3. In a logistic regression problem, there are 300 instances. 270 people voted. 30 people did not cast their votes. What is the probability of finding a person who cast one’s vote?**
**Answer:** c) 0.9 *(or 90%)*

**4. In a logistic regression problem, what is a possible output for a new instance?**
**Answer:** a) 0.85

**5. The output in a logistic regression problem is yes (equivalent to 1 or true). What is its possible value?**
**Answer:** b) Depends on the algorithm’s threshold value

**7. An artificially intelligent car knows if to brake or not based on its distance from the car in front of it. Logistic regression algorithm is used.**
**Answer:** a) True

**8. An artificially intelligent car decreases its speed based on its distance from the car in front of it. Which algorithm is used?**
**Answer:** d) Linear Regression

**9. In a logistic regression problem an instance is similar to 60 positive instances, 20 negative instances, dissimilar to 30 positive instances, 90 negative instances. What kind of an instance is this?**
**Answer:** b) Positive instance

**10. When was logistic regression invented?**
**Answer:** b) 1958

---
### **Logistic Regression (Part 2)**

**1. What function is used for hypothesis representation in logistic regression?**
**Answer:** d) Sigmoid function

**2. The value of a sigmoid function is 1.5.**
**Answer:** b) False

**3. How is the hypothesis represented? Transpose of t is tT.**
**Answer:** d) h(X) = 1/(1 + e(-tTx))

**4. Let g be the sigmoid function. Let a = 0. What is the value of g(a)?**
**Answer:** a) 1/2

**5. Probability of an event occurring is 1.2. What is odds ratio?**
**Answer:** c) Undefined

**7. What is the odds ratio?**
**Answer:** a) p/(1-p)

**8. The output of logistic regression is always 0 or 1.**
**Answer:** b) False *(It outputs a probability; the final classification applies a threshold to get 0 or 1)*

---

### **Logistic Regression (Part 3)**

**1. h(x) > 0.6 -> y = 1. What does the value 0.6 represent?**
**Answer:** b) Threshold value

**2. The value of a sigmoid function is the threshold value.**
**Answer:** b) False

**3. Threshold value is 0.5. h(x) = 0.7 for a particular instance. What is the value of y?**
**Answer:** d) 1

**4. Let g be the sigmoid function. Let a >= 0. What is the value of g(a)?**
**Answer:** a) g(a) >= 1/2

**5. Probability of an event occurring is 0.2. What is odds ratio?**
**Answer:** c) 1:4

**6. Probability of an event occurring is 0.8. What is odds ratio?**
**Answer:** b) 4:1

**7. Let g be the sigmoid function. Let a = infinite. What is the value of g(a)?**
**Answer:** c) 1

**8. The decision boundary is an important parameter in logistic regression.**
**Answer:** a) True

**9. Let g be the sigmoid function. Let a = -(infinite). What is the value of g(a)?**
**Answer:** d) 0

**10. Threshold value is 0.6. h(x) = 0.3 for a particular instance. What is the value of y?**
**Answer:** a) 0

---

### **Cost Function & Multiclass Classification**

**1. The cost function for logistic regression and linear regression are the same.**
**Answer:** b) False

**2. h(x) = y. What is the cost (h(x), y)?**
**Answer:** c) 0

**3. What is the generalized cost function?**
**Answer:** a) cost(h(x),y) = -y*log(h(x)) – (1 – y)*log(1-h(x))

**4. Let m be the number of training instances. What is the summation of cost function multiplied by to get the gradient descent?**
**Answer:** a) 1/m

**5. y = 1. How does cost(h(x), y) change with h(x)?**
**Answer:** c) cost(h(x), y) = 0 when h(x) = 1

**8. h(x) = 1, y = 0. What is the cost (h(x), y)?**
**Answer:** b) infinite

**9. The output is whether a person will vote or not, based on several features. It is an example of multiclass classification.**
**Answer:** b) False

**10. The output is whether a person will surely vote or surely not vote or may cast a vote, based on one feature. It is an example of multiclass classification.**
**Answer:** a) True

**11. y = {0, 1, …, n}. This problem is divided into ______ binary classification problems.**
**Answer:** c) n + 1

**12. y = {0, 1, …, 8}. This problem is divided into ______ binary classification problems.**
**Answer:** b) 9

**13. y = {0, 1, 2, 3, 4, 5, 6, 8}. This problem is divided into ______ binary classification problems.**
**Answer:** c) 8

**14. The outputs of an image recognition system is {0, 0, 1, 0}. The classes are dog, cat, elephant, and lion. What is the image of, according to our algorithm?**
**Answer:** c) Elephant

---

### **Gradient Descent & Stochastic Gradient Descent (SGD)**

**1. Gradient descent is an optimization algorithm for finding the local minimum of a function.**
**Answer:** a) True

**2. We can use gradient descent as a best solution, when the parameters cannot be calculated analytically.**
**Answer:** b) True

**3. Which of the following statements is false about gradient descent?**
**Answer:** d) In each iteration, the weight is updated in the direction of positive gradient

**4. In batch method gradient descent, each step requires the entire training set be processed in order to evaluate the error function.**
**Answer:** a) True

**6. What is the gradient of the function 2x² – 3y² + 4y – 10 at point (0, 0)?**
**Answer:** a) 0i + 4j

**7. The gradient is set to zero to find the minimum or the maximum of a function.**
**Answer:** b) True

**8. The main difference between gradient descents variants are based on the amount of data.**
**Answer:** a) True

**9. Which of the following statements is false about choosing learning rate in gradient descent?**
**Answer:** d) Small learning rate cause the training to progress very fast


**11. Given a function y = (x + 4)². What is the local minima of the function starting from the point x = 3 and the value of x after the first iteration using gradient descent (Assume the learning rate is 0.01)?**
**Answer:** c) -4, 2.86

**12. Given a function y = (x + 30)². How many iterations does it need to reach the first negative value of the function starting from the point x = 1 using gradient descent (Assume the learning rate is 0.01)?**
**Answer:** c) 2

**13. Stochastic gradient descent is also known as on-line gradient descent.**
**Answer:** a) True

**14. Stochastic gradient descent (SGD) methods handle redundancy in the data much more efficiently than batch methods.**
**Answer:** a) True

**15. Which of the following statements is true about stochastic gradient descent?**
**Answer:** c) It processes one training example per iteration

**16. Which of the following statements is not true about the stochastic gradient descent?**
**Answer:** c) Stochastic gradient descent is faster than mini batch gradient descent

**17. Stochastic gradient descent falls under Non-convex optimization.**
**Answer:** b) False *(It can be used for both, but it's fundamentally a technique originating in convex optimization)*

**18. Which of the following statements is not true about stochastic gradient descent?**
**Answer:** d) It is computationally slower

**19. In stochastic gradient descent the high variance frequent parameter updates causes the loss function to fluctuate heavily.**
**Answer:** b) True

**20. Stochastic gradient descent has the possibility of escaping from local minima.**
**Answer:** b) True

**21. Given an example from a dataset (x1, x2) = (4, 1), observed value y = 2 and the initial weights w1, w2, bias b as -0.015, -0.038 and 0. What will be the prediction y’.**
**Answer:** d) 0.1 *(Calculated as 0.098 which is closest to 0.1)*

**22. Given an example from a dataset (x1, x2) = (2,8) and the dependent variable y = -14, and the model prediction y’ = -11. What will be the loss function if we are using a squared difference method?**
**Answer:** c) 9

**23. Given the current bias b = 0, learning rate = 0.01 and gradient = -4.2. What will be the b’ value after the update?**
**Answer:** b) 0.042

**24. Given the example from a data set x1 = 3, x2 = 1, observed value y = 2 and predicted value y’ = -0.05. What will be the gradient if you are using a squared difference method?**
**Answer:** a) -4.1

**25. Given the example from a data set x1 = 4, x2 = 1, weights w1 = -0.02, w2 = -0.03, bias b = 0, observed value y = 2, predicted value y’ = -0.11 and learning rate = 0.05. What will be the next weight updating values if you are using a squared difference approach?**
**Answer:** b) -0.864, -0.241

**26. Stochastic gradient descent cannot be used for risk minimisation.**
**Answer:** a) False

**27. Stochastic gradient descent can be used for convex-smooth learning problems.**
**Answer:** b) True

**28. Which of the following statements is not true about stochastic gradient descent for regularised loss minimisation?**
**Answer:** d) Stochastic gradient descent has entirely different worst-case sample complexity bound from regularised loss minimisation

**29. In convex learning problems where the loss function is convex, the preceding problem is also a convex optimisation problem.**
**Answer:** b) True


### **The Quick Comparison**

|**Feature**|**Simple Linear Regression**|**Multivariate Linear Regression**|**Polynomial Regression**|**Logistic Regression**|
|---|---|---|---|---|
|**Primary Goal**|Predict a continuous value|Predict a continuous value|Predict a continuous value|**Classify** into categories (usually binary)|
|**Input Features**|1 independent variable|2+ independent variables|1 or more variables, raised to powers|1 or more independent variables|
|**Shape of Fit**|Straight Line|Flat Hyperplane (Multidimensional)|Curve|S-Curve (Sigmoid)|
|**Output Range**|$-\infty$ to $+\infty$|$-\infty$ to $+\infty$|$-\infty$ to $+\infty$|$0$ to $1$ (Probability)|
|**Best Used For**|Simple, direct trends|Complex systems with many factors|Data with curves, peaks, or valleys|Yes/No, True/False decisions|

---

### **1. Simple Linear Regression**

This is the most basic form of machine learning. You have one feature ($x$) and you want to predict an outcome ($y$) by drawing the best possible straight line through your data points.

- **The Math:** $y = \theta_0 + \theta_1x$
    
- **How it works:** The algorithm finds the optimal intercept ($\theta_0$) and slope ($\theta_1$) that minimizes the mean squared error (MSE) between the predicted line and the actual data points.
    
- **Engineering Example:** Predicting the execution time of a sorting algorithm ($y$) based solely on the size of the input array ($x$).
    

### **2. Multivariate Linear Regression**

Real-world problems rarely depend on just one variable. Multivariate regression is the exact same concept as simple linear regression, but it scales up to handle multiple input features. Instead of drawing a line in 2D space, it draws a 2D plane in 3D space, or a multi-dimensional "hyperplane" in higher dimensions.

- **The Math:** $y = \theta_0 + \theta_1x_1 + \theta_2x_2 + \dots + \theta_nx_n$
    
- **How it works:** It assigns a different weight ($\theta_n$) to every single feature ($x_n$) based on how strongly that feature influences the target variable.
    
- **Engineering Example:** Predicting a computer's total power consumption ($y$) based on CPU load ($x_1$), active memory ($x_2$), and network bandwidth usage ($x_3$).
    

### **3. Polynomial Regression**

What happens if your data doesn't form a straight line, but instead forms a curve? If you try to fit a straight linear regression line to curved data, you will get terrible accuracy (underfitting). Polynomial regression solves this by creating new features that are powers of the original feature.

- **The Math:** $y = \theta_0 + \theta_1x + \theta_2x^2 + \theta_3x^3 + \dots + \theta_nx^n$
    
- **How it works:** Under the hood, this is actually just Multivariate Linear Regression. The algorithm treats $x$, $x^2$, and $x^3$ as if they were entirely separate variables ($x_1$, $x_2$, $x_3$). This allows the model to bend and fit curves, peaks, and valleys.
    
- **Engineering Example:** Modeling the relationship between a CPU's clock speed ($x$) and its heat generation ($y$), which often scales exponentially rather than strictly linearly.
    

### **4. Logistic Regression**

Despite having "regression" in the name, this is a **classification** algorithm. It is used when your target variable is categorical (e.g., 0 or 1, Spam or Not Spam, Malicious or Benign).

- **The Math:** $y = \frac{1}{1 + e^{-(\theta_0 + \theta_1x)}}$
    
- **How it works:** It takes a standard linear regression equation and wraps it inside a Sigmoid function. This mathematical trick squashes the straight line into an "S-shape" curve that is strictly bounded between 0 and 1. The output is treated as a probability. If the probability is $> 0.5$, it predicts Class 1; otherwise, Class 0.
    
- **Engineering Example:** Analyzing an incoming network packet's features to classify whether it is a normal request ($0$) or a DDoS attack ($1$).
    

---

To understand the reasoning behind these answers, we must first look at the mathematical foundation they are built upon.

In logistic regression, the generalized cost function for a single training example (also known as Log Loss or Binary Cross-Entropy) is defined as:

$$Cost(h(x), y) = -y \log(h(x)) - (1 - y) \log(1 - h(x))$$

Where:

- **$y$** is the true label (it can only be exactly $0$ or exactly $1$).
    
- **$h(x)$** is the model's predicted probability (a value between $0$ and $1$).
    

Here is the step-by-step mathematical reasoning for each highlighted question based on this formula:

---

### **Question 2: $h(x) = y$. What is the cost $(h(x), y)$?**

**Answer: c) 0**

**Reasoning:**

If $h(x) = y$, it means the model's prediction perfectly matches the true label. Since $y$ can only be $0$ or $1$ in binary classification, there are two possible scenarios to evaluate:

- **Case 1: The true label $y = 1$ (which means $h(x) = 1$)**
    
    Substitute these values into the cost function:
    
    $$Cost(1, 1) = -1 \cdot \log(1) - (1 - 1) \cdot \log(1 - 1)$$
    
    $$Cost(1, 1) = -1 \cdot (0) - 0 \cdot \log(0) = 0$$
    
    _(Note: In limit calculations, $0 \cdot \log(0)$ is treated as $0$)_.
    
- **Case 2: The true label $y = 0$ (which means $h(x) = 0$)**
    
    Substitute these values into the cost function:
    
    $$Cost(0, 0) = -0 \cdot \log(0) - (1 - 0) \cdot \log(1 - 0)$$
    
    $$Cost(0, 0) = 0 - 1 \cdot \log(1) = 0 - 0 = 0$$
    

In both cases, a perfect prediction results in an error (cost) of exactly $0$.

---

### **Question 4: Let $m$ be the number of training instances. What is the summation of cost function multiplied by to get the gradient descent?**

**Answer: a) $1/m$**

**Reasoning:**

The cost function equation provided above calculates the error for a **single** training instance. However, to evaluate how well the model is performing overall and to update weights using gradient descent, you need the _Total Cost_ (usually denoted as $J$) across the entire dataset.

To find the average error across the entire dataset, you sum up the individual costs of all instances, and then divide by the total number of instances ($m$).

Mathematically, dividing the sum by $m$ is the exact same operation as multiplying the summation by $\frac{1}{m}$:

$$J(\theta) = \frac{1}{m} \sum_{i=1}^{m} Cost(h_\theta(x^{(i)}), y^{(i)})$$

---

### **Question 5: $y = 1$. How does cost$(h(x), y)$ change with $h(x)$?**

**Answer: c) cost$(h(x), y) = 0$ when $h(x) = 1$**

**Reasoning:**

Let's plug $y = 1$ into our generalized formula to see how the function simplifies when the true answer is positive:

$$Cost(h(x), 1) = -1 \cdot \log(h(x)) - (1 - 1) \cdot \log(1 - h(x))$$

$$Cost(h(x), 1) = -\log(h(x)) - 0 \cdot \log(1 - h(x))$$

$$Cost(h(x), 1) = -\log(h(x))$$

Now, the question states that the model's prediction is $h(x) = 1$. Plug $1$ into our simplified formula:

$$Cost(1, 1) = -\log(1)$$

Because the logarithm of $1$ is exactly $0$, the cost evaluates to $0$. Intuitive meaning: If the truth is $1$, and your model is 100% confident the answer is $1$, there is zero error.

---

### **Question 8: $h(x) = 1, y = 0$. What is the cost $(h(x), y)$?**

**Answer: b) infinite**

**Reasoning:**

Let's plug the true label $y = 0$ into our generalized formula to see how the function simplifies when the true answer is negative:

$$Cost(h(x), 0) = -0 \cdot \log(h(x)) - (1 - 0) \cdot \log(1 - h(x))$$

$$Cost(h(x), 0) = 0 - 1 \cdot \log(1 - h(x))$$

$$Cost(h(x), 0) = -\log(1 - h(x))$$

Now, plug in the model's prediction $h(x) = 1$:

$$Cost(1, 0) = -\log(1 - 1)$$

$$Cost(1, 0) = -\log(0)$$

In mathematics, as a value approaches $0$ from the right, its logarithm approaches negative infinity ($\log(0) \to -\infty$).

Therefore:

$$Cost(1, 0) = -(-\infty) = \infty$$

**Intuitive meaning:** The actual answer is $0$ (False), but the model predicted $1$ (True) with absolute, 100% certainty. The algorithm heavily penalizes a model that is both completely wrong and entirely confident, resulting in an infinite cost.