---
description: "Hub: every note about ML System Design"
type: hub
domain: ml
tags:
  - type/hub
  - topic/ml-system-design
---
# ML System Design

> [!info] Designing ML Systems chapters 1-4 and 8 plus an Instagram feed-ranking interview. Missing chapters 5-7 (feature engineering, model development, deployment).
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/ml-system-design`.

## Concepts
- [[MLOps Complete Guide]] — A long guide to MLOps: decomposing a business problem with the AI/ML Canvas, then the scoping, data, modelling and deployment phases of the pipeline.
- [[Mastering the 3-Stage Recommendation Pipeline]] — Explains the industry-standard three-stage recommender pipeline - candidate generation, ranking, post-processing - and why serving at scale needs it.
- [[Three Levels Of ML Software]] — Study guide on the three assets of ML software (data, model, code): data and ML pipeline stages, the four ML architectural patterns, and model serialization formats.

## References & cheat sheets
- [[ML Project Checklist]] — The eight-step checklist for running an ML project end to end, from framing the problem through data prep, model shortlisting, fine-tuning and presenting the solution.

## Book notes
- [[Designing ML Systems Ch1 - When To Use ML]] — Chapter 1 notes from Designing Machine Learning Systems: what MLOps means and the five conditions (learn, complex patterns, existing data, prediction, unseen data) that make a problem worth solving with ML.
- [[Designing ML Systems Ch2 - ML System Requirements]] — Chapter 2 notes: which problems suit ML, how to map ML metrics to business metrics, and the four requirements of an ML system (reliable, scalable, maintainable, adaptable).
- [[Designing ML Systems Ch3 - Data Engineering]] — Chapter 3 notes on data engineering for ML: data sources, formats and serialization, row vs column storage, OLTP vs OLAP, and the ETL pipeline.
- [[Designing ML Systems Ch4 - Training Data]] — Chapter 4 notes on training data: probability vs nonprobability sampling, labeling strategies and weak supervision, handling missing labels, and dealing with class imbalance.
- [[Designing ML Systems Ch8 - Data Shifts And Monitoring]] — Chapter 8 notes on production failures: software vs ML-specific failures, degenerate feedback loops, detecting and fixing data distribution shift, and monitoring vs observability.
- [[Designing ML Systems.1]] — Duplicate copy of the Designing ML Systems chapter 1 notes on MLOps and when ML is the right tool.

## Project notes
- [[Project Agent Arch]] — Architecture writeup for DataPilot AI, a LangGraph Text-to-SQL agent: the graph nodes from router through schema intelligence, memory, SQL generation, approval gate and retry loop.

## Interviews
- [[5G ML Use Cases for Telecom]] — The four ML use cases to talk about in a telecom interview: 5G network slicing, predictive maintenance on hardware, traffic prediction and load balancing, and churn plus fraud detection.
- [[Designing Instagram's Feed Ranking Model]] — A mock Meta ML system design interview: framing Instagram feed ranking, the 3-stage retrieval/ranking/re-rank pipeline, features, offline vs online metrics, and the model architecture.

## Related hubs
[[MLOps]], [[Feature Engineering & Pipelines]], [[Data Cleaning]], [[Recommender Systems]], [[Interviews]], [[Observability]]

## Notes to self (from the audit)
- [[Designing ML Systems Ch1 - When To Use ML]]: Byte-identical to 'Designing ML Systems.1.md' in the same folder - that copy is being inboxed.
- [[Designing ML Systems.1]]: Byte-identical duplicate of 'Design ML System.1.md' - kept there, this copy inboxed.
- [[Project Agent Arch]]: Content is GenAI agent engineering - likely belongs in the ai-eng domain rather than ml.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
