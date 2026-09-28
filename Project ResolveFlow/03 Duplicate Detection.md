---
date: 2026-09-28
type: project-note
project: resolveflow
status: active
tags:
  - domain/ai-eng
  - type/project-note
  - resolveflow
description: "Deterministic duplicate-charge detection rule and how the detector works."
hubs:
  - "[[00 ResolveFlow Index]]"
---

# 03 Duplicate Detection

> Part of [[00 ResolveFlow Index]]. Previous: [[02 Project Setup and Domain Models]] · Next: [[04 Mock Billing Gateway and Idempotency]]

## Duplicate-detection rule

Two transactions are potential duplicates when they:

- Have different transaction IDs.
- Are both completed.
- Belong to the same tenant and customer.
- Have the same order ID, amount, and currency.
- Occur within the configured time window.

The detector sorts by `charged_at`, making the earlier transaction the original and the later transaction the duplicate. Normal non-matches return `None`; they are not exceptional failures.

## Build notes

The duplicate detection system 
it recieves
- a sequence of transactions
- a time window supplied by the caller

it then:
1. Sort transactions chronologically 
2. compares each charge with later cahrges
3. requires matching tenant and customer and order and amount and currency
4. checks whether the charges occurred within the allowed window
5. returns the first mathcing pair as DuplicatedCHargedFinding
6. Returns `None` if no duplicate exists.

The graph currently supplies a five-minute window, meaning the general duplicate detector does not own that policy—the orchestration layer does.
