# MongoDB Clustered Collections (v5.3+)

## Overview
- **Introduced**: MongoDB 5.3
- **Purpose**: Improves read/write performance by storing documents inline with the clustered index (eliminates hidden index).
- **Key Concept**: Clustered index = data stored ordered by index key (documents in leaf pages of the index).
- **Comparison**: Like primary/clustered indexes in other DBs (e.g., SQL Server, MySQL InnoDB), but must be on `_id` field.
- **Default**: Collections are non-clustered (pre-v5.3 behavior).

> **Note**: MongoDB uses WiredTiger storage engine (acquired in v4+), supporting ACID, MVCC, and compression.

## Non-Clustered Collections (Default Behavior)
### Storage Structure
- **Hidden Index** (internal, not user-visible):
  - Key: Record ID (64-bit integer, 8 bytes).
  - Value: BSON document (compressed).
  - Acts as a clustered index on Record ID.
- **_id Index** (user-visible, auto-generated):
  - Key: `_id` (ObjectId, ~12 bytes).
  - Value: Record ID (pointer to hidden index).
- **Secondary Indexes**: Point to Record ID (fixed 8 bytes).

### Operations
- **Read (e.g., find by `_id`)**:
  1. Traverse `_id` index → Get Record ID.
  2. Traverse hidden index with Record ID → Get document.
  - **Cost**: 2 B-tree traversals (multiple I/Os possible).
  - Leads to random I/Os (Record IDs not sequential).
- **Write (insert/update/delete)**:
  - Update hidden index + `_id` index.
  - **Cost**: 2 writes (double B-tree updates).
- **Range Queries on `_id`**:
  - Sequential on `_id` index, but random jumps to hidden index → Poor cache efficiency, more evictions.
- **Storage Overhead**:
  - Duplicate structures: Hidden index + separate `_id` index.
  - Fixed 8-byte pointers in indexes.

### Drawbacks
- Random I/Os reduce performance.
- Higher storage (extra B-tree overhead).
- No TTL (time-to-live) on `_id` by default.

## Clustered Collections
### Storage Structure
- **No Hidden Index**: Eliminated.
- **Clustered Index on `_id`**:
  - Key: `_id` (~12 bytes, incremental with timestamp).
  - Value: BSON document (inline in leaf pages).
- **Secondary Indexes**: Point to `_id` value (variable size, e.g., 12 bytes default; larger for UUIDs).
- Documents stored in sorted order by `_id`.

### Operations
- **Read (e.g., find by `_id`)**:
  - Single traversal on clustered index → Document inline.
  - **Cost**: 1 B-tree traversal.
- **Write (insert/update/delete)**:
  - Single update on clustered index.
  - **Cost**: 1 write.
- **Range Queries on `_id`**:
  - Sequential access (documents co-located in pages) → Fewer I/Os, better cache hits.
- **TTL Support**: Use expireAfterSeconds on `_id` index for auto-deletion (eliminates separate TTL index).

### Creation
- Must specify at collection creation (cannot add later).
- Syntax:
  ```javascript:disable-run
  db.createCollection("myCollection", {
    clusteredIndex: {
      key: { _id: 1 },
      unique: true,
      name: "myClusteredIndex"
    }
  })
  ```
- **Limitations**:
  - Only one clustered index per collection.
  - Key must be `_id` (unique, ascending).
  - Cannot convert existing non-clustered → clustered (or vice versa); create new collection and migrate data.

## Benefits
| Aspect | Non-Clustered | Clustered | Improvement |
|--------|---------------|-----------|-------------|
| **Queries on `_id`** (equality/range) | 2 traversals | 1 traversal | ~50% faster reads; no secondary index needed. |
| **Inserts/Updates/Deletes** | 2 writes | 1 write | Faster bulk operations. |
| **Storage Size** | Higher (hidden + `_id` indexes) | Lower (single structure) | Reduced I/O; better cache efficiency. |
| **Range Scans** | Random I/Os on hidden index | Sequential (co-located docs) | Fewer page faults, higher throughput. |
| **TTL** | Requires separate index | Built-in on `_id` | Eliminates extra index overhead. |

- **General**: Lower storage → Less I/O overall.
- **Page Size**: WiredTiger uses 4KB pages; smaller storage fits more in cache.

## Limitations & Trade-offs
- **Creation Only**: Cannot add clustered index post-creation (avoids exclusive locks blocking R/W).
  - Workaround: Create new collection, migrate data.
- **Query Planner Behavior**:
  - Prefers secondary indexes over clustered if usable (even for `_id` queries).
  - **Risk**: Performance degradation (e.g., index scan + filter vs. direct clustered lookup).
  - **Fix**: Use `hint()` to force clustered index.
    ```javascript
    db.myCollection.find({ _id: ObjectId("...") }).hint({ _id: 1 })
    ```
- **Secondary Index Overhead**:
  - Point to `_id` (12+ bytes) vs. Record ID (8 bytes) → ~4 bytes extra per entry.
  - **Worse with Custom `_id`**: UUIDs (16 bytes binary or 36 bytes string) → Massive growth (e.g., +28 bytes/entry).
  - Multiplies with many indexes → Higher storage/I/O.
- **Key Size Impact**:
  - Large `_id` keys bloat clustered index + secondaries → Reduced benefits.
  - Max key size: 8MB (avoid large keys).
- **No Sharding on Clustered Key**: Cannot shard on `_id` (use hashed `_id` instead).
- **Storage Increase for Secondaries**: If many secondaries + large `_id`, total size may exceed non-clustered.

## Best Practices
- **Use When**: High `_id`-based queries, time-series data (leverages incremental `_id` timestamps), TTL needs.
- **Avoid When**: Custom large `_id` (e.g., UUID strings), heavy secondary index reliance without hints.
- **Migration**: For existing data, export/import to new clustered collection.
- **Monitoring**: Check `explain()` plans; use hints if planner picks wrong index.
- **Further Reading**:
  - [MongoDB Docs: Clustered Collections](https://www.mongodb.com/docs/manual/core/clustered-collections/)
  - WiredTiger internals (source code for hidden index details).

