---
description: "Hub: every note about FastAPI"
type: hub
domain: backend
tags:
  - type/hub
  - topic/fastapi
---
# FastAPI

> [!info] The most complete area: async routes, params, Pydantic models, response models, security, webhooks, file uploads and project structure. Missing: background tasks vs Celery, and testing with TestClient.
> Part of [[MOC - Backend]]. Also try the tag `#topic/fastapi`.

## Concepts
- [[01 - Overview and Project Layout]] — Maps which of the three libraries owns which job and traces one POST request end to end through the project layout.
- [[06 - Request vs Response Models Explained]] — Explains why request and response models are separate: filtering secrets out, transforming data and better auto-docs.
- [[Concurrency and Async]] — Walks through sync vs async execution in Python, async/await, coroutines, and how concurrency and parallelism play out in FastAPI path operations.
- [[FastAPI - Structure]] — Compares flat and nested FastAPI project layouts and when each one stops scaling.
- [[FastAPI Async and Routers]] — Explains when to declare a FastAPI path function async vs sync, and what an APIRouter is for.
- [[Optimizing GenAI Services for Multiple Users]] — Why GenAI services block under load and how to fix it: concurrency vs parallelism, Python execution models, asyncio, and FastAPI concurrency choices.

## How-tos & recipes
- [[02 - Database Session Dependency (get_db)]] — Builds the get_db dependency: SessionLocal, yielding a session per request and closing it afterwards.
- [[03 - Pydantic Schemas (Request and Response Models)]] — Defines the Pydantic request and response schemas that sit in front of the ORM models.
- [[04 - API Endpoints with Database Operations]] — Writes the CRUD endpoints against the database, including where each parameter comes from and the add/commit/refresh dance.
- [[05 - Running and Testing the App]] — Runs the app with uvicorn and walks a full manual curl test of every endpoint, including the expected 404.
- [[05 - Sessions and sessionmaker]] — The session factory, the commit-on-exit default, object states and the FastAPI session dependency.
- [[AWS Deployment Plan]] — Step-by-step plan to deploy a FastAPI + Nginx docker-compose stack to an AWS EC2 instance, from provisioning to transfer and run.
- [[Celery - Complete Guide]] — End-to-end practical guide to Celery: whether you need it, broker choice, the four components, configuration, task patterns and production concerns.
- [[FastAPI - MongoDB]] — How to wire FastAPI to MongoDB with the async Motor driver: Docker container setup, ObjectId handling in Pydantic, models and CRUD endpoints.
- [[FastAPI - Webhooks]] — Implementation guide for outgoing and incoming webhooks in FastAPI, with config, signature handling and the supporting code components.
- [[FastAPI AI Deployment (Docker + Azure)]] — Guide to shipping a heavy-dependency FastAPI service to Azure App Service via Docker Hub, with GitHub Actions automation.
- [[RBAC - Role Base Access Control]] — Cheat sheet for adding role-based access control to FastAPI: role field on the user model, a dependency that checks roles, and guarded routes.
- [[FastAPI - Scheduler]] `stub` — A three-line snippet adding APScheduler BackgroundScheduler interval jobs inside a FastAPI app file.
- [[Ngrok]] `stub` — A snippet that starts an ngrok tunnel in front of a local FastAPI app to get a public URL.
- [[Sorting - Sort Three Numbers]] `raw` — Code snippets lifted from the RAG proof of concept: content hashing for duplicate detection, a global model cache, and the async document-processing function.

## References & cheat sheets
- [[07 - Full Source Listing (copy-paste ready)]] — The complete working source for the integrated app in two file layouts, ready to copy.
- [[08 - Gotchas and Troubleshooting]] — Catalogue of the real errors you hit wiring FastAPI, Pydantic and SQLAlchemy, each with cause and fix, searchable by error text.
- [[09 - Cheatsheet]] — One-screen condensed setup, schema and endpoint templates for the FastAPI + SQLAlchemy stack.
- [[Headers VS Cookie]] — Side-by-side comparison of HTTP headers and cookies: purpose, transport, storage, security and how to read each one in FastAPI.
- [[FastAPI Users - Auth Backend]] `raw` — Combines a transport and a strategy into a FastAPI Users AuthenticationBackend (bearer + JWT example).
- [[FastAPI Users - Auth Router]] `raw` — Mounting the FastAPI Users auth router to get /login and /logout for a given backend.
- [[FastAPI Users - Auth Strategy]] `raw` — The strategy half of FastAPI Users auth: database-stored tokens vs JWT, with the tables and code each needs.
- [[FastAPI Users - Auth Transport]] `raw` — The transport half of FastAPI Users auth: cookie vs bearer, and when each fits browser or API clients.
- [[FastAPI Users - Full Example Layout]] `stub` — A link to the FastAPI Users full example plus the file tree it produces.
- [[FastAPI Users - Register Router]] `raw` — Mounting the FastAPI Users register router to expose a /register endpoint.
- [[FastAPI Users - Reset Password Router]] `raw` — Mounting the FastAPI Users reset-password router for /forgot-password and /reset-password.
- [[FastAPI Users - Router Setup]] `raw` — How to configure the FastAPIUsers object with the user manager and auth backends before mounting any routers.
- [[FastAPI Users - SQLAlchemy Adapter]] `raw` — The SQLAlchemy database adapter setup for FastAPI Users, including the async-session expire_on_commit=False warning.
- [[FastAPI Users - Schemas]] `raw` — The read/create/update Pydantic schemas FastAPI Users expects, and how to add your own fields to them.
- [[FastAPI Users - UserManager]] `raw` — How to subclass BaseUserManager in FastAPI Users to hook into register, forgot-password and verify events.
- [[FastAPI Users - Users Router]] `raw` — Mounting the FastAPI Users users router for reading and updating user records.
- [[FastAPI Users - Verify Router]] `raw` — Mounting the FastAPI Users verify router for email verification routes.
- [[Pydantic Settings]] `raw` — A pasted config.py snippet showing pydantic-settings BaseSettings reading values from a .env file.

## Book notes
- [[Ch2.Getting Started with FastAPI]] — Ch2 notes on FastAPI: first server setup, dependency injection, Pydantic v2 validation, auto docs, project structure and onion architecture.
- [[Ch3. Serving GenAI Models with FastAPI]] — Ch3 notes: how transformers, tokenization, embeddings and positional encoding work, then how to serve text, image, audio and 3D models from a FastAPI app.
- [[Ch6.Real-Time Communication with Generative Models]] — Ch6 notes comparing request/response, short polling, long polling, Server-Sent Events and WebSockets for streaming model output.
- [[Ch7.Integrating DB in AI services]] — Ch7 notes on wiring a database into a FastAPI AI service: SQLAlchemy ORM models, the engine as a connection pool, session dependency injection, and Alembic migrations.
- [[Ch8.Authentication and Authorization]] — Ch8 notes on auth for AI services: registration and login flows, password hashing, JWT access and refresh tokens, logout, and role-based authorization.
- [[Ch3. Creating the Database Layer]] — Book chapter building the data layer: the three layers, the models file with Player/Performance/League/Team relationships, and the database config.

## Course notes
- [[FastAPI - Asynchronous Code and Path Parameters]] — FastAPI course notes on async routes, HTTP methods, path and query parameters, Enum-constrained values and request bodies.
- [[FastAPI - Pydantic]] — FastAPI course notes on Pydantic models: field validation and metadata, nested models, lists of submodels, special types and request-body examples.
- [[FastAPI - Request Files, MLOps, and API Metadata]] — FastAPI course notes on file uploads, Dockerizing the app, Prometheus metrics and Evidently drift monitoring, plus error handling and OpenAPI metadata.
- [[FastAPI - Response Models and Status Codes]] — FastAPI course notes on response models and return types, multiple models for different purposes, and choosing HTTP status codes.
- [[FastApi - Security]] — FastAPI course notes on OAuth2 and OpenID Connect: how the flows work, OpenAPI security schemes, and a password-flow implementation with hashing and token models.

## Project notes
- [[Project Talk to RAG]] — Project notes for a talk-to-your-documents RAG app: the extract, transform, embed and store pipeline, starting with the file-upload step.

## Meta
- [[00 - Index]] — Index for the FastAPI + Pydantic + SQLAlchemy folder: reading order, look-up notes and a 'I want to find' table.

## Clippings (raw)
- [[AI Engineering Specific Use Cases]] `raw` — Verbatim copy of section 8 of the h9-tec/AI_deployment README on serving ML models and validating data pipelines with FastAPI.
- [[Advanced Topics and Best Practices]] `raw` — Verbatim copy of section 7 of the h9-tec/AI_deployment README on async SQLAlchemy, dependency injection and other FastAPI best practices.

## Related hubs
[[Auth & Security]], [[Pydantic]], [[SQLAlchemy]], [[API Design]], [[Concurrency & Async]], [[HTTP & Networking]]

## Notes to self (from the audit)
- [[Pydantic Settings]]: Snippet only - no prose; worth expanding into a real settings note.
- [[FastAPI - Scheduler]]: Stub - explain scheduler lifecycle, shutdown and why not Celery.
- [[FastAPI Users - Full Example Layout]]: Stub - just a link and a file list; paste the actual example or delete.
- [[Advanced Topics and Best Practices]]: Copied README section - overlaps the digested 'Integrating FastAPI, Pydantic, and SQLAlchemy' folder.
- [[AI Engineering Specific Use Cases]]: Copied README section - not rewritten.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
