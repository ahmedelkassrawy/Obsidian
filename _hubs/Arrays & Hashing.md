---
description: "Hub: every note about Arrays & Hashing"
type: hub
domain: cs
tags:
  - type/hub
  - topic/arrays-and-hashing
---
# Arrays & Hashing

> [!info] Subarray vs subsequence, frequency arrays, index mapping, hash tables. Decent coverage; the LeetCode pattern map lives in 'Array & Hashing Mastery'.
> Part of [[MOC - CS Fundamentals]]. Also try the tag `#topic/arrays-and-hashing`.

## Concepts
- [[Array]] — Defines subarray (contiguous) vs subsequence, gives the n*(n+1)/2 count of subarrays, and shows 2D array declaration.
- [[Frequency Array]] — The frequency-array trick explained in Arabic then in code: index the array by the value itself so counting occurrences is one pass.
- [[Hash Tables]] — Grokking-style intro to hash tables: a hash function maps strings to positions, so lookups are O(1) instead of a scan.
- [[Index Mapping]] — Explains the index-mapping trick for grid problems: keep row_mapping and column_mapping arrays and swap entries there instead of moving the data.

## References & cheat sheets
- [[Array & Hashing Mastery]] — Study guide for LeetCode array/hashing patterns: which problem maps to which pattern, a recommended study order, and short C++/Python templates for two-sum, frequency counting, group-anagrams and longest-consecutive.

## Solved problems
- [[Arrays - Max Subarray (Kadane Practice)]] `raw` — Two small C++ attempts at the maximum-subarray-sum problem, kept as a scratch pad; the only prose is a reminder to trace it on Python Tutor.
- [[Arrays - Max Subarray Sum (CF 518115S)]] `raw` — C++ solution that scans the array once keeping a running best sum (Kadane) to find the largest-sum contiguous subarray.
- [[Arrays - Maximum Subarray Sum (CF 386415I)]] `raw` — C++ solution for the maximum contiguous subarray sum on a Codeforces group problem, using a running sum reset at negatives.
- [[Arrays - Multiplication Of Matrices]] `raw` — C++ solution that multiplies two matrices with the standard triple loop over rows, columns and the shared dimension.
- [[Arrays - Pumbaa]] `raw` — C++ solution to the Pumbaa grid problem, walking a 2D array and applying the per-cell rule; solved with index mapping.
- [[Arrays - Shift Right]] `raw` — C++ solution that rotates an array's elements one position to the right.
- [[Arrays - Shift Zeros]] `raw` — C++ solution that moves every zero in an array to the end while keeping the other elements in order.
- [[Frequency Array - Canvas Frame]] `raw` — C++ solution to the Canvas Frame problem, counting occurrences in a fixed-range frequency array instead of sorting.
- [[Frequency Array - Good Array]] `raw` — C++ solution that uses a frequency count to decide whether the array can be made 'good'.

## Notes to self (from the audit)
- [[Arrays - Max Subarray Sum (CF 518115S)]]: Near-duplicate of 'Maximum Subarray Sum' and 'Max Subarray' in the same folder - same problem, three files.
- [[Arrays - Max Subarray (Kadane Practice)]]: No source link; duplicates 'Max Subarray Sum' / 'Maximum Subarray Sum'.
- [[Arrays - Maximum Subarray Sum (CF 386415I)]]: Duplicate topic of 'Max Subarray Sum' in the same folder.
- [[Arrays - Pumbaa]]: No source link in the note; linked from DSA/Index Mapping.
- [[Arrays - Shift Right]]: No source link in the note.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
