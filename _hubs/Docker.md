---
description: "Hub: every note about Docker"
type: hub
domain: backend
tags:
  - type/hub
  - topic/docker
---
# Docker

> [!info] Only a copied docker.com tutorial (moved to _inbox). Nothing here is yours - write a real Dockerfile and compose note.
> Part of [[MOC - Backend]]. Also try the tag `#topic/docker`.

## Concepts
- [[MLOps Maturity And Production Practices]] — Community-talk notes on getting models to production: MLOps maturity levels and anti-patterns, Python project structure with pyproject.toml, serving a model as a REST API, and ONNX export.

## How-tos & recipes
- [[AWS Deployment Plan]] — Step-by-step plan to deploy a FastAPI + Nginx docker-compose stack to an AWS EC2 instance, from provisioning to transfer and run.
- [[Enabling SSL,TLS]] — Step-by-step guide to enabling SSL/TLS on a Dockerised PostgreSQL, including generating certs and proving the traffic is encrypted.
- [[FastAPI - MongoDB]] — How to wire FastAPI to MongoDB with the async Motor driver: Docker container setup, ObjectId handling in Pydantic, models and CRUD endpoints.
- [[FastAPI AI Deployment (Docker + Azure)]] — Guide to shipping a heavy-dependency FastAPI service to Azure App Service via Docker Hub, with GitHub Actions automation.
- [[Grafana]] `stub` — The docker-compose service block for running Grafana next to Prometheus.
- [[Prometheus]] `stub` — The prometheus.yml scrape config for a FastAPI app and node-exporter.
- [[Sharding]] `raw` — Pasted SQL and Docker commands for spinning up two PostgreSQL shards behind a hash-based URL table.

## Course notes
- [[FastAPI - Request Files, MLOps, and API Metadata]] — FastAPI course notes on file uploads, Dockerizing the app, Prometheus metrics and Evidently drift monitoring, plus error handling and OpenAPI metadata.

## Interviews
- [[Docker & K8s]] — The short interview version of containers and orchestration: what a container really is, the three Docker terms and three Kubernetes terms to name, and the two reasons a telecom runs K8s.

## Clippings (raw)
- [[Docker]] `raw` — Verbatim copy of the docker.com getting-started tutorial covering docker run, what a container is, and container networking.

## Related hubs
[[FastAPI]], [[Observability]], [[MLOps]], [[Postgres]], [[Cloud Deployment]], [[MongoDB]]

## Notes to self (from the audit)
- [[Sharding]]: Code-only - no explanation of the shard key choice or routing logic.
- [[Docker]]: Copied tutorial, not your own notes. Docker is otherwise uncovered - worth writing a real note.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
