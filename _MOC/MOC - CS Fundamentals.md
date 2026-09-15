---
description: "Map of Content for the CS Fundamentals domain"
type: moc
domain: cs
tags:
  - type/moc
  - domain/cs
---
# MOC - CS Fundamentals

This is the competitive-programming and language-fundamentals half of the vault: C++ and Python as languages, the classic data structures and algorithms, and 103 solved contest problems under Problem Solving/Bookmarks.
Strongest area by far is PS Level 1 - the rewritten notes on BFS, DFS, recursion, bitmasks, prefix sums, two pointers, binary search and number theory are long, worked-through and written in plain English, and the ECPC Reference Sheet pulls them into one printable page.
Weakest area is the Bookmarks folder: about 90 of the 103 solved problems are pasted C++ with no write-up and a contest letter for a name, so they are unsearchable and teach nothing on a re-read. They are renamed here, not deleted.
Real gaps (see 'Knowledge Gaps Audit 2026-09-15'): no shortest-path notes beyond a 110-word Dijkstra stub that is factually wrong, no heaps/priority-queue theory beyond the STL API, no string algorithms (KMP, Z, hashing), no geometry, no DSU/MST, and no complexity-analysis note worth the name.
The OOP/ folder is a C# course sitting next to the C++ notes - it teaches OOP fine, just not in the language everything else here uses.

**212 notes** — digested 86, raw 107, stub 16, stale 0, empty 3. Search tip: tag `#domain/cs`.

## Hubs
- [[Complexity Analysis]] (2) — Big-O and the per-input-size time budget. Thin: one 49-word priori/posteriori table plus the budget table in the ECPC sheet. No amortised analysis, no space complexity.
- [[Arrays & Hashing]] (14) — Subarray vs subsequence, frequency arrays, index mapping, hash tables. Decent coverage; the LeetCode pattern map lives in 'Array & Hashing Mastery'.
- [[Prefix Sums]] (4) — 1D and 2D prefix sums and their inverse, the difference array. One of the best-written clusters in the vault. STL/Prefix Sum is the older, weaker copy.
- [[Two Pointers & Sliding Window]] (4) — The three two-pointer families and the fixed/variable window. Strong. Includes the useful negative case - which subarray problems are NOT sliding window.
- [[Binary Search]] (10) — Plain search, binary search on the answer, lower_bound/upper_bound. Well covered in theory and in seven solved problems.
- [[Sorting]] (5) — Selection, insertion and quicksort with their costs. Missing merge sort, counting/radix sort, and custom comparators beyond one struct snippet.
- [[Recursion & Backtracking]] (13) — Call stack order, pick/don't-pick, subsets, permutations, N-Queens, graph colouring. The strongest teaching notes here, backed by eight solved problems.
- [[Dynamic Programming]] (32) — Recursive with memoisation and bottom-up, plus memory reduction. 27 solved DP problems, but nearly all of them are code with no write-up.
- [[Bitmask]] (4) — Bitwise operators, subset enumeration with an integer mask. Solid intro; almost no bitmask DP.
- [[Math & Number Theory]] (8) — Divisors, prime factorisation, the sieve, modular arithmetic, binary exponentiation, GCD. Strong. No combinatorics or CRT.
- [[Graphs BFS & DFS]] (34) — The biggest cluster: BFS and DFS from zero, graph storage trade-offs, grid BFS, multi-source BFS, topological sort, tree diameter, plus 30 solved problems. Missing DSU, MST and bridges/articulation points.
- [[Shortest Paths]] (1) — Weakest hub in this domain. One 110-word Dijkstra stub that wrongly claims cycles break it. No Bellman-Ford, no Floyd-Warshall, no implementation.
- [[Trees & BST]] (1) — One good BST note - traversals, insert, search, delete, complexity. No AVL, no segment tree, no Fenwick.
- [[Linked Lists]] (2) — One long, thorough linked-list note. Nothing on the classic interview manipulations (reverse, cycle detection, merge).
- [[Heaps & Priority Queues]] (1) — Only the std::priority_queue API. No heap internals, no heapify, no k-largest patterns.
- [[String Algorithms]] (10) — Sparse: palindrome checks, anagrams, subsequence checks and seven small solved problems. No KMP, Z-algorithm, tries or string hashing.
- [[Geometry]] (1) — Nearly empty - one rectangle-overlap solution. No points/vectors, cross product, or convex hull.
- [[STL Containers]] (15) — vector, map, set, pair, stack, queue, deque, priority_queue. Good reference coverage; Unordered Map is an empty file.
- [[C++ Language]] (26) — Scope and linkage, references, pointers, templates, type conversion, overloading, headers, namespaces. Reasonable; pointers and strings are still snippet-only stubs.
- [[OOP]] (11) — Classes, inheritance, polymorphism, static members, enums, boxing. Split three ways - C#, C++ and Python notes all teaching the same ideas. Pick a canonical one.
- [[Python Language]] (17) — The best-maintained language cluster: decorators, data modeling, JSON/serialization, Protocol vs ABC, Pydantic, pytest. Missing generators/iterators, async, and typing beyond Pydantic.
- [[TypeScript & JavaScript]] (2) — Two notes only - the fundamentals course notes and how the JS engine works. No DOM, no async/promises, no TypeScript at all.
- [[Numpy]] (7) — Array basics only, picked up inside the pandas notes. There is no dedicated numpy note yet.

Gaps: [[Knowledge Gaps Audit 2026-09-15]]. Back to [[00 Home]].
