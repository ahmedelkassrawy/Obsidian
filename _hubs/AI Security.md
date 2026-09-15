---
description: "Hub: every note about AI Security"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/ai-security
---
# AI Security

> [!info] Guardrails, rate limiting, prompt attacks and agent sandboxing. Thin - the sandbox note is a stub.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/ai-security`.

## Concepts
- [[Sandbox in Agent]] `stub` — Sketch of a two-layer agent sandbox: a Docker container per deployed agent, and a bubblewrap sandbox per bash tool call.

## Book notes
- [[Ch5. Prompt Engineering]] — Chip Huyen Ch5 notes: what makes a prompt effective, and how to defend an application against prompt injection and other prompt attacks.
- [[Ch9.Securing AI Services]] — Ch9 notes on I/O guardrails for model inputs and outputs, plus the four rate-limiting algorithms (token bucket, leaky bucket, fixed and sliding window) compared for AI traffic.

## Related hubs
[[Agents]], [[Prompting]], [[Auth & Security]]

## Notes to self (from the audit)
- [[Sandbox in Agent]]: Placeholder - expand into a real note on isolating agent tool execution.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
