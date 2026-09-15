---
tags: [backend, system-design, distributed-systems, cap, consistency, availability]
domain: backend
type: lesson-note
status: digested
source: System Design Primer — Phase 1 (Scalability & Availability); Kassra growth-track session 2026-09-16
---
# Scalability & Availability

The foundations layer: what "scale" really means, the CAP trade-off, how fresh reads are, and how uptime is measured.

## 1. Performance vs Scalability

> [!definition] Performance vs Scalability
> **Performance** = one request is fast (low latency now, with few users).
> **Scalability** = it *stays* fast as load grows.

The test:
- Adding **users** makes each request slower → a **performance** problem.
- Adding **servers** fixes it → the system is **scalable**.
- Adding servers *doesn't* fix it → you hit a shared bottleneck (one DB, one lock).

## 2. Latency vs Throughput

> [!definition] Latency vs Throughput
> **Latency** = time for one request (ms).
> **Throughput** = requests handled per second.

- You want **acceptable latency at high throughput**.
- Batching trades one for the other: the raaaaag **50-chunk embed batch** raised throughput (fewer Cohere calls) at the cost of a little latency per chunk.
- That trade was correct because ingestion is **background work** — nobody's waiting on a single chunk.

## 3. CAP

When your data lives on **more than one machine** and the network between them breaks (a **partition** — not "if", *when*), you can keep only **two** of these three:

| Letter | Means |
|---|---|
| **C** — Consistency | every read sees the latest write |
| **A** — Availability | every request gets an answer (maybe stale) |
| **P** — Partition tolerance | the system keeps working when the network splits |

> [!warning] P is not optional
> On a real network, links *do* drop. So you can't opt out of partition tolerance — the real choice is only **C vs A during a partition**.

### The single decision that defines the choice

- Your data lives on two machines, **Node A** and **Node B**, that copy writes to each other.
- The cable between them breaks. Both are alive, but they can't talk.
- A user writes to **A**. Now **B** doesn't know about that write.
- Someone reads from **B**. **What does B do?** That one decision is the whole trade-off.

### CP — B refuses

B thinks: *"I might be stale. I won't guess."* So B returns an **error** until the cable is back and it's caught up.

- You lose **availability** (that read failed) to protect **consistency** (nobody ever sees old data).
- Right when being wrong is expensive:
  - **Bank balance** — you have $100. You withdraw $100 from A. If B still says "$100 available" and lets a second withdrawal through → you spent $200 you don't have. Better to error: "try again."
  - **Inventory** — 1 concert ticket left. A sells it. If B doesn't know and sells it too → two people, one seat. Better to refuse than oversell.

### AP — B answers anyway

B thinks: *"I'll give you what I've got. It might be a few seconds old. I'll sync up when the cable's back."*

- You keep **availability** (every read succeeds) and give up **consistency** for a short window (some reads are stale until the link is back).
- Right when stale-for-a-moment is harmless:
  - **Social feed** — your friend posted; the cable's down; you don't see it for 5 seconds. Nobody's hurt. Far better than the whole app showing an error.
  - **Analytics dashboard** — the view count says 1,000 but it's really 1,003. Fine. You'd rather the dashboard *load* than throw an error because one counter is behind.

> [!tip] The one-line rule
> During a network split, does serving *slightly old data* cause real damage?
> **Yes → CP** (refuse, stay correct) — money or anything that can't be undone and must be real-time.
> **No → AP** (answer, stay up) — availability is the key; being perfectly fresh isn't important.

**Tie to real work:** the Shutterabia D1 dashboard mirror is **AP** — a post shows "scheduled" for 3 seconds after it really published. Harmless → serve it, stay up.

### The trick: CAP needs replication first

**raaaaag on *one* Postgres — CP or AP?**

> [!note] Neither
> CAP only exists when data is on **more than one machine** — you need at least two copies for a partition to split them. One node = nothing to partition = **CAP doesn't apply at all**. It's neither CP nor AP.

The lesson: **don't reach for CAP until data is replicated.** The moment you add a read replica to that Postgres — which is exactly the URL-shortener scaling fix — *then* CAP wakes up and you must choose. (pgvector reads would be **AP**: a slightly stale search result is fine.)

## 4. Three consistency patterns

All three answer one question: **after a write lands, when do reads see it?**
Picture one **primary** DB (takes writes) copying to **replicas** (serve reads).

### Strong consistency
A read *always* sees the latest write, immediately.
- **How:** the write isn't "done" until every replica confirms it (or all reads go to the primary). The read waits if needed.
- **Cost:** latency — you pay the round-trip to sync before anyone can read. During a partition this becomes CP (refuse rather than serve stale).
- **Use when stale = damage:** billing balance, quota counter, inventory.

### Eventual consistency
Replicas catch up "soon" (usually milliseconds). A read right after a write *might* be stale.
- **How:** write returns as soon as the **primary** has it; replicas sync in the background.
- **Cost:** a brief stale window. Cheap, fast, highly available (AP).
- **Use when stale-for-a-moment is harmless:** the Shutterabia D1 dashboard mirror, view counts, search results.

### Read-your-writes consistency
The middle ground: **you** always see **your own** writes instantly; *other* people may lag.
- **The problem it fixes:** you edit your bio, hit save, the page reloads from a stale replica → your change vanished → you panic and save again. Bad UX even though the data was fine.
- **How:** route *your* reads to the primary (or the replica that has your write) for a short window after you write; everyone else reads normal replicas.
- It's eventual consistency **plus a personal guarantee**. Cheap win, big UX improvement.
- **Shutterabia fit:** SMM approves a draft → their next dashboard load must show it "approved" even if a colleague's screen lags a second.

> [!abstract] The ladder
> - **strong** = everyone fresh always (slow)
> - **eventual** = everyone fresh soon (fast, stale window)
> - **read-your-writes** = *you* fresh now, others soon (cheap fix for the "my edit disappeared" bug)

## 5. The nines (availability)

> [!definition] Availability
> The **% of time the system answers**. Measured in "nines" = how many 9s are in that percentage.

What matters is the **downtime that percentage allows:**

| Availability | Name | Downtime / year | Downtime / day |
|---|---|---|---|
| 99% | two nines | ~3.65 days | ~14 min |
| 99.9% | three nines | ~8.75 hours | ~86 sec |
| 99.99% | four nines | ~52 min | ~8.6 sec |
| 99.999% | five nines | ~5.25 min | ~0.86 sec |

- Each extra nine = **~10× less downtime** — and usually a lot more money (redundancy, failover, on-call). You don't chase nines for free.

### Series costs nines; parallel buys them back

**Series (dependencies) — multiply, and it gets *worse*.** If a request must pass through two things in a row, each 99.9%:

```text
0.999 × 0.999 = 0.998  →  99.8%   (worse than either piece alone)
```

A chain is only as available as the **product** of its links. Every hop (LB → app → DB → external API) drags the number down. Shutterabia depends on Meta's Graph API — **your uptime can't exceed theirs** on the publish path.

**Parallel (redundancy) — raises it.** Two components doing the same job, either one is enough; you're down only if **both** fail:

```text
1 − (0.01 × 0.01) = 0.9999  →  99.99%   (two 99% servers behind a load balancer)
```

> [!tip] Design takeaway
> **Series (dependencies) costs you nines; parallel (redundancy) buys them back.** A resilient system minimizes hard series dependencies and adds parallel redundancy at the weak points.

## Gate check (passed 2026-09-16)

1. **Consistency pattern** — SMM sees their own approval instantly, a colleague can lag → **read-your-writes** ✅
2. **Nines, series** — publish path LB(99.99%) → app(99.9%) → Meta(99.9%) → best ≈ **99.8%**; weak link = the **external Meta Graph API** ✅ (concept right; state the number + name the external link)
3. **Scalability + CAP** — a read replica fixes a **scalability** bottleneck; CAP "wakes up" with 2+ connected copies; stale search reads → **AP** ✅ (commit the verdict, don't just describe both)

> [!success] Phase 1 done
> Own: performance-vs-scalability, latency-vs-throughput, CAP (+ the "needs replication first" trap), the 3 consistency patterns, and the nines. **Next: Phase 2 — the building blocks (DNS, CDN, load balancers, reverse proxy, app layer).**
