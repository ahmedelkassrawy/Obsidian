## Both Indexes

```SQL
SELECT * FROM T WHERE F1 = 1 AND F2 = 4
```

- Used when result set is not too small or too large.
- Index intersection is faster than a full table scan or single-index lookup

## Only One Index

```SQL
SELECT * FROM T WHERE F1 = 1 AND F2 = 4
```

- One index is used for the search and the other col we use table scan
### Use Cases:
-  F1 is a primary key or highly selective.
- Table statistics suggest one index is sufficient.
- The second condition is less selective or not indexed efficiently.

## No Indexes Used (Full Table Scan)

### Uses Cases:
- The optimizer estimates a large result set, making indexes inefficient.
- Indexes are missing, outdated, or less selective.
- Table statistics indicate a full scan is faster.

## Force Index

```SQL
SELECT * FROM T WHERE F1 = 1 AND F2 = 4 
/*+ INDEX(T F1_IDX) */;
```

- **When to use**:
    - Optimizer chooses a suboptimal plan.
    - Table statistics are stale or misleading.
    - You want to test a specific index’s performance.
- **Caution**:
    - Hints can degrade performance if misused.
    - Regularly update statistics to avoid reliance on hints.

## 🧠 Summary

| Case       | Index Usage         | When It Happens                            | Performance Notes                        |
| ---------- | ------------------- | ------------------------------------------ | ---------------------------------------- |
| **Case 1** | Both (Intersection) | Medium-sized result set, efficient indexes | Fast for selective queries               |
| **Case 2** | One Index           | One condition is highly selective          | Moderate; depends on filter efficiency   |
| **Case 3** | None (Table Scan)   | Large result set or poor index selectivity | Slow for large tables                    |
| **Hint**   | Forced Index        | Optimizer overridden via hint              | Use cautiously; verify with EXPLAIN PLAN |