---
description: "Hub: every note about AI Evaluation"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/ai-evaluation
---
# AI Evaluation

> [!info] Why single-run eval is worthless and what a harness must collect. The weakest hub relative to its importance - the book chapter on evaluating AI systems is an empty file.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/ai-evaluation`.

## Concepts
- [[Agent Evaluation]] — Argues that one-run accuracy or LLM-as-judge is not agent evaluation, and lists what a production eval harness must collect across repeated non-deterministic runs.
- [[DSPy Optimization]] — The DSPy optimization workflow: how to build and split datasets, what an optimizer actually tunes, and a step-by-step walk through MIPROv2's bootstrapping and proposal stages.
- [[RAG Production]] — The production trade-offs in RAG: retrieval and generation metrics, why exact kNN does not scale and how ANN/HNSW replaces it, and chunking choices.
- [[System Design for AI Agents (Architecture and the Why)]] — Trains you to defend every agent design decision: start from constraints, place the system on the agency spectrum, split into single-responsibility agents, and route for cost vs quality.
- [[Uber Eats — Designing Agents and Eval Loops (Production Case Study)]] — Production case study of Uber Eats' photo-enhancement agent system, focused on how each stage is wrapped in its own eval loop and how routing controls agency.

## How-tos & recipes
- [[DSPy Evaluation]] `raw` — Pasted DSPy code for building Examples with input keys, setting up a reusable evaluator, and launching an evaluation run.
- [[Google ADK Observability And Eval]] `raw` — Short pasted snippet showing how to attach ADK's LoggingPlugin to an InMemoryRunner for agent observability.
- [[LangSmith]] `stub` — The .env variables that turn LangSmith tracing on and the two lines of Python that load them.

## Book notes
- [[Ch3. Eval]] — Chip Huyen Ch3: why evaluation is its own hard problem, the entropy/perplexity metrics, exact vs subjective evaluation, embedding similarity, and AI-as-a-judge.
- [[Ch4. Evaluating AI Systems]] `empty` — Empty placeholder for the AI Engineering chapter on evaluating whole AI systems.

## Related hubs
[[Agents]], [[System Design]], [[DSPy]], [[Observability]], [[Embeddings & Semantic Search]], [[Prompting]]

## Notes to self (from the audit)
- [[Ch4. Evaluating AI Systems]]: Zero words and the old filename misspelled 'Evaluation' - fill from the book or delete.
- [[Google ADK Observability And Eval]]: Barely started - add the eval half that the title promises.
- [[LangSmith]]: Contains a real LANGSMITH_API_KEY in plain text - revoke and rotate that key now.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
