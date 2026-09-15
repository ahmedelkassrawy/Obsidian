---
description: "Grokking-style intro: Dijkstra answers the shortest path on a weighted graph, where BFS only counts hops, and it breaks on negative-weight edges."
domain: cs
type: concept
status: stub
tags:
  - domain/cs
  - type/concept
  - status/stub
  - topic/shortest-paths
aliases:
  - "Dijkstra"
  - "weighted shortest path"
hubs:
  - "[[Shortest Paths]]"
---
- lets you answer “What’s the shortest path to X?” for weighted graphs.
- You learn about cycles in graphs, where Dijkstra’s algorithm doesn’t work.

- BFS will find you the path with the fewest segments (the first graph shown here). What if you want the fastest path instead (the second graph)? You can do that fastest with a different algorithm called Dijkstra’s algorithm.
![[Pasted image 20240506173105.png]]
![[Pasted image 20240506173238.png]]

- Dijkstra’s algorithm only works on graphs with no cycles, or on graphs with a positive weight cycle.
- You can’t use Dijkstra’s algorithm if you have negative-weight edges. Negative-weight edges break the algorithm