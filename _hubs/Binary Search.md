---
description: "Hub: every note about Binary Search"
type: hub
domain: cs
tags:
  - type/hub
  - topic/binary-search
---
# Binary Search

> [!info] Plain search, binary search on the answer, lower_bound/upper_bound. Well covered in theory and in seven solved problems.
> Part of [[MOC - CS Fundamentals]]. Also try the tag `#topic/binary-search`.

## Concepts
- [[Binary Search]] — Grokking-style intro to binary search: why the list must be sorted, what it returns, and the log n step count against linear search.
- [[Binary Search]] — Binary search from zero: the guess-the-number idea, a hand-traced example, the exists-or-not version, then lower_bound and upper_bound.

## References & cheat sheets
- [[Lower & Upper Bounds]] — What std::lower_bound and std::upper_bound return on a sorted range, how to turn the iterator into an index, and the edge cases.

## Solved problems
- [[Binary Search - Another Pair Problem]] `raw` — C++ solution that counts, for each index i, how many earlier indices satisfy the condition by binary searching a sorted list of valid indices.
- [[Binary Search - Another Pair Problem (Duplicate)]] `raw` — Second copy of the Another Pair Problem solution - counts valid earlier indices with a binary search.
- [[Binary Search - Line Segments]] `raw` — C++ binary search on the answer k: for a candidate k, check whether all segments still share a valid range.
- [[Binary Search - Machines]] `raw` — C++ binary search on the answer for the machines problem from the binary-search sheet.
- [[Binary Search - Magic Powder 2]] `raw` — C++ binary search on the number of cookies, with a check function that works out how much magic powder the target would need.
- [[Binary Search - Pirate Ships]] `raw` — C++ solution that marks shot positions, counts the still-valid ship segments, and binary searches for the first shot that makes the board invalid.
- [[Binary Search - Renting Bikes]] `raw` — C++ binary search on how many boys can rent: sort personal money descending and bike prices ascending, then compute the shared budget needed.

## Related hubs
[[STL Containers]]

## Notes to self (from the audit)
- [[Binary Search - Another Pair Problem]]: Byte-for-byte the same approach as 'problemo' in this folder (same vjudge problem O).
- [[Binary Search - Pirate Ships]]: No source link in the note.
- [[Binary Search - Another Pair Problem (Duplicate)]]: Duplicate-of 'Another Pair Problem - Binary Search' (same vjudge 661083 problem O, same code).

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
