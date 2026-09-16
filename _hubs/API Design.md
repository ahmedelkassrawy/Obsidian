---
description: "Hub: every note about API Design"
type: hub
domain: backend
tags:
  - type/hub
  - topic/api-design
---
# API Design

> [!info] REST constraints, URL naming, idempotency, pagination and input validation. Missing: versioning in practice and an OpenAPI-first contract workflow.
> Part of [[MOC - Backend]]. Also try the tag `#topic/api-design`.

## Concepts
- [[06 - Request vs Response Models Explained]] — Explains why request and response models are separate: filtering secrets out, transforming data and better auto-docs.
- [[API Gateway]] — Explains what an API gateway does (single entry point, routing, auth, rate limiting) and how it differs from and works alongside a load balancer.
- [[API Validations & Transformations]] — Why you validate and transform every incoming payload at the controller layer, with the syntactic/semantic/type validation split and a pipeline example.
- [[FastAPI Async and Routers]] — Explains when to declare a FastAPI path function async vs sync, and what an APIRouter is for.
- [[Handlers, Services, Repositories, Middleware & Request Context]] — Explains the handler/service/repository split, what middleware does in the request lifecycle, and why a request context object exists.
- [[JWT - API AUTH]] — Explains why JWT exists, its header/payload/signature parts, and how the signature makes stateless authentication possible.
- [[MLOps Maturity And Production Practices]] — Community-talk notes on getting models to production: MLOps maturity levels and anti-patterns, Python project structure with pyproject.toml, serving a model as a REST API, and ONNX export.
- [[gRPC and Protocol Buffers]] — Deep dive from HTTP/1 vs HTTP/2 fundamentals through Protocol Buffers and a hands-on gRPC service implementation.

## How-tos & recipes
- [[04 - API Endpoints with Database Operations]] — Writes the CRUD endpoints against the database, including where each parameter comes from and the add/commit/refresh dance.
- [[FastAPI - Webhooks]] — Implementation guide for outgoing and incoming webhooks in FastAPI, with config, signature handling and the supporting code components.

## References & cheat sheets
- [[Complete REST API Design]] — Full REST API design reference: the six constraints, URL naming, HTTP methods and idempotency, CRUD patterns, pagination/filtering/sorting and custom actions.

## Book notes
- [[Ch2.Getting Started with FastAPI]] — Ch2 notes on FastAPI: first server setup, dependency injection, Pydantic v2 validation, auto docs, project structure and onion architecture.
- [[Ch2. Selecting Your API Architecture]] — Book chapter comparing REST, webhooks, GraphQL, SOAP, WebSockets and gRPC with adoption numbers and when each architecture fits.

## Course notes
- [[FastAPI - Asynchronous Code and Path Parameters]] — FastAPI course notes on async routes, HTTP methods, path and query parameters, Enum-constrained values and request bodies.
- [[FastAPI - Response Models and Status Codes]] — FastAPI course notes on response models and return types, multiple models for different purposes, and choosing HTTP status codes.

## Clippings (raw)
- [[Clipping - Controllers Services and Repositories (YouTube)]] `raw` — Raw YouTube transcript walking through the request lifecycle in a backend server: what controllers, services, repositories, middlewares and request context each own.
- [[Clipping - REST API Design (YouTube)]] `raw` — Raw YouTube transcript of an end-to-end REST API design walkthrough - resources, verbs, status codes, versioning and pagination.
- [[Clipping - Validation and Transformation Pipelines (YouTube)]] `raw` — Raw YouTube transcript on where validation and transformation belong in a backend request pipeline and what each layer should reject.

## Related hubs
[[FastAPI]], [[HTTP & Networking]], [[Pydantic]], [[System Design]], [[Concurrency & Async]], [[gRPC]]

## Notes to self (from the audit)
- [[Clipping - Controllers Services and Repositories (YouTube)]]: Digest into Backend/Principles - this is the layering argument that note should make.
- [[Clipping - REST API Design (YouTube)]]: Digest into Backend/Principles - biggest single clipping (20k words), split it before writing.
- [[Clipping - Validation and Transformation Pipelines (YouTube)]]: Digest into API/FastAPI/Pydantic.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
