---
description: "Build spec for ResolveFlow — a multi-tenant agentic customer-support platform that demonstrates all 13 agent-engineering concepts in one flagship portfolio project. Merges the CV's Customer Support Agent + Multi-Tenant RAG entries."
domain: ai-eng
type: project-spec
status: digested
tags:
  - domain/ai-eng
  - type/project-spec
  - topic/agents
  - agents
  - portfolio
  - resolveflow
  - flagship
hubs:
  - "[[Agent Engineering MOC]]"
  - "[[Agents]]"
date: 2026-09-22
source: "Kassra growth-track session 2026-09-22; merges Claude + Codex proposals"
---
# ResolveFlow — Flagship Build Spec

> The one project that turns the 13-note [[Agent Engineering MOC]] cluster into shipped, provable code. **Merges two CV entries** (Customer Support Agent + Multi-Tenant RAG) into a single flagship — fewer disconnected demos, one strong product. Reuses existing strengths (FastAPI, LangChain, Redis, pgvector, Docker, multi-tenancy) and makes the weak areas (evaluation, testing, observability) *visible*.

## The pitch
**ResolveFlow — a multi-tenant agentic customer-support operations platform.** A company connects its docs, customer DB, billing, and policies. ResolveFlow investigates a ticket, proposes an evidence-grounded resolution, executes safe actions, and **pauses for human approval before anything consequential** (refunds, cancellations, account changes).

## The execution graph
```text
Customer ticket
      ↓
Input guardrails (PII / injection / tenant check)
      ↓
Structured intent router  → TicketIntent (Pydantic)
      ↓
Case supervisor / planner
      ├──────────────┬───────────────┬───────────────┐
   KB worker      Account tool     Policy worker    (parallel)
   RAG search     CRM / orders     refund rules
      └──────────────┴───────────────┴───────────────┘
      ↓
Resolution agent — ReAct tool loop  (step-limited)
      ↓
Evaluator / grounding check  → retry ≤ 2 (evaluator-optimizer)
      ↓
Risk classifier  → consequential?
      ↓ yes
Human approval (LangGraph interrupt)  → approve / edit / reject
      ↓
Idempotent action execution  (exactly once)
      ↓
Output guardrail → streamed response + LangSmith trace + 👍/👎
```

## How it covers all 13 concepts
| # | Concept (note) | ResolveFlow feature |
|---|---|---|
| 1 | [[LangGraph Reducers, Routing And Step-Limit Loops]] | reducers accumulate evidence/events; conditional edges route; every loop hard-capped |
| 2 | [[Agent Reasoning Patterns]] | ReAct for investigation, plan-execute for complex cases, reflection for answer polish, multi-candidate for hard cases |
| 3 | [[Agent Workflow Patterns (The Five)]] | chaining (normal path) · parallel retrieval · intent routing · supervisor-workers · evaluator-optimizer retries |
| 4 | [[LangGraph Short-Term & Long-Term Memory]] | Postgres checkpointer per conversation; namespaced customer prefs + prior resolutions (Store) |
| 5 | [[Context Engineering]] | Write/Select/Compress/Isolate — retrieve only relevant docs, summarize old turns, group tools, isolate worker contexts |
| 6 | [[Agent Handoffs And Tool Design]] | billing / technical / account / retention specialists; narrow typed tools grouped by domain |
| 7 | [[Agent Guardrails]] | injection + PII in; grounding + policy + brand out; **fail-closed** on actions |
| 8 | [[Human-in-the-Loop (Approval & Interrupts)]] | interrupt before refunds, cancellations, credits, outbound email, account edits |
| 9 | [[Streaming And Structured Outputs]] | SSE progress events + Pydantic `TicketIntent`, `ResolutionPlan`, `ProposedAction` |
| 10 | [[LLM Gateways]] | model aliases, fallback, retry, per-tenant rate limits + budget accounting |
| 11 | [[LLM Caching]] | Redis exact + semantic cache, embedding cache, provider prompt-prefix cache |
| 12 | [[LangSmith]] (observability) | traces of tool calls, tokens, cost, latency, cache hits, errors + user feedback |
| 13 | [[Agent Trajectory Evaluation]] | did it pick the right tools *in the right order*, not just sound right — gate releases in CI |

**Bonus tracks it also touches:** multi-tenant isolation (system design), pgvector RAG, Temporal (durable escalations), MCP (expose the tools).

> [!warning] Expose plans, not raw chain-of-thought
> Surface structured *plans, evidence, actions, and concise rationale* to the UI/logs — never the model's private raw reasoning.

## Stack
LangGraph (runtime) · FastAPI + SSE (API/stream) · PostgreSQL + pgvector (data/RAG) · Redis (cache + memory) · LiteLLM/OpenRouter (gateway) · Celery (simple jobs) or Temporal (durable ingestion) · LangSmith/Langfuse + `agentevals` + Pytest (eval) · Docker Compose + GitHub Actions · a simple dashboard (trace, evidence, approval card, resolution).

## Build in 4 milestones (each demoable)
1. **Core agent** — tenant-aware ingestion, ticket routing, parallel workers, supervisor synthesis, mock CRM/billing tools, streaming. *(1,2,3,6,13)*
2. **Safety & state** — checkpoints, long-term memory, guardrails, step limits, idempotency keys, approval interrupts. *(4,5,8,9)*
3. **Production layer** — LLM gateway, caching, budgets, retries, fallback models, structured events. *(7,10,11)*
4. **Evidence it works** — 50–100 ticket dataset (normal + prompt-injection + missing-evidence + tool-failure + cross-tenant + refund + repeated-action), trajectory eval + CI quality gate. *(11,12)*

> [!tip] Don't start with
> Voice, a fancy frontend, or a real Zendesk integration. Prove the graph + eval system first.

## The portfolio demo (one memorable scenario)
> A customer reports a **duplicate charge** and asks for a refund.

ResolveFlow: routes to billing → retrieves transactions + refund policy **in parallel** → detects the duplicate → produces a **structured refund proposal with citations** → **pauses for approval** → reviewer approves/edits/rejects → **resumes from checkpoint, refunds exactly once** → streams progress → records the full trace + eval result.

That single demo visibly proves: routing, tools, multi-agent coordination, RAG, structured output, guardrails, HITL, durability/idempotency, streaming, observability, and evaluation.

## On the CV — replace TWO entries with ONE
Remove the separate *Customer Support Agent* and *Multi-Tenant RAG System* entries; add:

**ResolveFlow — Multi-Tenant Agentic Support Platform**
*LangGraph, FastAPI, PostgreSQL/pgvector, Redis, Docker, LangSmith*
- Built a multi-tenant support-operations platform routing cases across specialized billing/technical/account agents, using parallel RAG + tool execution to produce evidence-grounded resolutions.
- Implemented durable conversation state, long-term customer memory, PII/policy guardrails, and human approval before refunds/cancellations and other consequential actions.
- Added streaming structured events, provider fallback + caching, full agent tracing, and **trajectory-evaluation CI across N scenarios**, achieving **X% task success at Y avg cost**.

> [!warning] Fill N / X / Y with REAL benchmarks
> Run the milestone-4 dataset and use measured numbers. Verified metrics beat estimated percentages, and the eval harness is exactly the "weak area made visible" that sets this apart from a course project.

## Why this is the right flagship
Existing CV strengths reused; weak areas (eval, testing, observability) made visible; every concept in the MOC demonstrated inside one believable product. It's the difference between "took a course" and "ships production agents."
