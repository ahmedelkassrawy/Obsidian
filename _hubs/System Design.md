---
description: "Hub: every note about System Design"
type: hub
domain: backend
tags:
  - type/hub
  - topic/system-design
---
# System Design

> [!info] A six-step method with latency numbers, scaling, queues, consistent hashing and layering patterns. Missing: worked end-to-end designs.
> Part of [[MOC - Backend]]. Also try the tag `#topic/system-design`.

## Concepts
- [[AI Workflows VS AI Agent]] — Separates fixed-code AI workflows (chaining, routing, parallelization) from autonomous agents, and gives rules for choosing or combining them.
- [[API Gateway]] — Explains what an API gateway does (single entry point, routing, auth, rate limiting) and how it differs from and works alongside a load balancer.
- [[Agentic System Best Practices]] — The patterns from Claude Code's architecture that transfer to any agentic system, starting with using an async generator as the agent loop instead of callbacks.
- [[Agents Best Practice]] — Production rules for agents treated as execution systems, not chat toys: orchestration, reliability handled by architecture, judgment left to the model.
- [[Backend Intro]] — Ground-level explanation of what a backend is, the journey of a request, why backends exist, and the frontend/backend wall including CORS and pooling.
- [[BootStrap Pipeline Best Practices]] — What Claude Code's startup sequence teaches about system design: each phase narrows the space of possibilities, and slow work is loaded in parallel.
- [[Caching]] — Introduction to caching: why it matters, cache types, read and write strategies, hit/miss, and invalidation problems.
- [[Claude Code Core Architecture]] — Deep dive into Claude Code's architecture: what separates an agent from a chatbot, the tech stack and scale, the execution flow, core components and the key design patterns.
- [[Concurrency]] — Shows a race condition in concurrent transactions and walks the fixes: single threading, locking and fine-grained locks, with common mistakes.
- [[Consistent Hashing]] — Explains the consistent hashing ring, the rebalancing problem it solves, and how to present it in a system design interview.
- [[DB Replications]] — Compares master/backup and multi-master replication, synchronous vs asynchronous, and the trade-offs of each including eventual consistency.
- [[Full Text Search using Elasticsearch for Blazingly Fast Search]] — Why LIKE queries stop scaling and how an inverted index plus Elasticsearch relevance scoring solves search at size.
- [[Handlers, Services, Repositories, Middleware & Request Context]] — Explains the handler/service/repository split, what middleware does in the request lifecycle, and why a request context object exists.
- [[Horizontal vs Vertical Scaling]] — Compares scaling up and scaling out, when each applies, and how both play out specifically for databases.
- [[Message Queues  (RabbitMQ)]] — Why message queues exist beyond request/response, polling vs push delivery, queue vs pub-sub, and when a queue is actually warranted.
- [[Singleton]] — Explains the Singleton pattern, a __new__-based Python implementation, and its pros, cons and sane use cases.
- [[System Design for AI Agents (Architecture and the Why)]] — Trains you to defend every agent design decision: start from constraints, place the system on the agency spectrum, split into single-responsibility agents, and route for cost vs quality.
- [[Uber Eats — Designing Agents and Eval Loops (Production Case Study)]] — Production case study of Uber Eats' photo-enhancement agent system, focused on how each stage is wrapped in its own eval loop and how routing controls agency.
- [[camelAI - VM-less Agent in a Durable Object]] — Beginner-level walkthrough of how camelAI moved a coding agent off VMs into a Cloudflare Durable Object, explaining each term and comparing it to serverless sandboxes.
- [[URL Shortener System Design]] `raw` — Excalidraw whiteboard of a URL-shortener design - client, API layer, hashing/ID generation, the key-value store and the redirect path - stored as drawing data plus its text labels.

## How-tos & recipes
- [[Best Practices for SQL Connection Pooling]] — Lessons from a Node.js/PostgreSQL to-do app on connection pooling and database permissions, with the problems hit and the fixes applied.
- [[Phase0]] — A fixed six-step method for attacking any system design prompt, plus the latency numbers and back-of-envelope estimation math behind steps 2-5.

## Book notes
- [[Agent UX Design]] — Ch3 notes on user experience for agentic systems: text and terminal interfaces, the discoverability problem, GUIs and generative UIs.
- [[Building Applications with Agents.Ch1 & 2]] — Ch1-2 notes: build a minimal 'cancel order' agent in a LangGraph StateGraph, why scoping matters, a minimal evaluation, and the core components of an agent system.

## Course notes
- [[BASE Model vs ACID]] — Course notes on the BASE model used by NoSQL stores (basically available, soft state, eventually consistent) and how it contrasts with ACID.
- [[CAP Theorem]] — Course notes on the CAP theorem: the three properties, why partition tolerance is not optional, and the AP/CP design choice.
- [[Caching - Capacity Estimation and Strategies]] — System Design lecture on caching: capacity estimation for a growing e-commerce system, cache placement, strategies and invalidation.
- [[Observability - Signals, Pillars and Correlation]] — Introduces observability through a fitness analogy: the four golden signals, the three pillars (metrics, logs, traces), correlation and a worked dice-game dashboard.

## Clippings (raw)
- [[Clipping - Caching Strategies (YouTube, Arabic)]] `raw` — Raw Arabic YouTube transcript on caching: what a cache buys you, the caching strategies and their trade-offs, eviction policies, and cache invalidation.
- [[Clipping - Observability From Scratch Part 1 (Podcast, Arabic)]] `raw` — Raw Arabic podcast transcript (Tech Podcast, part 1) introducing observability from scratch - logs, metrics and traces and why monitoring alone is not enough.

## Related hubs
[[Agents]], [[Caching]], [[Database Replication & Sharding]], [[Claude Code]], [[AI Evaluation]], [[API Design]]

## Notes to self (from the audit)
- [[Caching - Capacity Estimation and Strategies]]: Overlaps 'Caching.md' in the same folder - consider merging or cross-linking.
- [[Clipping - Caching Strategies (YouTube, Arabic)]]: Digest into Backend/System Design/Caching.
- [[Clipping - Observability From Scratch Part 1 (Podcast, Arabic)]]: Digest into Backend/Observability. Part 2 is not in the vault - grab it while you are there.
- [[URL Shortener System Design]]: It is an Excalidraw drawing: the text only makes sense in Excalidraw view. Worth writing up as a normal note next to it.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
