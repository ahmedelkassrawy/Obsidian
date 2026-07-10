### 1. Data Drift (Feature Drift)

**The Concept:** The relationship between your inputs and outputs hasn't changed, but the _distribution_ of your input data has shifted. The data the model is seeing in production looks very different from the data it was trained on.

- **Telecom Example:** You trained a model to predict churn based on "monthly data usage." During training, the average user consumed 10GB of data. Six months later, Orange launches a massive 5G marketing campaign, and suddenly everyone is streaming 4K video, pushing the average usage to 50GB.
    
- **The Problem:** The model has never seen numbers this high and doesn't know how to weigh them, leading to unpredictable outputs. The underlying inputs ($X$) have shifted.
    

### 2. Concept Drift

**The Concept:** The fundamental relationship between your inputs and your target variable has changed. What was true yesterday is no longer true today. The statistical relationship $P(y|X)$ has fundamentally shifted.

- **Telecom Example:** You train a model to predict if a user will upgrade to a premium plan. In 2025, a user buying an international roaming add-on was a strong indicator they were a wealthy customer likely to upgrade. In 2026, a competitor drops their roaming fees to zero, so Orange does the same. Suddenly, _everyone_ has roaming.
    
- **The Problem:** Roaming is no longer a signal for "wealthy customer likely to upgrade." The rules of the game changed, and the model's logic is now flawed.
    

### How do we detect it?

This is where MLOps monitoring tools (like Evidently AI, or custom scripts tracking MLflow metrics) come in. To catch drift before it impacts the business, we rely heavily on **statistics and probability**.

Detecting drift is essentially running continuous, automated **hypothesis testing** in the background:

- **Null Hypothesis ($H_0$):** The probability distribution of the live data is the same as the training data.
    
- **Alternative Hypothesis ($H_A$):** The distributions are significantly different.
    
    You establish confidence intervals around your baseline metrics. When the real-time data distributions drift outside those intervals—measured by statistical tests like the Kolmogorov-Smirnov (K-S) test or Population Stability Index (PSI)—an alarm goes off.
    

### The MLOps Solution: Continuous Training (CT)

When your automated hypothesis tests detect drift and trigger an alert, an MLOps pipeline doesn't require a human to manually fix everything.

Instead, it triggers a **Continuous Training (CT)** pipeline:

1. The system automatically pulls the latest, freshest data (e.g., the last 30 days of new 5G usage).
    
2. It retrains the model on this new data.
    
3. It evaluates the new model against the old, drifting model.
    
4. If the new model performs better, it is seamlessly deployed to replace the old one.
---
example: "Model: Fraud Detection. Alert: Accuracy has dropped from 94% to 81% over the last 48 hours."

In this scenario, you are actually experiencing **Concept Drift**, not just Data Drift.

- **Why?** Because the fundamental _definition_ of what a scam looks like has changed in the real world. The model learned the rules for the _old_ scams. The hackers invented a _new_ rulebook. The relationship between the inputs and the output (Fraud: Yes/No) has fundamentally shifted.

- Since the accuracy dropped due to a new scam tactic, we are facing Concept Drift.
- I wouldn't manually intervene. Instead, I would rely on the Continuous Training (CT) pipeline. 
- The pipeline should automatically ingest the network data from the last 48 hours—which contains the new phishing patterns—retrain the model to recognize them, validate that the accuracy improves, and deploy the updated model to production."

---
"We have a team of data scientists who just finished building a fantastic Python model that predicts which of our 5G cell towers are going to experience heavy network congestion in the next hour. Right now, it's just sitting in a Jupyter Notebook on someone's laptop. As our new MLOps intern, walk me through the steps you would take to get this model out of that notebook and into a reliable, automated production environment. What tools are you thinking about using, and how do we ensure it stays accurate a month from now?"

_"First, I would get the code out of the Jupyter Notebook. I'd refactor it into clean Python scripts, define the dependencies, and use **MLflow** to track the model version and parameters._

_Next, I'd run automated evaluations—perhaps using a tool like **Evidently**—to ensure it performs well against baseline data._

_Once approved, I would package the model and its environment using **Docker**. Because telecom data operates at a massive scale, I would deploy those Docker containers onto a **Kubernetes** cluster to handle the load and auto-scaling._

_Finally, I wouldn't just leave it there. I'd set up monitoring to watch for data or concept drift. If the network traffic patterns change and accuracy drops, it would trigger a **Continuous Training** pipeline to retrain the model on the freshest data."_