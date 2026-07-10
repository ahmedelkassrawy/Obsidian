# Machine Learning Systems Notes

## Characteristics of ML Problems

ML algorithms thrive in problems with the following characteristics:

1. **Repetitive Tasks**
    
    - Patterns repeat multiple times, making it easier for ML to learn.
    - Example: Recommender systems benefit from repetitive user interactions.
2. **Low Cost of Wrong Predictions**
    
    - Errors are forgiving, e.g., a bad recommendation in a recommender system is ignored by users.
    - Common in systems like ad recommendations where users skip irrelevant suggestions.
3. **At Scale**
    
    - "At scale" varies by task, e.g., large datasets or high request volumes.
    - Example: Social media platforms processing millions of daily predictions.
4. **Constantly Changing Patterns**
    
    - ML models can adapt to new data without needing to understand how data changes.
    - Systems can be set up to handle shifting data distributions automatically.

## Business and ML Objectives

### Key Points

- Businesses prioritize **business metrics** over ML metrics (e.g., profit, sales, customer satisfaction).
- ML success depends on tying model performance to business outcomes.
- Examples:
    - **E-commerce**: Improve purchase-through rate with online predictions for better relevance.
    - **Ad Systems**: Higher click-through rates directly increase ad revenue.
    - **Fraud Detection**: Each stopped fraudulent transaction saves money.

### Mapping ML to Business Metrics

- **Netflix Example**:
    - Metric: **Take-rate** (quality plays ÷ recommendations seen).
    - Higher take-rate correlates with increased streaming hours and lower cancellation rates.
- **Experiments**:
    - A/B testing to evaluate ML models based on business metrics, not just ML accuracy.
    - Example: A model with lower ML accuracy might improve business outcomes.

### Challenges

- Complex systems (e.g., cybersecurity) make it hard to trace ML’s impact on business metrics.
    - Example: ML detects anomalies, but downstream processes (logic, human review) obscure its role.
- Some companies use "AI-powered" branding to attract customers, even if ML’s impact is unclear.

## Requirements for ML Systems

### 1. Reliability

- Systems must perform correctly despite hardware/software faults or human errors.
- **Challenge**: ML systems can fail silently (e.g., wrong predictions without warnings).
    - Example: Google Translate errors may go unnoticed by users unfamiliar with the target language.
- Unlike traditional software, ML lacks clear error signals like crashes or 404 errors.

### 2. Scalability

- ML systems grow in:
    - **Complexity**: From simple models (e.g., logistic regression) to large neural networks.
    - **Traffic Volume**: From 10,000 to 1–10 million daily prediction requests.
    - **Model Count**: From one model to thousands (e.g., one per enterprise customer).
- **Resource Scaling**:
    - **Up-scaling**: Add resources (e.g., 100 GPUs at peak).
    - **Down-scaling**: Reduce resources (e.g., 10 GPUs normally) to save costs.
    - **Autoscaling**: Automatically adjust resources based on demand (e.g., Amazon’s Prime Day crash cost $72–99M).
- **Artifact Management**:
    - Managing many models requires automation for monitoring and retraining.
    - Example: Reproducing 100 models vs. one requires systematic version control.

### 3. Maintainability

- Infrastructure should support diverse tools for contributors.
- Requirements:
    - Documented code.
    - Versioned code, data, and artifacts.
    - Reproducible models for continuity without original authors.
- Enables collaborative problem-solving without blame.

### 4. Adaptability

- Systems must adapt to changing data distributions and business needs.
- Requires:
    - Performance monitoring for improvement opportunities.
    - Updates without service interruptions.
- Ties closely to maintainability due to rapid data changes.

## Iterative Process of ML System Development

- Developing ML systems is a **cyclic, ongoing process**, not linear.
- Example Workflow (Ad Prediction System):
    1. Choose a metric (e.g., ad impressions).
    2. Collect and label data.
    3. Engineer features.
    4. Train models.
    5. Error analysis reveals issues (e.g., wrong labels).
    6. Relabel data and retrain.
    7. Address data imbalance (e.g., 99.99% negative labels).
    8. Collect balanced data and retrain.
    9. Model performs well on old data but poorly on new data (stale model).
    10. Update with recent data and retrain.
    11. Deploy the model.
    12. Business reports declining revenue (e.g., low click-through rates).
    13. Adjust metric (e.g., optimize for click-through rate) and restart.

![[Pasted image 20250724173514.png]]

### Process Steps

1. **Project Scoping**
    - Define goals, objectives, constraints, and stakeholders.
    - Estimate and allocate resources.
2. **Data Engineering**
    - Handle data from various sources/formats.
    - Curate training data via sampling and labeling.
3. **ML Model Development**
    - Extract features and develop models.
    - Requires deep ML knowledge (feature engineering, model selection, training, evaluation).
4. **Deployment**
    - Make models accessible to users.
    - Deployment is a milestone, not an endpoint.
5. **Monitoring and Continual Learning**
    - Monitor performance decay.
    - Adapt to changing environments/requirements.
6. **Business Analysis**
    - Evaluate model performance against business goals.
    - Generate insights to refine or scope new projects.

# Framing Machine Learning Problems

## Case Study: Customer Service at a Bank

- **Scenario**: As an ML engineering tech lead at a bank targeting millennials, your boss wants to use ML to speed up customer service support, inspired by a rival bank that processes requests twice as fast.
- **Problem**: Slow customer support is a business issue, but not inherently an ML problem.
    - **ML Problem Definition**: Requires defining inputs, outputs, and an objective function.
- **Investigation**:
    - Bottleneck: Routing customer requests to the correct department (Accounting, Inventory, HR, IT).
    - **Solution**: Develop an ML model to predict the appropriate department for each request.
- **Framed as an ML Problem**:
    - **Task Type**: Classification problem.
    - **Input**: Customer request (text or structured data).
    - **Output**: One of the four departments (Accounting, Inventory, HR, IT).
    - **Objective Function**: Minimize the difference between predicted and actual department assignments.
- **Next Steps**:
    - Feature extraction from raw data (covered in Chapter 5).
    - Focus here: Model output and objective function.

## Task Types in Classification
![[Pasted image 20250724174209.png]]
### Binary vs. Multiclass Classification

- **Binary Classification**:
    - Simplest form with two classes.
    - Examples:
        - Classifying a comment as toxic or non-toxic.
        - Detecting cancer in lung scans (cancerous or non-cancerous).
        - Identifying fraudulent transactions (fraudulent or legitimate).
    - Easier to handle due to:
        - Intuitive metrics (e.g., F1 score).
        - Clear visualization (e.g., confusion matrices).
    - **Why Common?**: Either naturally prevalent or preferred by ML practitioners for simplicity.
- **Multiclass Classification**:
    - More than two classes.
    - Example: Classifying customer requests into Accounting, Inventory, HR, or IT.
    - **Challenges**:
        - **High Cardinality**: When the number of classes is large (e.g., thousands of diseases or products).
            - Requires significant data: ~100 examples per class (e.g., 1,000 classes need 100,000 examples).
            - Rare classes complicate data collection.
        - **Solution**: Hierarchical classification.
            - Step 1: Classify into broad groups (e.g., electronics, fashion).
            - Step 2: Classify into subgroups (e.g., shoes, shirts).
            - Example: Product classification into categories (electronics) then subcategories (phones, laptops).

### Multiclass vs. Multilabel Classification

- **Multiclass Classification**:
    - Each example belongs to exactly one class.
    - Example: An article is classified as _tech_ or _finance_, but not both.
    - Label representation: One-hot vector (e.g., `[0, 1, 0, 0]` for _entertainment_).
- **Multilabel Classification**:
    - Each example can belong to multiple classes.
    - Example: An article can be both _tech_ and _finance_.
    - Label representation: Binary vector (e.g., `[0, 1, 1, 0]` for _entertainment_ and _finance_).
- **Approaches to Multilabel Classification**:
    1. **Treat as Multiclass**:
        - Use a single model with a binary vector output for all classes.
        - Example: `[0, 1, 1, 0]` for an article with _entertainment_ and _finance_ labels.
    2. **Set of Binary Classifiers**:
        - Train one binary model per class (e.g., _Is this tech? Yes/No_).
        - Example: Four models for _tech_, _entertainment_, _finance_, _politics_.
- **Challenges in Multilabel Classification**:
    - **Label Annotation**:
        - Annotators may disagree on the number of labels per example.
        - Increases label multiplicity issues (covered in Chapter 4).
    - **Prediction Extraction**:
        - Hard to determine how many labels to assign from raw probabilities.
        - Example: For probabilities `[0.45, 0.2, 0.02, 0.33]`, do you pick the top 2 or 3 classes?
        - Multiclass: Pick the highest probability (e.g., 0.45).
        - Multilabel: Number of labels varies, complicating thresholding.

## Summary

- **Framing ML Problems**:
    - Translate business problems (e.g., slow customer service) into ML problems by defining inputs, outputs, and objective functions.
    - Example: Classifying customer requests into departments to reduce routing delays.
- **Business Alignment**:
    - ML systems must align with business objectives (e.g., faster request processing).
    - Business metrics (e.g., response time) take precedence over ML metrics (e.g., model accuracy).
- **System Requirements**:
    - ML systems should be reliable, scalable, maintainable, and adaptable.
    - Techniques to achieve these are covered in later chapters.
- **Iterative Process**:
    - ML development is cyclic, involving scoping, data engineering, model development, deployment, monitoring, and business analysis.
- **Data’s Role**:
    - Large datasets drive ML success (e.g., AlexNet, BERT, GPT).
    - Data engineering is critical and covered in subsequent chapters.
- **Next Steps**:
    - Dive into data engineering fundamentals (Chapter 3).
    - Explore feature engineering (Chapter 5) and model development (Chapter 6).
## Key Takeaways

- Align ML systems with business objectives for success.
- Ensure systems are reliable, scalable, maintainable, and adaptable.
- ML development is iterative, requiring constant monitoring and updates.
- Experiments (e.g., A/B testing) are critical to validate ML’s business impact.