---
description: "Hub: every note about Bitmask"
type: hub
domain: cs
tags:
  - type/hub
  - topic/bitmask
---
# Bitmask

> [!info] Bitwise operators, subset enumeration with an integer mask. Solid intro; almost no bitmask DP.
> Part of [[MOC - CS Fundamentals]]. Also try the tag `#topic/bitmask`.

## Concepts
- [[Bitmask - Subset Enumeration]] — Explains the subset-enumeration loop: an integer bitmask stands for a subset, bit j set means element j is included, so looping 0..2^n-1 walks every subset.
- [[Bitmasks]] — Bits explained as rows of light switches: converting to binary, every bitwise operator, shifting, the long-long safety belt, and using a mask to stand for a subset.

## References & cheat sheets
- [[Bitwise Operators]] — Table of the C++ bitwise operators (<<, >>, ~, &, |, ^) with what each does to the bits, plus short examples.
- [[Bit Prefix Sums (Archived)]] `raw` — Archived code dump: per-bit prefix sums over an array (prefixBits[64][n+1]) for answering bit-count queries on ranges.

## Notes to self (from the audit)
- [[Bit Prefix Sums (Archived)]]: Author already marked it _archived_ and it is superseded by PS Level 1/Bitmasks.md - code only, no prose.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
