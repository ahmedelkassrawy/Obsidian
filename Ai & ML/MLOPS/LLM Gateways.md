---
description: "The LLM gateway pattern — one API in front of many model providers, adding fallback, retries, caching, cost control, rate limits, key management and observability. What it is, a minimal code version, LiteLLM/OpenRouter, and best practices."
domain: ai-eng
type: concept
status: digested
tags:
  - domain/ai-eng
  - type/concept
  - status/digested
  - topic/llmops
  - topic/api-design
  - topic/system-design
  - llm-gateway
  - openrouter
  - litellm
  - fallback
  - cost-control
hubs:
  - "[[MLOps]]"
  - "[[API Design]]"
date: 2026-09-21
source: "Kassra growth-track session 2026-09-21"
---
# LLM Gateways

> Related: [[LLMOps Observability And Production Stack]] · [[Agent Workflow Patterns (The Five)]] (tier routing) · [[Agent Guardrails]]. This is also one of the **system-design AI-bank designs** ("an LLM gateway — rate limits / fallbacks / cost").

A **gateway** = a single entry point in front of many model providers, so the app talks to *one* API and the gateway handles the production concerns. You already use one — **OpenRouter is an LLM gateway** (that's why raaaaag points `base_url` at it).

```text
your app ──▶ ┌─────── LLM GATEWAY ───────┐ ──▶ OpenAI
one API      │ routing · fallback · retry │ ──▶ Anthropic
             │ cache · cost · rate-limit  │ ──▶ your vLLM
             │ keys · logging · guardrails│ ──▶ Cohere
             └───────────────────────────┘
```

> [!definition] LLM gateway
> A proxy between your app and one-or-many model providers. Your code makes one standard call; the gateway adds cross-cutting production concerns — fallback, retries, caching, cost control, key management, rate limits, observability — so every app doesn't re-implement them. It's the **reverse-proxy / API-gateway idea from system design**, specialized for LLMs.

## The jobs it does
| Job | What it solves |
|---|---|
| Unified API | swap GPT-4o ↔ Claude ↔ your vLLM by changing a string, not code |
| Fallback / failover | provider down or rate-limited → auto-retry on another model |
| Retries + backoff | transient 500s/timeouts handled once, centrally (+ jitter) |
| Caching | identical prompt → cached response, skip the paid call |
| Cost tracking + budgets | count tokens/spend per app/user; hard-cap runaway usage |
| Rate limiting | per-key/per-tenant caps (the sliding-window limiter, here) |
| Key management | provider keys live in the gateway, not scattered in apps |
| Observability | one place logging every call (latency, tokens, errors) |

## Minimal gateway — the core ideas in code
```python
import hashlib
from langchain_openai import ChatOpenAI

MODELS = {   # one string picks provider + model
    "fast":  ChatOpenAI(model="openai/gpt-4o-mini",
                        base_url="https://openrouter.ai/api/v1", api_key=KEY),
    "smart": ChatOpenAI(model="anthropic/claude-3.5-sonnet",
                        base_url="https://openrouter.ai/api/v1", api_key=KEY),
    "local": ChatOpenAI(model="qwen", base_url="http://localhost:8000/v1", api_key="x"),
}
FALLBACK = {"smart": "fast", "fast": "local"}   # who to try if one fails
_cache: dict[str, str] = {}

def gateway(prompt: str, tier: str = "fast") -> str:
    key = hashlib.sha256(f"{tier}:{prompt}".encode()).hexdigest()
    if key in _cache:                       # 1. CACHE
        return _cache[key]

    tried, name = [], tier
    while name:                             # 2. FALLBACK CHAIN
        try:
            resp = MODELS[name].invoke(prompt)   # (retries/backoff go here)
            _cache[key] = resp.content           # 3. store
            log(name, prompt, resp)              # 4. OBSERVABILITY + cost
            return resp.content
        except Exception as e:
            tried.append(name)
            name = FALLBACK.get(name)            # try the next model
    raise RuntimeError(f"all models failed: {tried}")
```
Four gateway jobs visible: **cache → fallback chain → logging/cost → unified invoke.** The app calls `gateway(prompt, "smart")` and never knows which provider answered.

## Don't build it — use one (usually)
| Option | What it is |
|---|---|
| **OpenRouter** | hosted gateway; one key, 100+ models (what raaaaag uses) |
| **LiteLLM** | self-host proxy; unified API + fallback + budgets + caching + keys |
| **Portkey / Cloudflare AI Gateway** | hosted; caching, analytics, guardrails |

```python
import litellm
litellm.completion(
    model="anthropic/claude-3.5-sonnet",
    messages=[{"role": "user", "content": "hi"}],
    fallbacks=["gpt-4o-mini"],      # auto-failover
    # + budgets, caching, per-key rate limits via the proxy config
)
```

## Best practices
- **Fallback across *providers*, not just models** — an OpenAI outage shouldn't take you down if Anthropic is up.
- **Cache identical calls** — dedupe by hash of (model + messages + params); big cost win on repeats.
- **Budgets + hard caps** — a looping bug shouldn't cost $10k; cap per key/tenant, fail-closed on spend.
- **Centralize keys** — provider keys in the gateway only; apps hold a *gateway* key. One place to rotate.
- **Route by tier** — cheap model for easy tasks, big model for hard (pairs with the routing workflow).
- **Fail-open vs fail-closed** — if the gateway itself is down, decide: block, or let apps hit a provider directly? (Same call as the rate limiter / guardrails.)
- **Stream-through** — pass streaming tokens, don't buffer the whole response.

> [!tip] The through-line
> A gateway is **the reverse proxy for LLMs**: one door, many models, with fallback / cache / cost / keys / limits pulled into that door. Don't scatter provider logic across apps — centralize it. And usually **don't build one** — OpenRouter or LiteLLM already do; build only for custom routing/policy.

## Fits
- **raaaaag** already goes through **OpenRouter** (a gateway) — that's how a string swaps models.
- **Shutterabia:** a gateway would centralize the model calls its MCP tools make — cost caps per client, fallback if a provider is down, one key to rotate.
- **System design:** this *is* the AI-bank "LLM gateway" design — the design and the code are the same thing.
