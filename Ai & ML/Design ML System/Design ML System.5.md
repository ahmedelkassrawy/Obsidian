#### Chapter 8. Data Distribution Shifts and 
His company learned the hard way an important lesson that the rest of the industry is also discovering: deploying a model isn’t the end of the process. A model’s performance degrades over time in production. Once a model has been deployed, we still have to continually monitor its performance to detect issues as well as deploy updates to fix these issues.
We’ll start by covering reasons why ML models that perform great during development fail in production.
## Introduction to ML Model Monitoring

- ML models in production often **degrade over time**.
- This degradation occurs because the underlying data distribution may change, or the model's performance may degrade due to issues that need to be detected.
- **Monitoring** is essential to continuously observe model performance and detect problems.
- Understanding the **causes of ML system failures** and **data distribution shifts** is critical.

## Causes of ML System Failures

- An ML system failure occurs when **one or more operational expectations are violated**.
- There are two main types of failures: **software system failures** and **ML-specific failures**.

### Software System Failures

- These are failures that **would have occurred even in non-ML systems**.
- Common types include:
    - **Dependency failure**: Issues with a software package or codebase that relies on other systems, often third-party ones.
    - **Deployment failure**: Problems during the deployment of the model, such as incorrect permissions for binaries or failure to write necessary files.
    - **Hardware failures**: Malfunctions of CPUs, GPUs, or other hardware components.
    - **Downtime or crashing**: A component of the system running on a server (e.g., AWS, a hosted service) goes down.
- Many ML system failures (e.g., 60 out of 96 Google failures in one review) are not ML-specific but relate to **distributed systems, data pipelines, and orchestration**.
- **Traditional software engineering skills** are crucial for building robust ML systems; ML engineering is primarily engineering, not just machine learning.

### ML-Specific Failures

- These failures are specific to ML systems and arise from issues like **data collection/processing problems, poor hyperparameters, changes in the training pipeline not replicated in inference, and data distribution shifts**.
- **Production data often differs from training data**, which is a major cause of ML-specific failures.
    - The model learns to predict from the training data, and the goal is to **generalize to unseen data** and maintain performance.
    - One common cause is when the **training data is different from the production data**.
    - **Training-serving skew** refers to the phenomenon where a model performs poorly because its real-world properties diverge from the training data it was built on.
    - Examples of such shifts include:
        - A model trained in one city and deployed in another.
        - Seasonal changes (e.g., holidays, weather) affecting user behavior and data distribution.
        - The **Wuhan during COVID-19 pandemic** example, where changes in user movement significantly impacted data distribution for a travel-related model.
    - Other operational expectation violations can be due to **missing values, inconsistencies in features, incorrect model versions, or bugs**.

### Edge Cases

- **Edge cases** are data samples that are so extreme or unusual that they cause the model to make **catastrophic mistakes**.
- They can often indicate that the **underlying data distribution has shifted**.
- Examples include autonomous vehicles facing rare scenarios, medical diagnosis systems misidentifying diseases, or customer service chatbots giving inappropriate responses.
- An **outlier** is a data point that **differs significantly from other examples** in the dataset.
- Detecting and addressing outliers can **improve model performance and generalization**.

### Degenerate Feedback Loops

- A **degenerate feedback loop** occurs when a model's predictions or outputs **influence the data it is trained on**, leading to a self-reinforcing, often negative, cycle.
- While some feedback loops are beneficial (e.g., "Natural Labels"), degenerate ones cause **model performance to decrease** over time.
- A classic example is in **recommender systems**: if a model consistently recommends only popular items, users may only click on those, leading to a biased training set that reinforces the popularity bias.
- Consequences of degenerate feedback loops include **reduced diversity in recommendations, "filter bubbles," and "echo chambers"**.
- To mitigate degenerate feedback loops:
    - Introduce **randomization** to break the loop, such as randomly showing less popular items.
    - Estimate the **unbiased value** of items (e.g., songs) independent of the feedback loop.
    - Use **positional features** (e.g., the position of a recommended item in a list) as inputs to the model to account for user interaction bias.

## Data Distribution Shifts

- **Data distribution shifts** refer to changes in the statistical properties of the data over time. This is a common and significant problem in ML systems.
- The **joint distribution P(X, Y)** represents the probability of inputs (X) and outputs (Y) occurring together.
- There are three primary types of data distribution shifts:
    - **Covariate shift**: Occurs when the distribution of the **input features P(X) changes**, but the relationship between inputs and outputs **P(Y|X) remains the same**.
        - Example: If the demographics of a city change, but a breast cancer prediction model's accuracy for a given demographic remains the same.
    - **Label shift**: Occurs when the distribution of the **output labels P(Y) changes**, but the conditional probability of inputs given labels **P(X|Y) remains the same**.
        - Example: An increase in breast cancer incidence, while the characteristics of affected women (e.g., age, income) remain consistent.
    - **Concept drift**: Occurs when the **relationship between inputs and outputs P(Y|X) changes**.
        - Example: The true price of a house in San Francisco changes due to new market conditions, not just changes in its features. Or flight prices fluctuate based on holiday seasons.
- **General data distribution shifts** encompass broader changes, including feature changes (e.g., adding/removing features) or label schema changes (e.g., changing sentiment categories from "POSITIVE/NEGATIVE" to "SAD/ANGRY").
- The primary impact of distribution shifts is **degraded model performance**.

### Detecting Data Distribution Shifts

- It is often challenging to detect shifts because **ground truth labels (Y) are frequently unavailable or delayed** in production.
- Monitoring often focuses on the **distribution of input features P(X)**, and sometimes predictions P(Y|X) or the joint distribution P(X, Y).
- **Statistical tests** are used to determine if two data populations (e.g., training vs. production data) are significantly different.
    - Examples include the **Kolmogorov-Smirnov test**, **Anderson-Darling test**, and **Maximum Mean Discrepancy (MMD)**.
    - The `Detect` open-source package offers implementations of many drift detection algorithms.
- **Time scale windows** are important for detecting shifts, as they can be sudden or gradual. Monitoring over different time windows (e.g., daily, weekly) is necessary.
    - **Cumulative sliding windows** are better for detecting sudden shifts than simple cumulative windows.
    - Tools like **Root Cause Analysis (RCA)** features can help understand why a data change happened.

### Addressing Data Distribution Shifts

- Common strategies to address data distribution shifts include:
    - **Retraining ML models** periodically or when shifts are detected. Retraining frequency can range from monthly to hourly.
    - **Adding new features** or modifying existing ones to better capture the evolving data characteristics.
    - Utilizing **unsupervised domain adaptation** and **transfer learning** techniques to adapt models to new data distributions without requiring new labels.
    - Revising the **retraining strategy**, such as determining which data (e.g., the last 24 hours, last week) should be used for retraining.
    - Focusing on adapting the model to the **new joint distribution P(X, Y)**, not just the input distribution P(X).

## Monitoring and Observability

- **Monitoring** and **observability** are critical for managing ML systems in production.
- **Monitoring** involves tracking, measuring, and correlating various metrics to understand system behavior.
- **Observability** focuses on understanding the internal state of a system from its external outputs, helping to explain _why_ something is happening.

### Monitoring ML Systems

- **Operational metrics** include latency, throughput, CPU utilization, and memory usage.
- **ML-specific metrics** are crucial for understanding model performance:
    - **Raw inputs**: Monitoring the original data fed into the system.
    - **Features**: Tracking processed features, ensuring they conform to expectations.
        - **Feature validation**: Defining **expectations** for features (e.g., min/max values, data types, unique values, allowed ranges) to ensure data quality. Tools like Great Expectations and TensorFlow Extended can assist.
    - **Predictions**: Monitoring the model's outputs and their distribution.
    - **Accuracy**: Tracking model performance over time, often requiring delayed ground truth.
- Monitoring should be **continuous**, potentially occurring every hour.
- **Dashboards** are useful for visualizing metrics over time, allowing for the detection of trends and shifts. However, dashboards can be misleading if the underlying metrics are inappropriate.

### Observability in ML Systems

- **Telemetry** is a core concept of observability, encompassing metrics, logs, and traces.
    - **Metrics**: Numerical values representing system behavior, often aggregated over time.
    - **Logs**: Records of discrete events within the system.
    - **Traces**: Represent the end-to-end paths of requests through various system components.
- Observability aims to provide **better visibility** into the complex behavior of software systems.

### Alerts

- **Alerts** notify stakeholders when a monitoring condition is met.
- An alert policy defines the conditions that trigger an alert (e.g., model accuracy falling below a threshold, HTTP response latency exceeding 10 minutes).
- **Notification channels** can include email, Slack, or PagerDuty.
- Alerts should be **actionable**, providing clear information for addressing the issue.
- It's important to minimize **false positives** (alerts without a real problem) and **false negatives** (missed problems).