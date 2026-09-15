---
description: "Hub: every note about MLflow & DVC"
type: hub
domain: ml
tags:
  - type/hub
  - topic/mlflow-and-dvc
---
# MLflow & DVC

> [!info] Experiment tracking, autolog, model registry, evaluation and DVC data versioning. Command-level coverage only.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/mlflow-and-dvc`.

## Concepts
- [[MLOps Complete Guide]] — A long guide to MLOps: decomposing a business problem with the AI/ML Canvas, then the scoping, data, modelling and deployment phases of the pipeline.

## How-tos & recipes
- [[MLflow Evaluation]] — Shows what mlflow.evaluate generates automatically - classification and regression metrics, ROC and residual plots, custom metrics - and how to evaluate a plain prediction function.
- [[Model Saving]] — Explains model serialization and shows saving and reloading a trained scikit-learn model with pickle and with joblib, plus why joblib is usually preferred.
- [[DVC]] `raw` — Command-by-command DVC setup: init, tracking a data file, adding a remote, pushing and pulling versioned data.
- [[Mlflow Tracking]] `raw` — Step-by-step MLflow tracking code: set the tracking URI, start a run, log params and metrics, log a model with a signature, and switch on autolog.

## References & cheat sheets
- [[MLFlow]] — A reference of MLflow commands: creating and tagging experiments, starting runs, logging and searching, registering models, custom pyfunc models, and the REST API.

## Related hubs
[[MLOps]], [[Git]], [[ML System Design]], [[Evaluation Metrics]]

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
