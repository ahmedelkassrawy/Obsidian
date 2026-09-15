---
description: "Hub: every note about MLOps"
type: hub
domain: ml
tags:
  - type/hub
  - topic/mlops
---
# MLOps

> [!info] Maturity levels, CI/CD, serving a model as an API, ONNX, monitoring and LLMOps. Read, not practised.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/mlops`.

## Concepts
- [[LLMOps Observability And Production Stack]] — Notes on LLMOps in production: which LLM metrics to monitor, the observability layers, LLM routing, feedback loops, versioning strategy, and cost and privacy controls.
- [[MLOps Complete Guide]] — A long guide to MLOps: decomposing a business problem with the AI/ML Canvas, then the scoping, data, modelling and deployment phases of the pipeline.
- [[MLOps Maturity And Production Practices]] — Community-talk notes on getting models to production: MLOps maturity levels and anti-patterns, Python project structure with pyproject.toml, serving a model as a REST API, and ONNX export.
- [[Three Levels Of ML Software]] — Study guide on the three assets of ML software (data, model, code): data and ML pipeline stages, the four ML architectural patterns, and model serialization formats.

## How-tos & recipes
- [[MLflow Evaluation]] — Shows what mlflow.evaluate generates automatically - classification and regression metrics, ROC and residual plots, custom metrics - and how to evaluate a plain prediction function.
- [[Model Saving]] — Explains model serialization and shows saving and reloading a trained scikit-learn model with pickle and with joblib, plus why joblib is usually preferred.
- [[Running Kubernetes Locally]] — How to run Kubernetes locally, the deployment.yaml/service.yaml MLOps blueprint, and the kubectl workflow commands.
- [[DVC]] `raw` — Command-by-command DVC setup: init, tracking a data file, adding a remote, pushing and pulling versioned data.
- [[Mlflow Tracking]] `raw` — Step-by-step MLflow tracking code: set the tracking URI, start a run, log params and metrics, log a model with a signature, and switch on autolog.

## References & cheat sheets
- [[ML Project Checklist]] — The eight-step checklist for running an ML project end to end, from framing the problem through data prep, model shortlisting, fine-tuning and presenting the solution.
- [[MLFlow]] — A reference of MLflow commands: creating and tagging experiments, starting runs, logging and searching, registering models, custom pyfunc models, and the REST API.

## Book notes
- [[Designing ML Systems Ch1 - When To Use ML]] — Chapter 1 notes from Designing Machine Learning Systems: what MLOps means and the five conditions (learn, complex patterns, existing data, prediction, unseen data) that make a problem worth solving with ML.
- [[Designing ML Systems Ch8 - Data Shifts And Monitoring]] — Chapter 8 notes on production failures: software vs ML-specific failures, degenerate feedback loops, detecting and fixing data distribution shift, and monitoring vs observability.
- [[Designing ML Systems.1]] — Duplicate copy of the Designing ML Systems chapter 1 notes on MLOps and when ML is the right tool.
- [[Practical MLOps Ch1 - DevOps Foundations]] — Practical MLOps chapter 1 definitions: continuous integration, continuous delivery, microservices, infrastructure as code, and monitoring and instrumentation.

## Course notes
- [[FastAPI - Request Files, MLOps, and API Metadata]] — FastAPI course notes on file uploads, Dockerizing the app, Prometheus metrics and Evidently drift monitoring, plus error handling and OpenAPI metadata.

## Interviews
- [[AWS SageMaker]] — What SageMaker is as a managed end-to-end ML platform, mapped tool by tool against the open-source stack, and why telecom shops pick it over running their own Kubernetes.
- [[CI & CD]] — CI, CD and the MLOps-specific "CT" (continuous training) explained for an interview answer, including why ML pipelines test data and models and not just code.
- [[Data Drift and Concept Drift]] — The difference between data drift (inputs shift) and concept drift (the input-to-output relationship shifts), how each is detected, and why continuous training is the fix.
- [[MLOps Lifecycle]] — The five phases of the MLOps lifecycle - data extraction, training, evaluation, deployment, monitoring - as the scripted answer to "walk me through MLOps".
- [[Orange MLOps Interview Visualization]] — A one-page ASCII map tying together every other note in the Orange folder: the lifecycle, the CI/CD/CT pipeline, both infrastructure stacks, the two drift types, and the golden terms.

## Clippings (raw)
- [[AI Engineering Specific Use Cases]] `raw` — Verbatim copy of section 8 of the h9-tec/AI_deployment README on serving ML models and validating data pipelines with FastAPI.

## Related hubs
[[ML System Design]], [[MLflow & DVC]], [[Interviews]], [[Cloud Deployment]], [[Observability]], [[FastAPI]]

## Notes to self (from the audit)
- [[AI Engineering Specific Use Cases]]: Copied README section - not rewritten.
- [[Orange MLOps Interview Visualization]]: This is the index for the Orange folder - link the other six notes from it so it works as a local MOC.
- [[Designing ML Systems Ch1 - When To Use ML]]: Byte-identical to 'Designing ML Systems.1.md' in the same folder - that copy is being inboxed.
- [[Designing ML Systems.1]]: Byte-identical duplicate of 'Design ML System.1.md' - kept there, this copy inboxed.
- [[LLMOps Observability And Production Stack]]: Opens with a LinkedIn link and a personal roadmap TODO - move that to a task note.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
