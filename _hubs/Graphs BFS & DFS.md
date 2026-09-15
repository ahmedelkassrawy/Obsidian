---
description: "Hub: every note about Graphs BFS & DFS"
type: hub
domain: cs
tags:
  - type/hub
  - topic/graphs-bfs-and-dfs
---
# Graphs BFS & DFS

> [!info] The biggest cluster: BFS and DFS from zero, graph storage trade-offs, grid BFS, multi-source BFS, topological sort, tree diameter, plus 30 solved problems. Missing DSU, MST and bridges/articulation points.
> Part of [[MOC - CS Fundamentals]]. Also try the tag `#topic/graphs-bfs-and-dfs`.

## Concepts
- [[BFS, Graph Applications]] — BFS explained with the ripple-in-a-pond picture: the queue/visited/dist trio, reconstructing the actual path with a parent array, grid BFS and multi-source BFS.
- [[Breadth First Search (BFS)]] — Grokking-style intro to BFS: it finds the shortest path in hops, with the checkers-AI and spell-checker examples.
- [[Graphs, DFS]] — Graphs from zero: directed vs undirected edges, the three ways to store a graph (edge list, matrix, adjacency list) with their trade-offs, then DFS and what it powers.

## References & cheat sheets
- [[ECPC Reference Sheet]] — The printable one-file contest sheet: complexity budget per input size, which STL container to reach for, sorting, binary search, two pointers, prefix sums, graphs, DP and number theory - each block written as concept, code, and when to use it.

## Solved problems
- [[BFS - Vjudge 692604 U (K Special Nodes)]] — The one BFS bookmark with a real write-up: restates the input (n nodes, m edges, k special nodes), explains running BFS from each special node to fill dist[k][i], and then how the k smallest distances are combined.
- [[Graph DFS - Vjudge 690295 V (Prime Labels On A Tree)]] — C++ tree solution with an Arabic write-up of the reasoning: the tree has to stay linear so that assigning prime numbers keeps every node's sum correct.
- [[BFS - Topological Sort (Vjudge 692604 B)]] `raw` — C++ Kahn's-algorithm solution: push every node with indegree 0 into a queue, peel them off in order, and report a cycle when the topological order is short.
- [[BFS - Vjudge 692604 G]] `raw` — Bare C++ BFS solution for problem G of the BFS & Graph Applications sheet - queue, visited array and level counting, no explanation.
- [[BFS - Vjudge 692604 H]] `raw` — Bare C++ BFS solution for problem H of the BFS & Graph Applications sheet, using a queue plus a stack helper.
- [[BFS - Vjudge 692604 I]] `raw` — C++ BFS that builds a parent for every node, attaching orphan nodes to the boss node, then prints each node's parent.
- [[BFS - Vjudge 692604 J]] `raw` — Bare C++ BFS solution for problem J of the BFS & Graph Applications sheet - shortest hop count over an adjacency list.
- [[BFS - Vjudge 692604 L]] `raw` — Bare C++ BFS solution for problem L of the BFS & Graph Applications sheet, no explanation kept.
- [[BFS - Vjudge 692604 M]] `raw` — C++ BFS solution for problem M; the one comment records the bug that the neighbour loop must sit inside the while loop.
- [[BFS - Vjudge 692604 N]] `raw` — C++ grid BFS for problem N - reads a character grid and spreads over it level by level.
- [[BFS - Vjudge 692604 P]] `raw` — Bare C++ BFS solution for problem P of the BFS & Graph Applications sheet.
- [[BFS - Vjudge 692604 Q]] `raw` — Bare C++ BFS solution for problem Q of the BFS & Graph Applications sheet.
- [[BFS - Vjudge 692604 S (BFS With State)]] `raw` — C++ BFS over a 3D distance array where the third dimension is a door state (open/closed) - the state-augmented BFS pattern.
- [[BFS - Vjudge 692604 T]] `raw` — C++ multi-source BFS: build the adjacency list from the rules, seed the queue with several starting nodes, then print each node's distance.
- [[BFS - Vjudge 692604 V]] `raw` — Bare C++ BFS solution for problem V of the BFS & Graph Applications sheet.
- [[BFS - Vjudge 692604 W (0-1 BFS)]] `raw` — C++ solution for problem W using a deque instead of a queue - the 0-1 BFS pattern for edges of weight 0 or 1.
- [[Graph DFS - Galactic Bonding]] `raw` — C++ DFS that groups stars into constellations: two stars are joined when their squared Euclidean distance is within the limit, then DFS counts the connected components.
- [[Graph DFS - Gold Search]] `raw` — C++ DFS over a grid that collects gold and stops at traps, exploring all four directions from the start cell.
- [[Graph DFS - Maze]] `raw` — C++ DFS through a character maze, walking from the start cell until the exit is reached.
- [[Graph DFS - Sum Friends]] `raw` — C++ DFS over friendship groups that sums each connected component and compares the totals.
- [[Graph DFS - Vjudge 690295 E (Grid Flood Fill)]] `raw` — C++ grid DFS with the four direction offsets spelled out in Arabic comments, skipping borders, walls and already-visited cells.
- [[Graph DFS - Vjudge 690295 G]] `raw` — Bare C++ DFS solution for problem G of the Intro To Graph & DFS sheet.
- [[Graph DFS - Vjudge 690295 J]] `raw` — C++ DFS on a tree that works upward from the leaves.
- [[Graph DFS - Vjudge 690295 K (Is It A Tree)]] `raw` — C++ solution that decides whether a directed graph is a tree: exactly one node with in-degree 0, then DFS to confirm it is connected and acyclic.
- [[Graph DFS - Vjudge 690295 O]] `raw` — Bare C++ DFS solution for problem O of the Intro To Graph & DFS sheet.
- [[Graph DFS - Vjudge 690295 P (One Component Check)]] `raw` — C++ DFS that counts connected components and answers yes when everything collapses into a single component / tree.
- [[Graph DFS - Vjudge 690295 R (Complete Components)]] `raw` — C++ DFS that counts the edges and vertices inside each connected component and calls the component complete when the counts match the clique formula.
- [[Graph DFS - Vjudge 690295 S (Waking Areas)]] `raw` — C++ spreading solution: an asleep area wakes once it has at least three awake neighbours, repeated until nothing changes.
- [[Graph DFS - Vjudge 690295 T (Tree Diameter)]] `raw` — C++ double-DFS that finds the tree diameter: DFS from node 0 to the farthest node, then DFS again from there for the longest path.
- [[Graph DFS - Vjudge 690295 U]] `raw` — Bare C++ DFS solution for problem U, using hash maps and sets for the adjacency.

## Related hubs
[[STL Containers]], [[Dynamic Programming]], [[Math & Number Theory]]

## Notes to self (from the audit)
- [[Graph DFS - Vjudge 690295 E (Grid Flood Fill)]]: No source link in the note - matched to the Intro To Graph & DFS sheet by its siblings.
- [[Graph DFS - Vjudge 690295 R (Complete Components)]]: Old filename had a typo ('MAnsoura').
- [[Graph DFS - Vjudge 690295 V (Prime Labels On A Tree)]]: The link points at the submission status page, not the problem page.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
