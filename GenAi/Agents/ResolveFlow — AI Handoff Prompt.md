---
description: "Paste-into-a-new-chat handoff brief to build ResolveFlow from scratch — self-contained: goal, the 13 concepts to demonstrate, architecture, stack, milestone plan, constraints, and the first task."
domain: ai-eng
type: handoff
status: digested
tags: [domain/ai-eng, type/handoff, topic/agents, resolveflow, portfolio]
hubs: ["[[ResolveFlow — Flagship Build Spec]]"]
date: 2026-09-22
---
# ResolveFlow — AI Handoff Prompt

> Copy everything below the line into a new AI chat to start building. It's self-contained.

---

You are helping me build **ResolveFlow**, my flagship portfolio project as an AI engineer. Work with me step by step — explain design choices briefly, write runnable code, and let me build/verify each part before moving on. I'm on **Windows (PowerShell)**, Python via **base conda (no venvs)**, and I use OpenRouter for models.

## What ResolveFlow is
A **multi-tenant agentic customer-support operations platform**. A company connects its docs, customer DB, billing, and policies. ResolveFlow investigates a support ticket, proposes an evidence-grounded resolution, executes safe actions, and **pauses for human approval before anything consequential** (refunds, cancellations, account changes).

## Why I'm building it
It's one flagship project that demonstrates **all 13 production agent-engineering concepts** in believable, shipped code (it replaces two separate CV projects: a customer-support agent and a multi-tenant RAG system). The goal is portfolio proof that I can build production agents, not toy demos.

## The 13 concepts it must demonstrate
1. **LangGraph core** — reducers (accumulate evidence/messages), conditional routing, step-limited loops
2. **Reasoning patterns** — ReAct for investigation, plan-and-execute for complex cases, reflection for answer polish
3. **Workflow patterns** — chaining (normal path), parallel retrieval, intent routing, supervisor-workers, evaluator-optimizer retry
4. **Memory** — Postgres checkpointer (per conversation) + namespaced Store (per-customer prefs/history)
5. **Context engineering** — retrieve only relevant docs, summarize old turns, group tools, isolate worker contexts
6. **Handoffs & tool design** — supervisor → billing/technical/account specialists; narrow typed tools grouped by domain
7. **Guardrails** — input PII/injection + tenant check; output grounding/policy/brand; fail-closed on actions
8. **Human-in-the-loop** — LangGraph `interrupt` before refunds/cancellations/credits/account edits
9. **Streaming & structured outputs** — SSE progress events + Pydantic models (`TicketIntent`, `ResolutionPlan`, `ProposedAction`)
10. **LLM gateway** — model aliases, fallback, retry, per-tenant rate limits + budget accounting (LiteLLM or OpenRouter)
11. **Caching** — Redis exact + semantic cache, embedding cache, provider prompt-prefix cache
12. **Observability** — LangSmith/Langfuse traces (tool calls, tokens, cost, latency, cache hits, errors) + 👍/👎 feedback by run_id
13. **Trajectory evaluation** — score whether the agent picked the right tools in the right order (not just the final answer); gate releases in CI (`agentevals` + Pytest + GitHub Actions)

> Expose structured plans/evidence/actions/rationale to the UI and logs — never raw private chain-of-thought.

## Architecture (target)
```text
Customer ticket
  → input guardrails (PII / injection / tenant check)
  → structured intent router  → TicketIntent
  → case supervisor / planner
       ├─ KB worker (RAG search)   ┐ parallel
       ├─ account tool (CRM/orders)│
       └─ policy worker (refund rules) ┘
  → resolution agent (ReAct, step-limited)
  → evaluator / grounding check  → retry ≤ 2
  → risk classifier → consequential?
       → yes: human approval (interrupt) → approve/edit/reject
  → idempotent action execution (exactly once)
  → output guardrail → streamed response + trace + feedback
```

## Stack
LangGraph · FastAPI + SSE · PostgreSQL + pgvector · Redis · LiteLLM/OpenRouter (gateway) · Celery or Temporal (background/durable) · LangSmith or Langfuse + `agentevals` + Pytest · Docker Compose · GitHub Actions · a simple dashboard (trace + evidence + approval card + resolution).

## Build plan — 4 milestones (build in order, each demoable)
1. **Core agent** — tenant-aware doc ingestion, ticket routing, parallel workers, supervisor synthesis, mock CRM/billing tools, streaming. *(concepts 1,2,3,6,9)*
2. **Safety & state** — Postgres checkpointer, long-term Store memory, guardrails, step limits, idempotency keys, approval interrupts. *(4,5,7,8)*
3. **Production layer** — LLM gateway, caching, budgets, retries, fallback models. *(10,11)*
4. **Evidence** — dataset of 50–100 tickets (normal + prompt-injection + missing-evidence + tool-failure + cross-tenant + refund + repeated-action), trajectory eval + CI quality gate + LangSmith tracing/feedback. *(11,12,13)*

Do **not** start with voice, a fancy frontend, or a real Zendesk integration — prove the graph + eval first.

## The demo that proves everything (target end state)
> A customer reports a **duplicate charge** and asks for a refund.

Route to billing → retrieve transactions + refund policy **in parallel** → detect the duplicate → produce a **structured refund proposal with citations** → **pause for approval** → reviewer approves → **resume from checkpoint, refund exactly once** → stream progress → record the full trace + eval result.

## Start here (Milestone 1, first task)
Scaffold the repo and build the **core graph skeleton**:
- Repo layout (`src/` with `graph/`, `tools/`, `rag/`, `api/`; `tests/`; `evals/`; `docker-compose.yml`; `pyproject.toml`).
- A LangGraph `StateGraph` with: `input_guard → router → supervisor → {billing, technical, account} workers → resolution → output`, message-accumulating state, and a step limit.
- One specialist (billing) with 1–2 mock typed tools.
- A FastAPI `POST /ticket` endpoint that **streams** the run over SSE.
- Use `ChatOpenAI(base_url="https://openrouter.ai/api/v1")`.

Give me the folder structure and the graph skeleton first; I'll run it, then we add the billing worker + RAG. Explain each design choice in 1–2 lines as we go.
