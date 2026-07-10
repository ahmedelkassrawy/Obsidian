Data extraction, Model training, Model evaluation, Model deployment, and Model monitoring.

### 1. Data Extraction
- **The Goal:** Programmatically pull the required data (e.g., call durations, billing history, network usage) from various sources into a centralized environment for the model to use.
    
- **MLOps Context:** This process must be automated and reproducible. 
- If the model needs retraining next month, the extraction pipeline should seamlessly pull the newest data without manual intervention.
### 2. Model Training
You don't just train one model; you experiment with dozens. MLOps tools (like MLflow) track every experiment—recording which dataset was used, the hyperparameters (settings), and the resulting accuracy. This ensures you can always reproduce a good result.
### 3. Model Evaluation
- **The Goal:** Test the model on a holdout dataset (data it has never seen) to ensure it generalizes well and doesn't just memorize the training data.
- This step is automated in a CI/CD pipeline.
- The system checks metrics like Precision and Recall. 
- If the new model performs worse than the current production model, the pipeline automatically halts the deployment.

### 4. Model Deployment
- **The Goal:** Make the model accessible so other applications
- The model is packaged into a container (using Docker) with all its dependencies.
- Then deployed to a server or cloud cluster (managed by Kubernetes), often exposed as a REST API. 
- This ensures it runs consistently and can scale up if millions of predictions are needed at once.
    
### 5. Model Monitoring
- A model's accuracy is highest the moment it is deployed. 
- After that, it degrades because the real world changes.
- **The Goal:** Continuously watch the model's performance in the wild.
    
- We monitor for **Data Drift** (when the input data changes) , e.g., a new 5G plan alters customer usage patterns
- **Concept Drift** (when the relationship between inputs and outputs changes). 
- If accuracy drops below a threshold, the monitoring system triggers an alert to automatically restart the pipeline at Step 1 to retrain the model.