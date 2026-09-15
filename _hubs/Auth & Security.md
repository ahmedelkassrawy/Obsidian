---
description: "Hub: every note about Auth & Security"
type: hub
domain: backend
tags:
  - type/hub
  - topic/auth-and-security
---
# Auth & Security

> [!info] JWT, OAuth2/OpenID, RBAC and the whole FastAPI Users series. Most FastAPI Users notes are still doc excerpts rather than your own words.
> Part of [[MOC - Backend]]. Also try the tag `#topic/auth-and-security`.

## Concepts
- [[JWT - API AUTH]] — Explains why JWT exists, its header/payload/signature parts, and how the signature makes stateless authentication possible.
- [[SSL,TLS]] — Plain-English guide to SSL/TLS: goals, versions, the handshake step by step, the record layer, cipher suites and why TLS 1.3 is better.

## How-tos & recipes
- [[Agent with Tools]] — Tutorial notes on building a secure multi-user agent with Arcade.dev and LangGraph: per-user identity, authorized tool calls, and human-in-the-loop approval.
- [[Best Practices for SQL Connection Pooling]] — Lessons from a Node.js/PostgreSQL to-do app on connection pooling and database permissions, with the problems hit and the fixes applied.
- [[Enabling SSL,TLS]] — Step-by-step guide to enabling SSL/TLS on a Dockerised PostgreSQL, including generating certs and proving the traffic is encrypted.
- [[RBAC - Role Base Access Control]] — Cheat sheet for adding role-based access control to FastAPI: role field on the user model, a dependency that checks roles, and guarded routes.

## References & cheat sheets
- [[Headers VS Cookie]] — Side-by-side comparison of HTTP headers and cookies: purpose, transport, storage, security and how to read each one in FastAPI.
- [[FastAPI Users - Auth Backend]] `raw` — Combines a transport and a strategy into a FastAPI Users AuthenticationBackend (bearer + JWT example).
- [[FastAPI Users - Auth Router]] `raw` — Mounting the FastAPI Users auth router to get /login and /logout for a given backend.
- [[FastAPI Users - Auth Strategy]] `raw` — The strategy half of FastAPI Users auth: database-stored tokens vs JWT, with the tables and code each needs.
- [[FastAPI Users - Auth Transport]] `raw` — The transport half of FastAPI Users auth: cookie vs bearer, and when each fits browser or API clients.
- [[FastAPI Users - Full Example Layout]] `stub` — A link to the FastAPI Users full example plus the file tree it produces.
- [[FastAPI Users - OAuth2]] `empty` — Empty note - contains only a link to the FastAPI Users OAuth2 docs page.
- [[FastAPI Users - Password Hashing]] `raw` — How to swap the password hashing algorithm in FastAPI Users by passing your own pwdlib PasswordHash to PasswordHelper.
- [[FastAPI Users - Register Router]] `raw` — Mounting the FastAPI Users register router to expose a /register endpoint.
- [[FastAPI Users - Reset Password Router]] `raw` — Mounting the FastAPI Users reset-password router for /forgot-password and /reset-password.
- [[FastAPI Users - Router Setup]] `raw` — How to configure the FastAPIUsers object with the user manager and auth backends before mounting any routers.
- [[FastAPI Users - SQLAlchemy Adapter]] `raw` — The SQLAlchemy database adapter setup for FastAPI Users, including the async-session expire_on_commit=False warning.
- [[FastAPI Users - Schemas]] `raw` — The read/create/update Pydantic schemas FastAPI Users expects, and how to add your own fields to them.
- [[FastAPI Users - UserManager]] `raw` — How to subclass BaseUserManager in FastAPI Users to hook into register, forgot-password and verify events.
- [[FastAPI Users - Users Router]] `raw` — Mounting the FastAPI Users users router for reading and updating user records.
- [[FastAPI Users - Verify Router]] `raw` — Mounting the FastAPI Users verify router for email verification routes.

## Book notes
- [[Ch8.Authentication and Authorization]] — Ch8 notes on auth for AI services: registration and login flows, password hashing, JWT access and refresh tokens, logout, and role-based authorization.
- [[Ch9.Securing AI Services]] — Ch9 notes on I/O guardrails for model inputs and outputs, plus the four rate-limiting algorithms (token bucket, leaky bucket, fixed and sliding window) compared for AI traffic.

## Course notes
- [[Deep Look into Postgres Wire Protocol with Wireshark]] — Course notes tracing a Node.js to PostgreSQL connection in Wireshark: TCP handshake, startup message, auth request, query and teardown.
- [[Encryption]] — Course notes on symmetric vs asymmetric encryption, where each is used, and the TLS-termination-at-the-load-balancer debate.
- [[FastApi - Security]] — FastAPI course notes on OAuth2 and OpenID Connect: how the flows work, OpenAPI security schemes, and a password-flow implementation with hashing and token models.

## Interviews
- [[InstaBug Assessment]] — The InstaBug written assessment with worked answers: ULID vs UUID as a primary key, race conditions and locks, webhooks, HTTP auth headers, statelessness, and page tables.

## Related hubs
[[FastAPI]], [[HTTP & Networking]], [[Postgres]], [[Agents]], [[Tool Use & Function Calling]], [[AI Security]]

## Notes to self (from the audit)
- [[FastAPI Users - Full Example Layout]]: Stub - just a link and a file list; paste the actual example or delete.
- [[FastAPI Users - OAuth2]]: Empty: link only, no content.
- [[InstaBug Assessment]]: Good interview material but the answers are generic; add one line per question on how you would say it out loud.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
