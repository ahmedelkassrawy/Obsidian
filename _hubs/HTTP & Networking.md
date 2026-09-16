---
description: "Hub: every note about HTTP & Networking"
type: hub
domain: backend
tags:
  - type/hub
  - topic/http-and-networking
---
# HTTP & Networking

> [!info] SSL/TLS, headers vs cookies, the Postgres wire protocol. Missing: HTTP caching headers, CORS in depth and load balancers.
> Part of [[MOC - Backend]]. Also try the tag `#topic/http-and-networking`.

## Concepts
- [[API Gateway]] — Explains what an API gateway does (single entry point, routing, auth, rate limiting) and how it differs from and works alongside a load balancer.
- [[Backend Intro]] — Ground-level explanation of what a backend is, the journey of a request, why backends exist, and the frontend/backend wall including CORS and pooling.
- [[Nginx]] — What NGINX actually does - web server, reverse proxy, load balancer, cache - and why you would pick it over other servers.
- [[SSL,TLS]] — Plain-English guide to SSL/TLS: goals, versions, the handshake step by step, the record layer, cipher suites and why TLS 1.3 is better.
- [[gRPC and Protocol Buffers]] — Deep dive from HTTP/1 vs HTTP/2 fundamentals through Protocol Buffers and a hands-on gRPC service implementation.

## How-tos & recipes
- [[FastAPI - Webhooks]] — Implementation guide for outgoing and incoming webhooks in FastAPI, with config, signature handling and the supporting code components.
- [[Ngrok]] `stub` — A snippet that starts an ngrok tunnel in front of a local FastAPI app to get a public URL.

## References & cheat sheets
- [[Complete REST API Design]] — Full REST API design reference: the six constraints, URL naming, HTTP methods and idempotency, CRUD patterns, pagination/filtering/sorting and custom actions.
- [[Headers VS Cookie]] — Side-by-side comparison of HTTP headers and cookies: purpose, transport, storage, security and how to read each one in FastAPI.
- [[Requests]] `raw` — Two pasted Python requests snippets showing a POST with a JSON payload and a GET against a local FastAPI service.

## Book notes
- [[Ch6.Real-Time Communication with Generative Models]] — Ch6 notes comparing request/response, short polling, long polling, Server-Sent Events and WebSockets for streaming model output.
- [[Ch2. Selecting Your API Architecture]] — Book chapter comparing REST, webhooks, GraphQL, SOAP, WebSockets and gRPC with adoption numbers and when each architecture fits.

## Course notes
- [[Deep Look into Postgres Wire Protocol with Wireshark]] — Course notes tracing a Node.js to PostgreSQL connection in Wireshark: TCP handshake, startup message, auth request, query and teardown.
- [[Encryption]] — Course notes on symmetric vs asymmetric encryption, where each is used, and the TLS-termination-at-the-load-balancer debate.

## Clippings (raw)
- [[Clipping - Controllers Services and Repositories (YouTube)]] `raw` — Raw YouTube transcript walking through the request lifecycle in a backend server: what controllers, services, repositories, middlewares and request context each own.
- [[Clipping - REST API Design (YouTube)]] `raw` — Raw YouTube transcript of an end-to-end REST API design walkthrough - resources, verbs, status codes, versioning and pagination.

## Related hubs
[[API Design]], [[FastAPI]], [[Auth & Security]], [[System Design]], [[gRPC]], [[Cloud Deployment]]

## Notes to self (from the audit)
- [[Requests]]: Code-only scratch note.
- [[Clipping - Controllers Services and Repositories (YouTube)]]: Digest into Backend/Principles - this is the layering argument that note should make.
- [[Clipping - REST API Design (YouTube)]]: Digest into Backend/Principles - biggest single clipping (20k words), split it before writing.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
