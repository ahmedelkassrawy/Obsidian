

> [!info]
> A visual map of all the interview prep topics in this folder. Use this as your one-page reference before the interview.

## The Full MLOps Lifecycle

The 5 phases that make up the complete answer to "walk me through MLOps":

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  1. Data    │──▶│  2. Model   │──▶│  3. Model   │──▶│  4. Model   │──▶│  5. Model   │
│  Extraction │   │  Training   │   │  Evaluation │   │  Deployment │   │  Monitoring │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
     │                │                   │                 │                    │
  CDR, billing,    MLflow tracks      Holdout test      Docker → K8s        Watch for drift,
  network data     experiments:       Precision/Recall  or SageMaker        trigger CT if
  automated &      hyperparams,       halts if worse    Endpoint as REST    below threshold
  reproducible     datasets, acc      than prod         API
```

---

## CI / CD / CT Pipeline

| Pipeline "C" | What It Does | Why Orange Cares |
|---|---|---|
| **CI - Continuous Integration** | Auto-test code, data, and model on every commit. Catches bugs before they reach prod. | A fraud detection bug costs money every minute. CI catches it in 15 min, not 2 days. |
| **CD - Continuous Deployment** | Auto-package into Docker, push to K8s/SageMaker, swap old pods for new ones. | Zero human error, zero manual IT work. Deploy in minutes. |
| **CT - Continuous Training** | Triggered by drift detection. Pulls fresh data, retrains, evaluates, deploys if better. | Model accuracy degrades over time. CT keeps it fresh automatically. |

> [!tip] Interview Quote
> _"CI/CD is the wall that stops bad code from taking down Orange's network. Try deploying buggy code and the CI server protects production before anyone is impacted."_

---

## Infrastructure: Two Stacks, Same Concepts

| Open Source | AWS SageMaker Equivalent | What It Does |
|:-:|:-:|---|
| `Docker` + `K8s` | **SageMaker Endpoints** | Auto-scaled, managed container deployment |
| `MLflow` | **SageMaker Experiments & Registry** | Track experiments, log accuracy, store models |
| `Evidently` | **SageMaker Model Monitor** | Detect Data Drift & Concept Drift |
| `Airflow/Jenkins` | **SageMaker Pipelines** | Automate the full CI/CD/CT loop |
| Jupyter Notebooks | **SageMaker Studio** | Cloud IDE with GPU on demand |

> [!note] Why SageMaker for Telecom
> Strict security and data privacy laws require that data stays inside the AWS ecosystem. SageMaker endpoints are optimized for millions of requests/second with low latency — perfect for 5G slicing and churn prediction.

---

## Drift: The Two Types

| | **Data Drift** | **Concept Drift** |
|---|---|---|
| **What changed?** | Input distribution shifted | The relationship $P(y|X)$ changed |
| **Still valid logic?** | Model logic is fine, just没见过 high numbers | The rules of the game changed |
| **Example** | 5G campaign → avg usage jumps 10GB to 50GB | Hackers invent new scam patterns |
| **Detection** | K-S test, PSI, hypothesis testing | Accuracy drops, K-S test on outputs |

> [!example] Scenario — Fraud Detection accuracy drops 94% → 81% in 48 hours
> This is **Concept Drift** because the fundamental definition of "scam" changed. The model learned old scam rules; hackers have a new rulebook.
>
> **Response:** Don't manually intervene. Rely on CT pipeline — ingest last 48 hours of data (contains new phishing patterns), retrain, validate, deploy.

---

## Telecom Use Cases (5G ML)

| Use Case | ML Technique | MLOps Consideration |
|---|---|---|
| **5G Network Slicing** | Dynamic bandwidth/latency allocation | Real-time predictions, multi-model coordination |
| **Predictive Maintenance** | Anomaly detection on IoT sensor data | False positives cost real money (dispatching techs) |
| **Traffic Prediction & Load Balancing** | Time-series (LSTM, XGBoost) | Peak loads need auto-scaling (K8s pods) |
| **Customer Churn & Fraud** | Classification on billing/support logs | High ROI, accuracy must be monitored for drift |

---

## The "Golden Terms" Quick Reference

### Docker
- **Dockerfile** = The Recipe (text file with build instructions)
- **Image** = The Blueprint (frozen snapshot from `docker build`)
- **Container** = The Live App (running process from `docker run`)

### Kubernetes
- **Pod** = Smallest unit, wraps 1 container
- **Node** = Physical/virtual machine (AWS EC2)
- **Cluster** = Fleet of nodes managed by Control Plane
- **Auto-Scaling** = Spins up/down pods based on traffic
- **Self-Healing** = Restarts dead pods on healthy nodes

### Master Interview Quote
> _"MLOps is about treating ML models like robust software. I'd track experiments with **MLflow**, run **CI/CD** to test and deploy via **Docker** to **Kubernetes** or **SageMaker**, then monitor for drift. When accuracy drops, **Continuous Training** retrains on fresh data automatically."_

---

## Tool Chain Map by Source File

| File | Key Concepts | Interview Relevance |
|---|---|---|
| `5G ML` | Network Slicing, Predictive Maintenance, Load Balancing, Churn/Fraud | **High** — Orange use cases, shows business context |
| `AWS SageMaker` | Endpoints, Experiments, Monitor, Pipelines, Studio | **Medium** — "do you know the managed alternative?" |
| `CI & CD` | CI (test), CD (deploy), CT (retrain), 15min vs 2 days | **High** — the engineering rigor question |
| `Docker & K8s` | Dockerfile/Image/Container, Pod/Node/Cluster, Auto-scale | **High** — "how do you put models in production?" |
| `Drifts` | Data Drift vs Concept Drift, hypothesis testing, CT pipeline | **High** — "how do models degrade?" |
| `MLOPS Lifecycle` | Extraction → Training → Evaluation → Deployment → Monitoring | **Highest** — the master framework question |
