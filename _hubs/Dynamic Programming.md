---
description: "Hub: every note about Dynamic Programming"
type: hub
domain: cs
tags:
  - type/hub
  - topic/dynamic-programming
---
# Dynamic Programming

> [!info] Recursive with memoisation and bottom-up, plus memory reduction. 27 solved DP problems, but nearly all of them are code with no write-up.
> Part of [[MOC - CS Fundamentals]]. Also try the tag `#topic/dynamic-programming`.

## Concepts
- [[DP Iterative]] — Bottom-up DP: filling the table in order instead of recursing, and cutting the table down to one or two rows (memory reduction).
- [[DP Recursive Patterns]] — Recursive DP with memoisation, worked through Fibonacci, minimum path sum in a grid, counting paths under a sum constraint, knapsack, and LCS with reconstruction.
- [[Dynamic Programming]] — Grokking-style intro to DP through the knapsack grid, and why the fractional version cannot be done with the DP table (that one is greedy).
- [[Dynamic_Programming_Notes]] `empty` — Empty file - nothing but the filename.

## References & cheat sheets
- [[ECPC Reference Sheet]] — The printable one-file contest sheet: complexity budget per input size, which STL container to reach for, sorting, binary search, two pointers, prefix sums, graphs, DP and number theory - each block written as concept, code, and when to use it.

## Solved problems
- [[DP - Vjudge 694272 T]] — Recursive C++ DP for problem T, with a short note in Arabic explaining that the naive direction TLEs so the recurrence is flipped to go from the fixed value to the variable one.
- [[DP - Vjudge 694272 E]] `raw` — Bare recursive C++ DP with memoisation for problem E of the recursive-DP sheet.
- [[DP - Vjudge 694272 J (Gym And Contest Days)]] `raw` — Recursive C++ DP over days where each day is one of four states (gym open/closed, contest held/not) and the transition picks the best activity.
- [[DP - Vjudge 694272 K]] `raw` — Bare recursive C++ DP with memoisation for problem K; only a 'base case' comment survives.
- [[DP - Vjudge 694272 L]] `raw` — Recursive C++ DP for problem L with counting done under a modulus; a comment notes the modulus trick was taken from ChatGPT and other notes.
- [[DP - Vjudge 694272 M]] `raw` — Bare recursive C++ DP with memoisation for problem M of the recursive-DP sheet.
- [[DP - Vjudge 694272 N]] `raw` — Recursive C++ DP for problem N that alternates between odd and even positions at each step.
- [[DP - Vjudge 694272 O]] `raw` — Bare recursive C++ DP with memoisation for problem O of the recursive-DP sheet.
- [[DP - Vjudge 694272 P]] `raw` — Recursive C++ DP for problem P, built over a graph/queue input.
- [[DP - Vjudge 694272 R]] `raw` — Recursive C++ DP for problem R where the transition satisfies a removal condition.
- [[DP - Vjudge 694272 S (Counting Valid Arrays)]] `raw` — Recursive C++ DP that counts valid arrays: at each index the value may stay, go one up or one down, and fixed values short-circuit the branch.
- [[DP - Vjudge 694272 U]] `raw` — Recursive C++ DP with two limits; the comment explains the base case when either limit hits zero.
- [[DP - Vjudge 694272 V]] `raw` — Recursive C++ DP for problem V, memoised with an unordered_map because the state space is sparse.
- [[DP - Vjudge 694272 W]] `raw` — Bare recursive C++ DP for problem W, memoised with an unordered_map.
- [[DP - Vjudge 694272 X]] `raw` — Recursive C++ DP for problem X that loops for the best value then continues from there; only two scrappy comments remain.
- [[DP - Vjudge 694272 Z (Bracket Sequences)]] `raw` — Recursive C++ DP over bracket sequences: track the running open-bracket balance, and a balance of zero means one group has closed and a new one starts.
- [[DP Iterative - Vjudge 696069 B]] `raw` — Bottom-up C++ DP table for problem B of the iterative-DP sheet.
- [[DP Iterative - Vjudge 696069 C]] `raw` — Bottom-up C++ DP for problem C where each state looks ahead to i+1 and i+2 (the stairs/jump shape).
- [[DP Iterative - Vjudge 696069 D]] `raw` — Bottom-up C++ DP for problem D, minimising over the table with INT_MAX as the unreachable marker.
- [[DP Iterative - Vjudge 696069 E]] `raw` — Bottom-up C++ DP table for problem E of the iterative-DP sheet.
- [[DP Iterative - Vjudge 696069 K (Coin Combinations)]] `raw` — Bottom-up coin-change count: loop over coins on the outside so each combination is counted once and ordered pairs are not double counted.
- [[DP Iterative - Vjudge 696069 N]] `raw` — Bottom-up C++ DP for problem N, with a step that removes the zero case.
- [[DP Iterative - Vjudge 696069 P]] `raw` — Bottom-up C++ DP for problem P, built on prefix accumulation via <numeric>.
- [[DP Iterative - Vjudge 696069 U (Good And Bad Keys)]] `raw` — Bottom-up C++ DP over chests: a good key costs k, a bad key halves the reward, so dp[i][j] compares both choices.
- [[DP Iterative - Vjudge 696069 W]] `raw` — Bottom-up C++ DP table for problem W of the iterative-DP sheet.
- [[DP Iterative - Vjudge 696069 X (Knapsack)]] `raw` — Bottom-up knapsack over cows where the capacity loop runs in reverse so each item is used at most once.
- [[DP Iterative - Vjudge 696069 Y]] `raw` — Bottom-up C++ DP for problem Y that also needs modular exponentiation (a^b % mod) to build the table.

## Related hubs
[[STL Containers]], [[Graphs BFS & DFS]], [[Math & Number Theory]]

## Notes to self (from the audit)
- [[Dynamic_Programming_Notes]]: 0 words. Either fill it or delete it; DSA/Dynamic Programming.md and PS Level 1/DP.md already cover the topic.
- [[DP - Vjudge 694272 S (Counting Valid Arrays)]]: No source link in the note - identified from the code comments.
- [[DP - Vjudge 694272 X]]: No source link in the note.
- [[DP Iterative - Vjudge 696069 K (Coin Combinations)]]: Filename says J but the link inside points at problem K of vjudge 696069.
- [[DP Iterative - Vjudge 696069 U (Good And Bad Keys)]]: No source link in the note - identified from the code comments.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
