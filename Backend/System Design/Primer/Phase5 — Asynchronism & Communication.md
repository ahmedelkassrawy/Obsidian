---
tags: [backend, system-design, async, queues, back-pressure, idempotency, rest, rpc, tcp, udp]
domain: backend
type: lesson-note
status: digested
source: System Design Primer — Phase 5 (Asynchronism & Communication); Kassra growth-track session 2026-09-16
---
# Asynchronism & Communication

This phase is mostly **naming things you already built.** Temporal, your scheduler, retry+backoff, the idempotency guard, HMAC webhooks — all of it lives here.

## The core question: sync or async?

> [!definition] Sync vs Async
> **Sync** = the caller waits for the result before doing anything else.
> **Async** = the caller hands off the work and returns immediately; the result comes later (via a queue, callback, or poll).

- **Sync when** the user needs the answer *now* to continue — a search query, a login, reading a draft.
- **Async when** the work is slow, can fail-and-retry, or nobody's waiting on it — publishing a post, embedding 751 chunks, sending a webhook.
- **The rule:** if making the user wait adds no value (or the work might fail and need retrying), push it off the request path into a queue.

## Message queues vs task queues

> [!definition] Queue
> A buffer between a **producer** (puts work in) and a **consumer** (takes work out). It decouples them — the producer doesn't wait for the consumer, and either can scale independently.

- **Message queue** — moves *messages/events* between services (RabbitMQ, SQS, Kafka). "Post published" → analytics service picks it up later.
- **Task queue** — moves *jobs to run* to worker processes (Celery). "Embed this document" → a worker does it.
- **Why it matters:** the queue **absorbs bursts.** 10,000 posts hit at once? They sit in the queue; workers drain them at a steady rate instead of crashing the DB.

## Back pressure — the queue fills faster than it drains

> [!definition] Back pressure
> When work arrives faster than consumers can process it, the queue grows without bound → memory blows up, latency skyrockets. Back pressure = pushing back on the producer to slow down.

Three ways to handle it:
- **Reject / 429** — refuse new work when the queue is full (ties to your **rate limiter** — that *is* back pressure at the edge).
- **Drop / shed load** — throw away low-priority work (old analytics events).
- **Scale consumers** — add more workers to drain faster.

> [!warning] An unbounded queue is a hidden bug
> "Just queue it" isn't free. A queue with no limit and no back pressure just moves the crash from "now" to "later, worse." Always bound the queue and decide what happens when it's full.

## Retries + idempotency (a pair)

- **Retry with backoff + jitter** — a failed job retries after a growing, randomized delay (so 1,000 clients don't all retry at the same instant — a "thundering herd").
- **The catch:** retries mean the same work can run **twice** (the ack got lost but the work succeeded). So every retryable operation must be **idempotent** — running it twice = same result as once.
- **You proved this twice:** the raaaaag `chunk_uid` + `ON CONFLICT DO NOTHING` upsert, and the Shutterabia idempotency guard on publishing.
- Retries + idempotency are a **pair** — you can't safely retry without it.

## REST vs RPC (how services talk)

> [!definition] REST vs RPC
> **REST** = model everything as *resources* + standard HTTP verbs (GET/POST/PUT/DELETE on `/posts/42`).
> **RPC** = call a *function* on a remote server (`publishPost(42)`) as if it were local.

- **REST** — resource-oriented, cacheable, standard, loosely coupled. Best for **public APIs** (your MCP-over-HTTP surface).
- **RPC** (gRPC) — action-oriented, faster (binary), tightly coupled. Best for **internal service-to-service** calls where speed matters.
- **Rule:** REST at the boundary (public), RPC inside (between your own services).

## TCP vs UDP (the transport underneath)

| | TCP | UDP |
|---|---|---|
| Guarantee | reliable, ordered, retransmits lost packets | fire-and-forget, no guarantee |
| Cost | slower (handshake + acks) | fast, low overhead |
| Use for | almost everything — HTTP, DBs, APIs | live video/voice, gaming, DNS where a dropped packet doesn't matter |

- **Rule:** TCP by default (you want correctness). UDP only when **speed beats completeness** and losing a packet is fine.

> [!tip] The through-line
> Async + queues **decouple** producers from consumers so slow/failing work doesn't block the user — but every queue needs **bounds + back pressure**, and every retry needs **idempotency**. Those two pairs are the whole phase.

## Gate 5 (passed 2026-09-16)

**Scenario:** an SMM schedules a post for 6pm; at 6pm the system must call Meta's Graph API to publish it.

### Q1 — sync or async, and where's the queue?
**Async.** The SMM isn't sitting there at 6pm — they scheduled it earlier, publishing is slow, and it can fail. So it goes on a **scheduled/delayed queue** that holds the job until 6pm, then a worker pops it and calls Meta. Nobody's blocked. In the real build, **Temporal** plays this role — the durable timer + worker *is* the queue here.

### Q2 — safe retry after a Meta timeout: the two mechanisms
- **Retry with backoff + jitter** → the **Shutterabia retry-backoff**. Backoff stops you hammering Meta on every failure; **jitter** stops all your scheduled 6pm posts from retrying at the *exact same instant* (thundering herd) when Meta has a blip.
- **Idempotency** → the **Shutterabia idempotency guard**. Meta timed out but *may have actually published* before the timeout — so a blind retry risks a **double-post**. The guard makes the retry a no-op if that post already went out.

> [!tip] The senior framing
> These two aren't optional add-ons — they're what *makes* the retry safe. **Backoff protects the downstream (Meta); idempotency protects the data (no duplicates).** Name both every time you say "we'll retry."

> [!success] Phase 5 done
> Own: sync-vs-async, message vs task queues, back pressure + bounded queues, retries+idempotency as a pair, REST-vs-RPC, TCP-vs-UDP — each mapped to shipped code. **Next: Phase 6 — full designs end-to-end (method → estimate → API → data → high-level → scale, defended under questioning). Start with a primer classic, then pivot to the AI bank the Interview Track wants.**
