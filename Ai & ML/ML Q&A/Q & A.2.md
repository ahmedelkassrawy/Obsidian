**Question 1: A retail store wants to classify customers based on their past purchases for marketing purposes. Which of the following is a suitable model for this scenario?**

**Answer: Decision tree** Explanation: Decision trees are well-suited for customer classification based on past purchases because they handle categorical and numerical data effectively, are interpretable, and can capture complex patterns in customer behavior. K-nearest neighbors and Naïve Bayes are also viable, but decision trees are often preferred for their simplicity and ability to handle diverse datasets. Neural networks, while powerful, are typically overkill for this task unless the dataset is very large and complex.

---

**Question 2: Which voting scheme can be used to assign the final label in a one-versus-one classification approach?**

**Answer: Popularity vote** Explanation: In a one-versus-one (OvO) classification approach, multiple binary classifiers are trained for each pair of classes. The final label is determined by aggregating the predictions of these classifiers, typically through a majority vote (popularity vote), where the class with the most votes is selected. Random selection is not systematic, probability weighing is more relevant to probabilistic models, and one-hot encoding is a data preprocessing technique, not a voting scheme.

---

**Question 3: You want to determine the best feature to split the data at each node while building a decision tree. Which of the following criteria will you use?**

**Answer: Information gain** Explanation: In decision trees, the best feature to split on at each node is typically chosen based on information gain, which measures the reduction in entropy (or increase in purity) after a split. Accuracy score is a model evaluation metric, mean squared error is used for regression tasks, and random selection would not optimize the tree’s performance.

---

**Question 4: You want to evaluate the quality of each split while building a regression tree. Which criterion is commonly used in this task?**

**Answer: Mean squared error (MSE) method** Explanation: In regression trees, the quality of a split is commonly evaluated using the mean squared error (MSE), which measures the reduction in variance of the target variable after the split. Entropy reduction is used for classification trees, exhaustive search is a method for finding splits, and midpoints method is not a standard criterion.

---

**Question 5: You are using K-nearest neighbors (KNN) to classify customer behavior into loyalty categories. How does increasing the value of k affect the KNN model?**

**Answer: Causes underfitting by generalizing too much** Explanation: Increasing the value of k in KNN means considering more neighbors when making a prediction, which smooths the decision boundary and can lead to underfitting by overly generalizing the model. This reduces sensitivity to noise but may miss finer patterns in the data. Overfitting is more likely with smaller k, and the other options are not accurate descriptions of k’s effect.