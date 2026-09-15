---
description: "Hub: every note about Operating Systems"
type: hub
domain: backend
tags:
  - type/hub
  - topic/operating-systems
---
# Operating Systems

> [!info] Two OSTEP chapters and a stack-vs-heap stub. Missing: scheduling, virtual memory and everything after OSTEP chapter 2.
> Part of [[MOC - Backend]]. Also try the tag `#topic/operating-systems`.

## Concepts
- [[Stack vs Heap]] `stub` — Bullet notes on what lives on the stack vs the heap and what happens to the stack on each function call.

## How-tos & recipes
- [[laptop-startup-cleanup-2026-08-28]] — What was disabled at Windows startup on the Dell laptop to cut RAM pressure, why it was RAM and not failing hardware, and the exact steps to undo each change.

## Book notes
- [[OSTEP - Virtualization, Concurrency and Persistence]] — OSTEP opening chapter: the OS as a virtualizer of CPU and memory, system calls, concurrency, persistence and the OS design goals.
- [[OSTEP - Processes and Time Sharing]] `stub` — Short bullet list on CPU virtualization, time sharing and the illusion of concurrency created by process switching.

## Interviews
- [[InstaBug Assessment]] — The InstaBug written assessment with worked answers: ULID vs UUID as a primary key, race conditions and locks, webhooks, HTTP auth headers, statelessness, and page tables.

## Related hubs
[[Concurrency & Async]], [[C++ Language]], [[Interviews]], [[Auth & Security]]

## Notes to self (from the audit)
- [[OSTEP - Processes and Time Sharing]]: Stub - expand with process states, the process API and context switching.
- [[Stack vs Heap]]: Stub - no allocation cost or fragmentation discussion yet.
- [[laptop-startup-cleanup-2026-08-28]]: Only Windows/local-machine note in the vault, so it is tagged under Operating Systems rather than getting its own hub. If more Windows notes arrive, split out a "Windows & Local Machine" hub.
- [[InstaBug Assessment]]: Good interview material but the answers are generic; add one line per question on how you would say it out loud.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
