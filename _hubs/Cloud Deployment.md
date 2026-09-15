---
description: "Hub: every note about Cloud Deployment"
type: hub
domain: backend
tags:
  - type/hub
  - topic/cloud-deployment
---
# Cloud Deployment

> [!info] EC2 + compose, Azure App Service twice, Hugging Face Spaces. Missing: CI/CD beyond a sketch, and secrets management.
> Part of [[MOC - Backend]]. Also try the tag `#topic/cloud-deployment`.

## Concepts
- [[Kubernetes Core Concepts]] — Kubernetes core concepts for an AI engineer: containers, pods, deployments, services, jobs/cronjobs and Helm.
- [[Nginx]] — What NGINX actually does - web server, reverse proxy, load balancer, cache - and why you would pick it over other servers.
- [[Three Levels Of ML Software]] — Study guide on the three assets of ML software (data, model, code): data and ML pipeline stages, the four ML architectural patterns, and model serialization formats.

## How-tos & recipes
- [[AWS Deployment Plan]] — Step-by-step plan to deploy a FastAPI + Nginx docker-compose stack to an AWS EC2 instance, from provisioning to transfer and run.
- [[FastAPI AI Deployment (Docker + Azure)]] — Guide to shipping a heavy-dependency FastAPI service to Azure App Service via Docker Hub, with GitHub Actions automation.
- [[Running Kubernetes Locally]] — How to run Kubernetes locally, the deployment.yaml/service.yaml MLOps blueprint, and the kubectl workflow commands.
- [[Web App Deployment (React + NET)]] — Deploying a React + .NET app to Azure App Service with GitHub Actions CI/CD, without containers.
- [[AWS Bedrock Agent Core]] `raw` — Pasted CLI and Python snippets for configuring, launching, and adding memory to an agent on AWS Bedrock AgentCore with LangGraph.
- [[Google ADK Deployment And A2A]] `raw` — How ADK's to_a2a() wraps an agent in an A2A server with an auto-generated agent card, and how to serve and call it from another agent.
- [[Model Hosting (Hugging Face Spaces)]] `stub` — Short walkthrough of hosting a model on Hugging Face Spaces with Gradio and calling it from a client.

## Book notes
- [[Practical MLOps Ch1 - DevOps Foundations]] — Practical MLOps chapter 1 definitions: continuous integration, continuous delivery, microservices, infrastructure as code, and monitoring and instrumentation.

## Interviews
- [[AWS SageMaker]] — What SageMaker is as a managed end-to-end ML platform, mapped tool by tool against the open-source stack, and why telecom shops pick it over running their own Kubernetes.

## Related hubs
[[MLOps]], [[Docker]], [[FastAPI]], [[Kubernetes]], [[Agents]], [[Agent Memory]]

## Notes to self (from the audit)
- [[AWS Bedrock Agent Core]]: Pasted commands with almost no prose - add a short explanation of what each agentcore step does.
- [[Model Hosting (Hugging Face Spaces)]]: Thin - add secrets, hardware tiers and cold-start behaviour.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
