# MLOps Complete Guide

## Introduction: Understanding Business Problems in ML Projects

The most important phase in any software project is to understand the business problem and create requirements. **ML-based software** is no different here.

- **Initial Step**: Conduct a thorough study of business problems and requirements.
- **Translation**: These requirements are translated into **model objectives** and **model outputs**.
- **Key Specifications**:
    - Possible errors.
    - Minimum success criteria for launching.
- **Most Useful Question**: "How costly are wrong predictions?"
    - Answering this defines the **feasibility** of the ML project.

## Workflow Decomposition

Each task of the entire business process needs to be decomposed into its constituent elements to identify where **prediction (ML model)** can be introduced.

### The Workflow Decomposition Process

To answer "how to implement AI/ML", follow these steps:

1. **Identify the Concrete Process**: Select a process that might be powered by AI/ML (see [[Figure: Workflow Decomposition]]).
2. **Decompose the Process**: Break it into a **directed graph of tasks**.
3. **Identify Human-Replacable Tasks**: Determine what tasks can be replaced by a prediction element (e.g., ML model).
4. **Estimate ROI**: Calculate the **Return on Investment (ROI)** for implementing an AI/ML tool for each task.
5. **Rank-Order Tasks**: Prioritize AI/ML implementations based on ROI.
6. **Structure Implementation**: Start from the top of the list and complete either the **AI Canvas** or the **Machine Learning Canvas**.

- **Purpose of Canvases**: These tools structure the breakdown process and articulate:
    - What needs to be predicted.
    - How to react to errors in predictions.

## AI Canvas

The **AI Canvas** was proposed by A. Agrawal et al. in their book _Prediction Machines: The Simple Economics of Artificial Intelligence_ (2018). It is an aid for contemplating, building, and assessing AI tools.

- **Description**: See [[Figure: AI Canvas by Agrawal et al.]] for an example and component descriptions.
- **Figure Source**: [Noted in original text].

**When to Use**: For high-level structuring of ML/AI implementations.

## Machine Learning Canvas

While the AI Canvas provides a high-level structure, the **Machine Learning Canvas** (suggested by Louis Dorard) specifies both the vision and specifics of the ML system.

- **Initial Steps**:
    - Identify the **objective**: What do we want to achieve for end-users?
    - Connect the business goal to the **ML task**.
- **Central Block**: **Value Proposition** – Describes products/services that create value for customers.
    - Key Questions:
        - What problems are we solving?
        - Why is it important?
        - Who is the end-user?
        - What value does the ML project deliver?
        - How will they use the outputs/predictions?
    - **Template for Value Proposition** (Geoffrey Moore's):
        
        > **For** (target customer) **who** (need or opportunity), **our** (product/service name) **is** (product category) **that** (benefit).
        
    - **Tip**: Narrow the domain (e.g., build a bot for scheduling conference calls instead of a universal chatbot).

The canvas is divided into three categories:

- **Learning**: How the ML model is learned.
- **Prediction**: How predictions are performed.
- **Evaluation**: Methods and metrics for model/system evaluation.

### Detailed Blocks in the Machine Learning Canvas

See [[Figure: Machine Learning Canvas]] for an example by Louis Dorard. The canvas has **10 compound blocks**:

#### 1. Value Proposition

- Crucial block for clarifying objectives.
- Questions:
    - What is the problem? Objective? What for the end-user?
    - Why important?
    - Who is the end-user? (Specify persona.)
- Output: Effective statement using the template above.

#### 2. Data Sources

- Clarify available/possible data for ML training.
- Examples of Sources:
    - Internal/external databases.
    - Data marts, OLAP cubes, data warehouses, OLTP systems.
    - Hadoop clusters.
    - REST APIs.
    - Static files, spreadsheets.
    - Web scraping.
    - Outputs from other (ML) systems.
    - Open-source datasets (e.g., Kaggle Datasets, Google's Dataset Search, UCI Repository, Wikipedia's list of datasets for ML research).
- **Hidden Costs to Consider**:
    - Data storage expenses.
    - Purchasing external data.
    - Data access tools/processes.

#### 3. Prediction Task

- Brainstorm ML type after data clarification.
- Key Questions:
    - Supervised or unsupervised learning?
    - Anomaly detection?
    - Recommendation (option selection)?
    - Regression (continuous value)?
    - Classification (category prediction)?
    - Clustering (grouping data)?
    - If supervised: Classification, regression, or ranking?
    - If classification: Binary or multiclass?
    - Input for prediction? (e.g., Email text.)
    - Output? (e.g., "spam" vs. "regular".)
    - Model complexity? (e.g., Ensemble learning? Hidden layers in deep learning?)
    - Complexity costs? (Training/inference time.)

#### 4. Features (Engineering)

- Specify how input data is represented for ML algorithms.
- Questions:
    - How to extract features from raw sources?
    - Involve domain experts for important data aspects.

#### 5. Offline Evaluation

- Set up evaluation methods/metrics before deployment.
- Specifications:
    - Domain-specific metrics (e.g., simulated revenue vs. traditional methods).
    - Technical metrics: Precision, Recall, F1-measure, Accuracy.
    - Meaning of errors (false positives/negatives).
    - Test data: What is it? How much for confidence?

#### 6. Decisions

- Specify post-prediction actions.
- Questions:
    - How are predictions used for decisions?
    - End-user/system interaction? (e.g., Product recommendations; Spam classification.)
    - Hidden costs? (e.g., Human in the loop.)

#### 7. Making Predictions

- Details on prediction timing for new inputs.
- Questions:
    - When available? (On app open, on request, scheduled.)
    - On-the-fly or batch?
    - Inference complexity?
    - Human in the loop?

#### 8. Collecting Data

- Gather info on new data for re-training to prevent model decay.
- Questions:
    - How to label new data?
    - Costs: Collection, processing (e.g., images/sound/video)?
    - Human in the loop for cleaning/labeling?

#### 9. Building Models

- Address model updates/re-training.
- Questions:
    - Frequency? (Hourly, weekly, per data point.)
    - Hidden costs? (Cloud resources; Pricing via Google Cloud Calculator, Amazon ML Pricing, Microsoft Azure Calculator.)
    - Training time?
    - Scaling issues?
    - Tech stack changes? (Adapt to new tools/workflows.)

#### 10. Live Evaluation and Monitoring

- Post-deployment evaluation using **S.M.A.R.T.** metrics (Specific, Measurable, Achievable, Relevant, Time-bound).
- Questions:
    - Track performance? (e.g., A/B Testing.)
    - Evaluate value? (e.g., Less time spent by users.)
- Ensure model and business metrics correlate.

## Deliverables and Decision Points

- **Deliverable**: Completed **Machine Learning Canvas**.
- **Potential Outcomes**:
    - Initiates discussions on objectives and hidden costs.
    - May lead to deciding **not to implement AI/ML** if:
        - Solution doesn't tolerate wrong predictions.
        - Low ROI.
        - Maintenance not guaranteed.
- **Deployment Timing**: Consider trade-offs of early vs. late ML deployment (see [[Figure: When to Deploy AI?]]).

---

# MLOps Pipeline Phases

## 1. Scoping

- **Define project goals and success metrics**: Clearly outline the project's objectives and the metrics that will determine success.

## 2. Data

- **Collect and define data**: Gather relevant data and specify its sources and structure.
- **Label and organize data**: Annotate the data as needed and organize it for efficient processing.
- **Establish baseline**: Create a baseline model or performance metric to measure progress against.

## 3. Modeling

- **Select model**: Choose an appropriate machine learning model based on the problem and data.
- **Train model**: Train the selected model using the prepared dataset.
- **Perform error analysis**: Analyze model errors to identify areas for improvement.

## 4. Deployment

- **Deploy in production**: Integrate the trained model into a production environment for real-world use.

## 5. Monitoring & Maintenance

- **Monitor system performance**: Continuously track the model's performance to ensure it meets expectations.
- **Maintain and update system**: Update the model and system as needed to maintain performance and adapt to new data.

![[Pasted image 20250428025131.png]]

---

# Data Version Control (DVC)

DVC, or Data Version Control, is an open-source tool for versioning and managing machine learning projects. It helps track and reproduce datasets, models, and pipelines, similar to how Git manages code. DVC integrates with Git, storing metadata and enabling collaboration.

## DVC Pipeline Stages

**dvc.yaml** file:
- Stage 1: Data Collection
- Stage 2: Data Preparation
- Stage 3: Feature Engineering
- Stage 4: Model Building
- Stage 5: Model Evaluation

### Data Collection

- Fetch the data
- Train Test Split
- make a folder called **data** containing folder called **raw**
- raw contains the **train.csv** , **test.csv**

```yaml
stages:
  data_collection:
    cmd: python src/data_collection.py
    deps:
    - src/data_collection.py
    outs:
    - data/raw
```

**stages**: This is the top-level key in dvc.yaml that defines the pipeline stages.
- **cmd: python src/data_collection.py**: The command DVC will execute for this stage. Here, it runs a Python script (data_collection.py) located in the src/ directory to perform data collection.
- **deps: - src/data_collection.py**: The dependencies for this stage. DVC will track changes to src/data_collection.py. If the script changes, DVC will know to rerun this stage.
- **outs: - data/raw**: The outputs of this stage. The data/raw directory (or file) will be generated by the script, and DVC will version it. This ensures that the output data is tracked and reproducible.

### Data Preparation 

- Fetch the file from the raw folder
- Fill the missing values
- data -> processed folder containing(train_processed.csv, test_processed.csv)

### Model Building

- Fetch file from the processed folder
- train_data.csv
- Choose model
- Save model

## DVC Commands

- `git init`
- `dvc init`
- `dvc repro`
- `dvc metrics show`

## Complete DVC Pipeline Example

```yaml
stages:
  data_ingestion:
    cmd: python src/data_ingestion.py
    deps:
      - src/data_ingestion.py
    outs:
      - data/raw

  data_preprocessing:
    cmd: python src/data_preprocessing.py
    deps:
      - src/data_preprocessing.py
      - data/raw
    outs:
      - data/processed

  feature_engineering:
    cmd: python src/feature_engineering.py
    deps:
      - src/feature_engineering.py
      - data/processed
    outs:
      - data/features

  model_building:
    cmd: python src/model_building.py
    deps:
      - src/model_building.py
      - data/features
    outs:
      - model.pkl

  model_evaluation:
    cmd: python src/model_evaluation.py
    deps:
      - src/model_evaluation.py
      - model.pkl
    metrics:
      - metrics.json
```

---

## Training: Domain-Driven Design for Machine Learning Products

- **Focus**: Apply domain-driven design principles to ML products.
- **Key Idea**: Align ML models with business domains for better integration and value delivery.
- **Study Tip**: Explore how domain experts contribute to features, requirements, and evaluation in the canvases above.

---

**Study Notes**:

- **Review Sequence**: Start with Workflow Decomposition → AI Canvas → Machine Learning Canvas.
- **Key Questions to Ponder**: For each block, ask the listed questions and apply to a sample project (e.g., spam detection).
- **Resources**:
    - Book: _Prediction Machines_ by Agrawal et al.
    - Canvas Examples: Embed figures in Obsidian if available.
- **Next Steps**: Practice filling out a Machine Learning Canvas for a real-world problem.
