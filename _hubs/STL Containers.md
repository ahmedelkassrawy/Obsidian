---
description: "Hub: every note about STL Containers"
type: hub
domain: cs
tags:
  - type/hub
  - topic/stl-containers
---
# STL Containers

> [!info] vector, map, set, pair, stack, queue, deque, priority_queue. Good reference coverage; Unordered Map is an empty file.
> Part of [[MOC - CS Fundamentals]]. Also try the tag `#topic/stl-containers`.

## References & cheat sheets
- [[Deque]] — std::deque as a vector that can also push and pop at the front, with the member-function demo program.
- [[ECPC Reference Sheet]] — The printable one-file contest sheet: complexity budget per input size, which STL container to reach for, sorting, binary search, two pointers, prefix sums, graphs, DP and number theory - each block written as concept, code, and when to use it.
- [[Lower & Upper Bounds]] — What std::lower_bound and std::upper_bound return on a sorted range, how to turn the iterator into an index, and the edge cases.
- [[Map]] — std::map vs std::unordered_map (sorted by key vs hashed), with basic usage and the two ways to search - count and find.
- [[Pair]] — std::pair: holding two values of different types, reaching them through .first and .second, and the helper functions.
- [[Priority Queue]] — std::priority_queue as a max-heap by default, how to flip it to a min-heap, using it with a custom struct, and the common methods.
- [[Queue]] — std::queue member functions (empty, size, front, back, push, pop) with the FIFO picture.
- [[Sets]] — std::set: unique elements kept sorted ascending by default, how to sort descending with greater<>, and the member functions.
- [[Stack]] — std::stack member functions (empty, size, top, push, pop) with their O(1) costs.
- [[Vectors]] — std::vector as a dynamic array: declaring one, adding, accessing, changing and deleting elements, how it compares to a raw array, and how it grows.
- [[Unordered Map]] `empty` — Empty file - nothing but the filename.

## Solved problems
- [[STL - Dragons]] — C++ solution to the Dragons problem with an Arabic explanation: pair each dragon's level with its energy bonus, sort by level, and fight from the weakest upward.
- [[STL - Min Element In Chunks]] — C++ solution walking the array in chunks of size K and taking min_element of each chunk; the note explains how dereferencing the min_element iterator works.
- [[STL - Double Strings]] `raw` — C++ solution that uses an unordered_set to test whether a string can be split into two identical halves.
- [[STL - Lucky Numbers Using Permutations]] `raw` — C++ solution that generates every lucky number (digits 4 and 7 only) with next_permutation, growing the length until one is at least n.

## Related hubs
[[Dynamic Programming]], [[Graphs BFS & DFS]], [[Math & Number Theory]], [[Binary Search]], [[Heaps & Priority Queues]]

## Notes to self (from the audit)
- [[Unordered Map]]: 0 words. STL/Map.md already covers unordered_map; either fill this or fold it in.
- [[STL - Lucky Numbers Using Permutations]]: No source link in the note.
- [[STL - Min Element In Chunks]]: No source link in the note.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
