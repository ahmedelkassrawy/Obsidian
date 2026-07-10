# Memcached In-Memory Database Architecture

## Overview
Memcached is an in-memory key-value store, originally written in Perl and later rewritten in C. It is widely used by companies like Facebook, Netflix, and Wikipedia due to its simplicity. Unlike more complex systems, Memcached focuses solely on being an in-memory key-value store without features like persistence or rich data types. Even distribution across servers is handled by the client, not the server.

This note dives deep into Memcached's architecture, emphasizing its design choices for simplicity. We'll cover memory management, threading, LRU eviction, reads/writes, collisions, and distributed caching. The goal is to provide a study-friendly breakdown, including explanations, diagrams (described in text), and opinions on design trade-offs.

### Key Principles
- **Simplicity as a Core Feature**: Memcached avoids "fancy" additions to remain transparent and easy to reason about.
- **Caching as a Last Resort**: Before using Memcached, optimize underlying issues (e.g., database queries, RPC calls). Caching should not be a "duct-tape" solution.
  - For slow database queries: Analyze execution plans, add indexes, rewrite queries, or add filters to reduce search space.
  - For chatty RPCs: Investigate library/framework misuse and eliminate unnecessary calls.
- **Limitations as Features**: No persistence means it's transient; always design applications assuming cache misses.

## What is Memcached?
Memcached is a key-value store designed for caching. It stores data in memory for fast access, typically for expensive database queries or HTTP responses.

- **Key Constraints**:
  - Keys: Strings, up to 250 characters.
  - Values: Any type, up to 1 MB by default.
  - TTL (Time to Live): Expiration for keys, but not guaranteed due to LRU eviction.
- **Use Case Advice**: Ideal for transient caching. Do not use for durable storage. Always handle cache misses gracefully ("Plan for the worst, hope for the best").

## Memory Management
Memcached's memory management is designed to prevent fragmentation, a common issue where scattered unused memory gaps make allocation inefficient.

### Fragmentation Problem
- In typical programs, allocations (e.g., arrays, strings) create random gaps in memory.
- This leads to **external fragmentation**: Enough total memory exists, but no contiguous block is large enough for new items.
- OS uses virtual memory to map scattered physical pages, but this incurs performance costs (e.g., multiple I/Os, mapping overhead).

![[Pasted image 20251006013108.png]]

### Memcached's Solution: Slab Allocation
- Memcached pre-allocates memory in 1 MB pages (hence the 1 MB value limit).
- Pages are divided into fixed-size **chunks** based on **slab classes**.
  - Slab classes define chunk sizes, growing exponentially (e.g., Slab Class 1: 72 bytes; Slab Class 43: 1 MB).
- Items (key + value + metadata) are assigned to the smallest slab class that fits them.
  - Example: A 40-byte item fits in a 72-byte chunk (Slab Class 1), wasting 32 bytes.
  - Clients should optimize item sizes to minimize waste.

![[Pasted image 20251006013118.png]]

- **Chunk Calculation**:
  - Slab Class 1 (72 bytes): 1 MB page holds ~14,563 chunks (1,048,576 / 72 ≈ 14,563).
  - Slab Class 43 (1 MB): 1 chunk per page.
- **Allocation Process**:
  - For a new item: Find the appropriate slab class.
  - If a page in that class has free chunks, use one.
  - If full, allocate a new 1 MB page for that slab class.
- Benefits: Avoids OS-level fragmentation by managing memory internally. Items are contiguous within pages.

![[Pasted image 20251006013129.png]]

- **Handling Full Slabs**:
  - If all pages for a slab class are full, allocate a new page.
  
![[Pasted image 20251006013137.png]]

- **Opinion**: This pre-allocation keeps things simple and performant, but clients must be aware of waste in chunks for efficiency.

## Threading
Memcached handles network connections efficiently, supporting TCP (default) and UDP (disabled by default due to 2018 reflection attacks).

### Listener and Worker Threads
- **Listener Thread**: Creates a TCP socket on port 11211, accepts incoming connections.
- **Worker Pool**: Connections are distributed to a configurable pool of threads.
  - Each worker thread handles one or more connections via file descriptors.
  - Threads poll for data (asynchronous I/O for scalability).
- **Why Threading?**:
  - Early I/O was blocking; threading allowed parallelism.
  - Even with async I/O, CPU-intensive tasks (hashing, LRU updates) benefit from multi-threading.

![[Pasted image 20251006013147.png]]
![[Pasted image 20251006013158.png]]
- **Historical Context**: In the early 2000s, blocking I/O limited scalability. Async I/O improved this, but threading remains for CPU-bound work.
- **Configuration**: Number of worker threads is tunable for performance.

## LRU (Least Recently Used) Eviction
When memory fills, Memcached evicts items using LRU to make space, rather than blocking inserts.

### Core Mechanism
- Each slab class has its own LRU linked list.
- Items are linked in a list with head (most recent) and tail (least recent).
- On access (get/set): Move item to head.
- On memory full: Evict from tail (least used).

![[Pasted image 20251006013207.png]]

- **Big Picture**:
  - Chunks in pages are part of the LRU.
  - Eviction happens per slab class.
  
![[Pasted image 20251006013224.png]]

- **Why Not Optional?** (Opinion): LRU adds complexity (locks, maintenance). Disabling it could simplify Memcached, shifting eviction responsibility to clients. However, it prioritizes client convenience.

### LRU Locking and Evolution
- **Concurrency Issue**: Multiple threads can't update LRU simultaneously without corruption.
- **Original Design**: Global lock → Serialized all operations, limiting multi-threading benefits.
- **Improvement 1**: Per-slab-class locks → Parallel access across classes, but serialized within.
- **Improvement 2**: Batched updates (every 60 seconds) to reduce lock contention.
- **2018 Redesign**: Sub-LRUs per slab class by "temperature" (hot/warm/cold) → Further reduces locking.

![[Pasted image 20251006013240.png]]

- **Performance Impact**: Locks can bottleneck throughput. Sub-LRUs help, but intra-temperature contention remains.
- **Study Tip**: Understand trade-offs: LRU ensures availability but introduces overhead. Compare to strict memory limits without eviction.

## Reads and Writes
Operations use hash tables for O(1) average-case access.

### Hash Table Basics
- Keys hash to indices in a fixed-size array (modulo table size).
- Each index points to an item (or chain for collisions).

### Reads (Get)
1. Hash key → Get index.
2. Follow pointer to item in slab chunk.
3. Read value.
4. Update LRU: Lock slab's LRU, move item to head.
- If same-slab concurrent reads: Serialized due to lock.

![[Pasted image 20251006013254.png]]

- Sequential Reads: Reading another key (e.g., "buzz" → item c) moves c to head after d.

![[Pasted image 20251006013302.png]]

### Writes (Set)
1. Hash key → Get index.
2. If empty: Allocate chunk in appropriate slab, store item, point hash table to it.
3. If exists: Update value, move to LRU head (with lock).
- For new items: May allocate new page if slab full.

![[Pasted image 20251006013310.png]]

## Collisions
Hash collisions occur when multiple keys map to the same index.

- **Resolution**: Chaining – Each index points to a linked list of items.
- **Read/Write Cost**: O(N) worst-case (traverse chain).
- **Mitigation**: Monitor chain lengths; resize hash table if too long (rehash all items).

![[Pasted image 20251006013319.png]]

- **Performance Note**: Long chains degrade reads. Resizing flattens but is expensive.

## Distributed Cache
- **Design Philosophy**: Servers are isolated – No inter-server communication.
- **Client Responsibility**: Clients hash keys across servers (e.g., consistent hashing).
- **Benefits**: Simplicity, no coordination overhead (e.g., unlike ZooKeeper).
- **Opinion**: Elegant and scalable; pushes complexity to clients where it belongs.

![[Pasted image 20251006013327.png]]

## Additional Notes and Opinions
- **Overall Simplicity**: Memcached's "feature-stripped" approach makes it reliable but requires careful application design.
- **Potential Improvements** (From Article): Make LRU optional for even more simplicity.
- **Demo Placeholder**: The original article mentions a demo but doesn't provide one. For study, experiment with Memcached via tools like `telnet` or libraries (e.g., Python's `pymemcache`).
  - Example Command: `set key 0 60 5\r\nvalue\r\n` (key, flags, TTL, length, value).