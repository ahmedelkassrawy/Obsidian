# Three Levels of ML Software: A Study Guide

## Introduction to ML Software and MLOps

**ML/AI** is rapidly adopted across applications and industries. The goal of an ML project is to build a **statistical model** using collected data and ML algorithms. Building successful ML-based software is challenging due to managing three assets:

- **Data**: Quality and quantity are critical for model performance.
- **Model**: The core ML algorithm and trained artifact.
- **Code**: Software infrastructure for deployment and integration.

**MLOps** (Machine Learning Operations), an extension of DevOps, establishes practices for designing, building, and deploying ML models into production.

- **Recommendation**: Document every step of the ML pipeline for traceability and reproducibility.

## Data: Data Engineering Pipelines

**Data** is the foundation of any ML workflow. The phrase **“Garbage In, Garbage Out”** emphasizes that model quality depends on data quality. Data engineering is time-consuming, often taking the majority of project effort.

### Data Engineering Pipeline Stages

The pipeline creates **training** and **testing datasets** through the following stages:

#### 1. Data Ingestion

- **Definition**: Collecting data from various systems/frameworks/formats (e.g., databases, data marts, OLAP cubes, data warehouses, OLTP systems, Spark, HDFS).
- **Additional Methods**: Synthetic data generation, data enrichment.
- **Best Practices** (Maximize automation):
    - **Data Sources Identification**: Document data origin (**data provenance**).
    - **Space Estimation**: Assess storage needs.
    - **Space Location**: Create a workspace with sufficient storage.
    - **Obtaining Data**: Convert data to a manipulable format without altering it.
    - **Back up Data**: Work on copies, keep originals untouched.
    - **Privacy Compliance**: Ensure GDPR compliance (e.g., anonymize sensitive data).
    - **Metadata Catalog**: Document metadata (size, format, aliases, last modified, access control).
    - **Test Data**: Reserve a test set to avoid **data snooping bias** (selecting models based on test set performance).

#### 2. Exploration and Validation

- **Definition**: Data profiling to understand content/structure and validation to assess quality.
- **Output**: Metadata (e.g., max, min, avg) and error detection via user-defined functions.
- **Examples**:
    - Validate address consistency (e.g., correct postal codes, missing values).
- **Best Practices**:
    - **Use RAD Tools**: Jupyter notebooks for exploration/experimentation records.
    - **Attribute Profiling**: Document metadata for each attribute:
        - Name, number of records, data type (categorical, numerical, text, etc.).
        - Numerical measures (min, max, avg, median).
        - Missing value ratio (absent values ÷ total records).
        - Distribution type (Gaussian, uniform, logarithmic).
    - **Label Attribute Identification**: Identify target attribute(s) for supervised learning.
    - **Data Visualization**: Create visual representations of value distributions.
    - **Attributes Correlation**: Analyze correlations between attributes.
    - **Additional Data**: Identify useful data for model building (return to [[Data Ingestion]]).

#### 3. Data Wrangling (Cleaning)

- **Definition**: Programmatic data preparation (re-formatting, restructuring) to adjust schema.
- **Recommendation**: Write reusable scripts/functions for transformations.
- **Operations**:
    - **Transformations**: Identify promising transformations.
    - **Outliers**: Fix or remove (optional).
    - **Missing Values**: Fill (e.g., zero, mean, median) or drop rows/columns.
    - **Not Relevant Data**: Drop uninformative attributes (relevant for feature engineering).
    - **Restructure Data** (from _Principles of Data Wrangling_):
        - Reorder record fields (move columns).
        - Create new fields by extracting values.
        - Combine multiple fields into one.
        - Filter datasets by removing records.
        - Shift granularity via aggregations/pivots.

#### 4. Data Splitting

- **Definition**: Split data into **training (80%)**, **validation**, and **test** datasets for ML stages.

## Model: Machine Learning Pipelines

The core of ML workflows involves writing and executing algorithms to produce an **ML model**. The **model engineering pipeline** includes:

### Model Engineering Stages

#### 1. Model Training

- **Definition**: Apply ML algorithms on training data, including **feature engineering** and **hyperparameter tuning**.
- **Feature Engineering** (from _Hands-On Machine Learning_ by Aurélien Géron):
    - Discretize continuous features.
    - Decompose features (e.g., categorical, date/time).
    - Add transformations (e.g., log(x), sqrt(x), x²).
    - Aggregate features into new features.
    - Feature scaling (standardize/normalize).
    - Add new features quickly for production.
- **Further Reading**: _Feature Engineering for Machine Learning_ by Alice Zheng, Amanda Casari.
- **Workflow** (Iterative):
    - Version and review model specification code.
    - Train multiple models (e.g., linear regression, logistic regression, k-means, naive Bayes, SVM, Random Forest) with standard parameters.
    - Compare performance using **N-fold cross-validation** (mean/std of performance).
    - **Error Analysis**: Analyze error types.
    - Refine feature selection/engineering.
    - Identify top 3–5 models, preferring diverse error types.
    - Tune hyperparameters using **random search** (preferred over grid search).
    - Use **ensemble methods** (majority vote, bagging, boosting, stacking) for better performance.
    - **Further Reading**: _Ensemble Methods: Foundations and Algorithms_ by Zhi-Hua Zhou.

#### 2. Model Evaluation

- **Definition**: Validate the model against **business objectives** before production deployment.

#### 3. Model Testing

- **Definition**: Measure performance on the **hold-back test dataset** to estimate **generalization error** via a **Model Acceptance Test**.

#### 4. Model Packaging

- **Definition**: Export the model to a format (e.g., PMML, PFA, ONNX) for consumption by business applications.
- **Details**: See [[ML Model Serialization Formats]].

## ML Workflows and Architectural Patterns

ML workflows vary by **training** and **prediction** methods, classified along two dimensions:

1. **ML Model Training**:
    - **Offline Learning (Batch/Static)**: Train on collected data; model remains constant until retrained due to **model decay**.
    - **Online Learning (Dynamic)**: Regularly retrain as new data arrives (e.g., time-series, streaming data).
2. **ML Model Prediction**:
    - **Batch Predictions**: Predict on historical data (non-time-critical).
    - **Real-time Predictions (On-demand)**: Predict using current data at request time.

### Four ML Architectural Patterns

(See [[Figure: ML Workflows]] for illustration.)

#### 1. Forecast

- **Description**: Common in academic research/data science education (e.g., Kaggle). Train on a dataset, run on historical data to produce forecasts.
- **Use Case**: Experimental, not common in production (e.g., mobile apps).

#### 2. Web-Service

- **Description**: Deploy ML model as a **web service** (microservice) via REST API or gRPC, trained offline but using real-time data for predictions.
- **Difference from Forecast**: Processes single records near real-time.
- **Architecture**: See [[Figure: Web Service Pattern]].

#### 3. Online Learning

- **Description**: Continuously retrain on streaming data (single points or mini-batches), often called **incremental learning**. Runs as a service (e.g., on Kubernetes) with **lambda architecture**.
- **Challenges**: Bad data can degrade performance.
- **Architecture**: See [[Figure: Online Learning ML System]].

#### 4. AutoML

- **Description**: Automated ML model selection and configuration with minimal expertise. Executes full training pipelines in production.
- **Providers**: Google, MS Azure.
- **Status**: Experimental, requires high accuracy for real-world use.
- **Further Reading**:
    - AutoML: Overview and Tools.
    - AutoML Benchmark.

## ML Model Serialization Formats

To distribute ML models, they must be **executable** and **independent**. Formats are **language-agnostic** or **vendor-specific**.

### Language-Agnostic Formats

- **Amalgamation**: Bundle model and code into one file (e.g., via SKompiler). Supports SQL, Excel, PFA, or multi-language code (C, JavaScript, Rust, Julia).
    - **Pros**: Portable, compact for simple models (e.g., logistic regression).
    - **Cons**: Model code/parameters managed together.
- **PMML**: XML-based (.pmml), standardized by Data Mining Group (DMG).
    - **Limitations**: Limited algorithm support, licensing issues.
- **PFA (Portable Format for Analytics)**: JSON-based, replaces PMML. Supports control structures, extensible functions.
    - **Requirement**: PFA-enabled runtime.
- **ONNX (Open Neural Network Exchange)**: Framework-independent, supported by Microsoft, Facebook, Amazon.
    - **Use**: Consumed by ONNX-enabled runtime libraries.

### Vendor-Specific Formats

- **Scikit-Learn**: Pickled Python objects (.pkl).
- **H2O**: POJO or MOJO (.jar).
- **SparkML**: MLeap format (.jar/.zip), supports Spark, Scikit-learn, TensorFlow.
- **TensorFlow**: Protocol buffer files (.pb).
- **PyTorch**: Torch Script (.pt), served from C++.
- **Keras**: Hierarchical Data Format (.h5).
- **Apple Core ML**: .mlmodel for iOS, supports TensorFlow, Scikit-learn via converters.

### Serialization Formats Table

|Format|Open|Vendor|Extension|License|Supported Tools/Platforms|Human-Readable|Compression|
|---|---|---|---|---|---|---|---|
|Amalgamation|−|−|−|−|−|✓|−|
|PMML|✓|DMG|.pmml|AGPL|R, Python, Spark|✓ (XML)|✘|
|PFA|✓|DMG|JSON|−|PFA-enabled runtime|✓ (JSON)|✘|
|ONNX|✓|SIG, LFAI|.onnx|−|TF, CNTK, Core ML, MXNet, ML.NET|−|✓|
|TF Serving Format|✓|Google|.pf|−|TensorFlow|✘|g-zip|
|Pickle Format|✓|−|.pkl|−|Scikit-learn|✘|g-zip|
|JAR/POJO|✓|−|.jar|−|H2O|✘|✓|
|HDF|✓|−|.h5|−|Keras|✘|✓|
|MLeap|✓|−|.jar/.zip|−|Spark, TF, Scikit-learn|✘|g-zip|
|Torch Script|✘|−|.pt|−|PyTorch|✘|✓|
|Apple .mlmodel|✘|Apple|.mlmodel|−|TF, Scikit-learn, Core ML|−|✓|

- **Further Reading**:
    - ML Models Training File Formats.
    - Open Standard Models.

## Code: Deployment Pipelines

The final stage involves deploying and monitoring the ML model.

### Deployment Pipeline Stages

1. **Model Serving**: Deploy the model in production.
2. **Model Performance Monitoring**: Observe performance on live/unseen data, tracking **prediction deviation** as a retraining trigger.
3. **Model Performance Logging**: Log every inference request.

### Model Serving Patterns

Five patterns for integrating ML models into production (applicable to serialization formats):

#### 1. Model-as-Service

- **Description**: Wrap model and interpreter as a web service (REST API/gRPC).
- **Use Cases**: Forecast, Web Service, Online Learning.
- **Architecture**: See [[Figure: Model as Service Pattern]].

#### 2. Model-as-Dependency

- **Description**: Package model as a dependency (e.g., JAR) invoked by the application.
- **Use Case**: Forecast pattern.
- **Architecture**: See [[Figure: Model as Dependency]].

#### 3. Precompute Serving

- **Description**: Precompute predictions on batch data, store in a database, query for results.
- **Use Case**: Forecast workflow.
- **Architecture**: See [[Figure: Precompute Serving Pattern]].

#### 4. Model-on-Demand

- **Description**: Model as a runtime dependency with a separate release cycle, using a **message-broker architecture** (input/output queues).
- **Process**:
    - Prediction requests written to input queue.
    - Event processor (with model) reads requests, generates predictions, writes to output queue.
- **Architecture**: See [[Figure: Model on Demand]].
- **Further Reading**:
    - Event-driven architecture.
    - Web services vs. streaming for real-time ML endpoints.

#### 5. Hybrid-Serving (Federated Learning)

- **Description**: Combines server-side and user-side models.
    - **Server Model**: Trained once, general-purpose, sets initial model for users.
    - **User Models**: Trained on devices for personalization, updated periodically with server model.
    - **Process**: Devices train models locally, send model data (not personal data) to server for updates. Updates occur when devices are idle, on WiFi, and charging.
- **Benefits**:
    - Personal data stays on devices.
    - Highly accurate, personalized models.
- **Challenges**:
    - Mobile devices have limited power.
    - Distributed, intermittent data.
- **Tool**: **TensorFlow Federated (TFF)** for lightweight federated learning.
- **Architecture**: See [[Figure: Federated Learning]].

### Deployment Strategies

Two common strategies for deploying ML models:

#### 1. Deploying as Docker Containers

- **Description**: Package ML tech stack and inference code into a **Docker container**, orchestrated by Kubernetes or AWS Fargate, accessed via REST API (e.g., Flask).
- **Status**: De-facto standard for on-premise, cloud, or hybrid deployments.
- **Architecture**: See [[Figure: Docker Infrastructure for Model Deployment]].

#### 2. Deploying as Serverless Functions

- **Description**: Package application code and dependencies into .zip files with a single entry point, managed by cloud providers (e.g., AWS Lambda, Azure Functions, Google Cloud Functions).
- **Platforms**: AWS SageMaker, Google Cloud AI Platform, Azure Machine Learning Studio, IBM Watson.
- **Constraints**: Artifact size limitations.
- **Architecture**: See [[Figure: Serverless Infrastructure for Model Deployment]].

## Study Notes

- **Review Sequence**: Study [[Data Engineering Pipelines]] → [[Machine Learning Pipelines]] → [[ML Workflows and Architectural Patterns]] → [[Deployment Pipelines]].
- **Key Questions**:
    - How does data quality affect model performance?
    - Compare offline vs. online learning for your use case.
    - Evaluate trade-offs of serving patterns (e.g., Model-as-Service vs. Precompute).
- **Practice**:
    - Simulate a data pipeline for a sample dataset (e.g., customer churn).
    - Choose a serving pattern and sketch its architecture.
- **Resources**:
    - Books: _Hands-On Machine Learning_ (Géron), _Feature Engineering for Machine Learning_ (Zheng, Casari), _Ensemble Methods_ (Zhou).
    - Figures: Embed [[Figure: ML Workflows]], [[Figure: Web Service Pattern]], etc., in Obsidian.
- **Next Steps**: Apply the Machine Learning Canvas (from prior content) to a deployment scenario.