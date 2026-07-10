DB engines sometimes called "Storage engines" sometimes called "Embedded db" are software libraries that DBMS uses to.
## Core Concept: What is a Database Engine?
A **database engine** is essentially a library that handles:
- **Disk storage** (e.g., SSD or HDD).
- **CRUD operations** (Create, Read, Update, Delete) at the lowest level.
### Simple Analogy
When you run INSERT INTO table VALUES (1, 2, 3);:
1. Multiple layers process the query.
2. **Lowest layer**: Flushes data to disk (e.g., writing bytes to a file).
3. The engine abstracts this away—no need to manually manage file I/O.

**Key Insight**: Databases aren't just "storing stuff on disk." They're sophisticated systems with features built on top.
### Minimal Example: Key-Value Store
- As simple as **LevelDB**: Put a key → Store value on disk. That's it.
- No complex queries—just basic persistence.
## ACID Properties and Advanced Engine Features
Engines can support **full ACID transactions**:
- **A**tomicity: All or nothing.
- **C**onsistency: Data remains valid.
- **I**solation: Concurrent transactions don't interfere.
- **D**urability: Changes persist after commit.
### Rich Features in Engines
- **Transactions**: Rollback on failure.
- **Foreign keys**: Enforce relationships.
- **Indexing**: B-trees, LSM-trees, etc.

**Study Tip**: Engines enable **reusability**—build your own DBMS on top without reinventing storage.

## DBMS vs. Database Engine: Separation of Concerns
Modern trend: **Break monolithic databases** into:
- **Engine**: Core storage + CRUD (low-level, reusable).
- **DBMS Layer**: Higher-level features (client-server, replication).
### Why Separate?
- **Reusability**: Use the same engine for different DBMS designs.
- **Customization**: Tailor DBMS for specific workloads.
- **Embedded Use**: Run engine directly in your app (no client-server overhead).
#### Engine (Storage-Focused)
- Handles disk I/O, transactions, ACID.
- Independent of networking or advanced queries.
#### DBMS (Feature-Focused)
- **Master-Follower Replication**: Leader writes, followers copy (not storage-related).
- **Isolation Levels**: Serializable, Read Committed, etc.
- **Stored Procedures**: Server-side code execution.
- **Foreign Keys & Constraints**: Business logic enforcement.

**Key Point**: Features like replication are **DBMS-level**, not engine-level. Engines focus on "how to store," DBMS on "how to use."
## Building Custom Databases
### Why Create Your Own?
- **General-purpose DBMS** (e.g., PostgreSQL) may not optimize for your workload.
- **Latency/Performance Matters**: Design for specific patterns.
- **Use Existing Engines**: Don't start from scratch—pick one and build DBMS on top.
### Use Case Examples

|   |   |   |   |
|---|---|---|---|
|Use Case|Focus|Trade-offs|Example|
|**High-Insert Workload** (e.g., Logs)|Fast writes, slow reads OK|Sacrifice query speed for write throughput|Log storage (append-only)|
|**High-Read Workload**|Fast reads, writes can be slower|Denormalize data, heavy caching|Analytics dashboards|
|**Balanced**|ACID + queries|General-purpose, but less optimized|Web apps|

**Study Question**: How would you design an engine for a "write-once, read-many" scenario (e.g., immutable logs)?

## Embedded Databases
- **Definition**: Engine as a **library** you import—no separate server.
- **Run Directly**: Embed in your app (e.g., on laptop, no network setup).
- **Pros**: Simple, fast startup, low overhead.
- **Examples**: SQLite (embedded SQL), LevelDB (key-value).
**When to Use**: Prototyping, mobile apps, or single-process apps.
## Database Flexibility: Switchable Engines
Some DBMS allow **switching engines per table** for optimization.
### MySQL/MariaDB/Percona
- **Multiple Engines**: InnoDB (ACID, transactions), MyISAM (fast reads, no transactions).
- **Syntax**: CREATE TABLE my_table (id INT) ENGINE=InnoDB;
- **Pros**: Tailor storage per table (e.g., archival data → MyISAM).
- **Cons**: Complexity in management.
### PostgreSQL
- **Fixed Engine**: Stuck with B-tree indexing (no easy swaps).
- **Pros**: Simplicity, consistency.
- **Cons**: Less flexibility for niche optimizations.
**Study Tip**: Compare engines:

```sql
-- MySQL: Switch engines
CREATE TABLE users (id INT PRIMARY KEY) ENGINE=InnoDB;  -- ACID-safe
CREATE TABLE logs (timestamp DATETIME) ENGINE=MyISAM;   -- Fast inserts
```

## Real-World Case: Uber's Database Switch
- **From**: PostgreSQL → **To**: MySQL.
- **Likely Reasons**:
    - MySQL's engine flexibility (InnoDB for transactions, others for scale).
    - Better horizontal scaling for Uber's high-throughput needs.
- **Reference**: Uber Engineering Blog - Schema Evolution (confirm details).

**Study Question**: Why might engine choice matter for a ride-sharing app (high writes for trips, high reads for maps)?

## Key Takeaways for Exam/Review

- **Engine = Storage Library**: CRUD + disk I/O. Can be simple (KV) or complex (ACID).
- **DBMS = Features Layer**: Replication, procedures, isolation—built _on_ engines.
- **Trends**: Modular design → More specialized databases (e.g., for logs vs. analytics).
- **Flexibility**: MySQL shines with swappable engines; PostgreSQL prioritizes consistency.
- **Embedded**: Engines as libs for direct app integration.