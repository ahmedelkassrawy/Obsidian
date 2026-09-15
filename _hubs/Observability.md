---
description: "Hub: every note about Observability"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/observability
---
# Observability

> [!info] Golden signals, three pillars, and MySQL profiling. Missing: an OpenTelemetry or Prometheus setup you actually ran.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/observability`.

## Concepts
- [[LLMOps Observability And Production Stack]] — Notes on LLMOps in production: which LLM metrics to monitor, the observability layers, LLM routing, feedback loops, versioning strategy, and cost and privacy controls.

## How-tos & recipes
- [[Google ADK Observability And Eval]] `raw` — Short pasted snippet showing how to attach ADK's LoggingPlugin to an InMemoryRunner for agent observability.
- [[Grafana]] `stub` — The docker-compose service block for running Grafana next to Prometheus.
- [[LangSmith]] `stub` — The .env variables that turn LangSmith tracing on and the two lines of Python that load them.
- [[Langgraphics Graph Visualizer]] `stub` — A single snippet showing how to wrap a compiled LangGraph with langgraphics' watch() to visualize a run.
- [[Prometheus]] `stub` — The prometheus.yml scrape config for a FastAPI app and node-exporter.
- [[Python Logger Setup]] `raw` — Line-by-line walkthrough of a Python logging setup: a private _setup_logging method, named loggers, level from settings, file and console handlers, and a formatter.

## Book notes
- [[Designing ML Systems Ch8 - Data Shifts And Monitoring]] — Chapter 8 notes on production failures: software vs ML-specific failures, degenerate feedback loops, detecting and fixing data distribution shift, and monitoring vs observability.
- [[High Performance MySQL - Benchmarking]] — Book chapter on benchmarking MySQL: why synthetic workloads mislead, benchmarking strategies and tactics, and the tools to use.
- [[Profiling Server Performance]] — Book chapter on profiling MySQL server performance: where response time goes, profiling types, instrumentation and the tools.

## Course notes
- [[FastAPI - Request Files, MLOps, and API Metadata]] — FastAPI course notes on file uploads, Dockerizing the app, Prometheus metrics and Evidently drift monitoring, plus error handling and OpenAPI metadata.
- [[LLM Proxies]] — Course notes on running a LiteLLM proxy in front of several model providers: config file, starting the server, calling it with the OpenAI client, logging and load balancing.
- [[Observability - Signals, Pillars and Correlation]] — Introduces observability through a fitness analogy: the four golden signals, the three pillars (metrics, logs, traces), correlation and a worked dice-game dashboard.

## Clippings (raw)
- [[Clipping - Observability From Scratch Part 1 (Podcast, Arabic)]] `raw` — Raw Arabic podcast transcript (Tech Podcast, part 1) introducing observability from scratch - logs, metrics and traces and why monitoring alone is not enough.

## Related hubs
[[Docker]], [[MLOps]], [[AI Evaluation]], [[LangGraph]], [[LLM Serving & vLLM]], [[System Design]]

## Notes to self (from the audit)
- [[Google ADK Observability And Eval]]: Barely started - add the eval half that the title promises.
- [[LangSmith]]: Contains a real LANGSMITH_API_KEY in plain text - revoke and rotate that key now.
- [[Clipping - Observability From Scratch Part 1 (Podcast, Arabic)]]: Digest into Backend/Observability. Part 2 is not in the vault - grab it while you are there.
- [[LLMOps Observability And Production Stack]]: Opens with a LinkedIn link and a personal roadmap TODO - move that to a task note.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
