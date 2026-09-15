---
description: "Hub: every note about Recursion & Backtracking"
type: hub
domain: cs
tags:
  - type/hub
  - topic/recursion-and-backtracking
---
# Recursion & Backtracking

> [!info] Call stack order, pick/don't-pick, subsets, permutations, N-Queens, graph colouring. The strongest teaching notes here, backed by eight solved problems.
> Part of [[MOC - CS Fundamentals]]. Also try the tag `#topic/recursion-and-backtracking`.

## Concepts
- [[Backtracking]] — The five backtracking templates - subset generation, permutations, combinations, N-Queens and graph colouring - and why the for-loop pattern needs only one recursive call.
- [[Quicksort]] — Quicksort explained through divide-and-conquer: find the base case, shrink the problem toward it, partition around a pivot.
- [[Recursion]] — Recursion from the ground up in Python: what happens with and without a base case, how the call stack drives the order of execution, and Collatz-style conditional recursion.
- [[Recursion Notes]] — Recursion from the ground up: how the call stack sets the order of execution, printing before vs after the call, accumulate-on-return, memoisation, and the pick/don't-pick template.

## Solved problems
- [[Backtracking - Apple Division]] `raw` — C++ recursive pick/don't-pick solution that splits apple weights into two groups with the smallest possible difference.
- [[Backtracking - Creating Expression]] `raw` — C++ recursive solution that tries every + / - placement between numbers to build the target expression.
- [[Backtracking - Creating Strings]] `raw` — C++ recursive solution that generates every distinct permutation of a string, using a set to drop duplicates.
- [[Backtracking - Knapsack]] `raw` — C++ recursive 0/1 knapsack: at each item take the better of including it (if it fits) or skipping it.
- [[Backtracking - Knapsack Recursive]] `raw` — C++ recursive 0/1 knapsack with the base case on capacity or items running out.
- [[Backtracking - Queen Gambit]] `raw` — C++ N-Queens style backtracking solution that places queens row by row and undoes a placement when it conflicts.
- [[Backtracking - SkillUP]] `raw` — C++ recursive solution for the minimum-cost book selection: try taking or skipping each book until every skill level meets the requirement.
- [[Backtracking - Unnamed Practice Problem]] `raw` — Unlabelled C++ backtracking attempt - includes and a recursive skeleton, with no problem statement, link or comments.
- [[Recursion - Reach Value (CF 223339W)]] `raw` — C++ recursive solution to a Codeforces group problem: from a starting number, repeatedly branch and check whether the target value can be reached.

## Related hubs
[[Sorting]]

## Notes to self (from the audit)
- [[Backtracking - Apple Division]]: Old filename had a typo ('Backtarcking').
- [[Backtracking - Knapsack]]: Same problem as 'Knapsack' in this folder - two copies of the recursive knapsack.
- [[Backtracking - Knapsack Recursive]]: Duplicate-of 'Knapsack Backtracking' in the same folder.
- [[Backtracking - Unnamed Practice Problem]]: No source link and no problem name anywhere in the note; needs identifying or deleting.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
