---
description: "Hub: every note about Testing"
type: hub
domain: backend
tags:
  - type/hub
  - topic/testing
---
# Testing

> [!info] Almost empty - only a manual curl run and the SQLAlchemy review checklist. This is the single biggest hole in the backend domain.
> Part of [[MOC - Backend]]. Also try the tag `#topic/testing`.

## Concepts
- [[MLOps Maturity And Production Practices]] — Community-talk notes on getting models to production: MLOps maturity levels and anti-patterns, Python project structure with pyproject.toml, serving a model as a REST API, and ONNX export.

## How-tos & recipes
- [[05 - Running and Testing the App]] — Runs the app with uvicorn and walks a full manual curl test of every endpoint, including the expected 404.
- [[Testing with pytest]] — pytest aimed at validation: the habit of testing that bad input is rejected with pytest.raises, not just that good input constructs, and isolating one variable per test.

## References & cheat sheets
- [[14 - Best Practices Checklist]] — A tick-box review checklist for any file that touches SQLAlchemy, each item linking to the note that explains it.

## Book notes
- [[High Performance MySQL - Benchmarking]] — Book chapter on benchmarking MySQL: why synthetic workloads mislead, benchmarking strategies and tactics, and the tools to use.

## Interviews
- [[CI & CD]] — CI, CD and the MLOps-specific "CT" (continuous training) explained for an interview answer, including why ML pipelines test data and models and not just code.

## Related hubs
[[MLOps]], [[FastAPI]], [[SQLAlchemy]], [[MySQL]], [[Observability]], [[Interviews]]

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
