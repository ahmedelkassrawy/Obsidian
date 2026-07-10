This document captures key insights into PostgreSQL query performance analysis using `EXPLAIN` and `EXPLAIN ANALYZE`, based on example queries run on `employees` and `grades` tables.

## Query 1: Selecting `id` with Exact Match

**Query:**

```sql
EXPLAIN ANALYZE SELECT id FROM employees WHERE id = 2000;
```

**Output:**

```
Index Only Scan using employees_pkey on employees
   Heap Fetches: 0
```

**Analysis:**

- **Index Only Scan**: Uses the primary key index (`employees_pkey`) to directly fetch the `id`.
- **Heap Fetches: 0**: No need to access the table data (heap) since `id` is in the index, making it very efficient.
- **Performance**: Fast because it leverages the index for a precise lookup.

## Query 2: Pattern Matching on `name`

**Query:**

```sql
EXPLAIN ANALYZE SELECT id, name FROM employees WHERE name LIKE '%Zs%';
```

**Initial Output (No Index):**

```
Seq Scan on employees
```

**Analysis (No Index):**

- **Sequential Scan (Seq Scan)**: Scans the entire table since no index exists for `name`.
- **Performance**: Slow, especially for large tables, as it reads every row to check for the pattern `%Zs%`.

**Action Taken:**

```sql
CREATE INDEX employees_name ON employees(name);
```

**Query (After Index):**

```sql
EXPLAIN ANALYZE SELECT id, name FROM employees WHERE name LIKE '%Zs%';
```

**Output (With Index):**

```
Bitmap Index Scan on employees_name
```

**Analysis (With Index):**

- **Bitmap Index Scan**: Uses the `employees_name` index but still slow for `LIKE '%Zs%'`.
- **Why Slow?**: Leading wildcards (`%Zs%`) prevent efficient index usage, as PostgreSQL cannot skip to specific index entries. It scans the entire index, negating most benefits.

## Query 3: Full Table Scan on `grades`

**Query:**

```sql
EXPLAIN SELECT * FROM grades;
```

**Output:**

```
Seq Scan on grades
(cost=0.00..289025 rows=1214121215 width=...)
```

**Analysis:**

- **Sequential Scan**: Reads every row in `grades`, with no filtering conditions.
- **Cost**:
    - `0.00`: No prior operations (e.g., joins or aggregations).
    - `289025`: Estimated time to fetch all rows.
- **Rows**: `1,214,121,215` rows, indicating a massive table.
- **Width**: Represents the average row size in bytes (binary size).
- **Performance Tip**: Avoid `SELECT COUNT(*)` for row counts on large tables due to poor performance. Use `EXPLAIN` to estimate row counts instead.

## Query 4: Sorting on `name` in `grades`

**Query:**

```sql
EXPLAIN SELECT * FROM grades ORDER BY name;
```

**Output:**

```
Gather Merge
   Sort
      Seq Scan on grades
(cost=0.00..1024586 rows=1214121215 width=...)
Workers Planned: 2
```

**Analysis:**

- **Read from Bottom to Top**:
    1. **Seq Scan on grades**: Full table scan, no index on `name` (`cost=0` for scan alone).
    2. **Sort**: Sorts rows by `name` (`cost=1024586`, significant due to sorting large dataset).
    3. **Gather Merge**: Combines results from parallel workers.
- **Workers Planned: 2**: Two threads process the query in parallel.
- **Performance**: High cost due to sorting without an index. Sorting large datasets is expensive.
- **Solution**: Create an index to optimize sorting:
    
    ```sql
    CREATE INDEX grades_name ON grades(name);
    ```
    
    This allows PostgreSQL to use the index for ordered results, reducing sort overhead.

## General Performance Tips

- **Indexes**:
    - Use for frequent `WHERE`, `JOIN`, or `ORDER BY` columns.
    - Be cautious with `LIKE '%...%'`—consider trigram or full-text search indexes.
- **Avoid Full Scans**:
    - Filter rows early with `WHERE` clauses.
    - Use indexes to reduce scanned rows.
- **EXPLAIN ANALYZE**:
    - Use to measure actual execution time and compare planned vs. actual rows.
    - Read plans bottom-up to understand query flow.
- **Row Counts**:
    - Avoid `SELECT COUNT(*)` on large tables.
    - Use `EXPLAIN` for quick row estimates.
- **Parallelism**:
    - PostgreSQL uses parallel workers for large scans/sorts if enabled.
    - Check `Workers Planned` to see thread usage.