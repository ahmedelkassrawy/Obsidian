
## Single-Column Index

### Creating a Single-Column Index

```sql
CREATE INDEX id_idx ON grades(id);
```

### Query with Index Scan

```sql
EXPLAIN ANALYZE SELECT name FROM grades WHERE id = 7;
```

- **Result**: Index Scan
- **Explanation**: The query uses the index `id_idx` to find the row with `id = 7`, but it must go back to the table to fetch the `name` column, as it is not included in the index.

### Query with Index-Only Scan

```sql
EXPLAIN ANALYZE SELECT id FROM grades WHERE id = 7;
```

- **Result**: Index-Only Scan
- **Explanation**: Since the `id` column is already in the index, the database can retrieve the data directly from the index without accessing the table.

## Covering Index (INCLUDE Clause)

### Creating a Covering Index

```sql
CREATE INDEX id_idx ON grades(id) INCLUDE (name);
```

### Query with Covering Index

```sql
EXPLAIN ANALYZE SELECT name FROM grades WHERE id = 7;
```

- **Result**: Index-Only Scan
- **Explanation**: The index now includes the `name` column as a non-key column, allowing the database to retrieve both `id` and `name` directly from the index, avoiding table access.

## Composite (Multi-Column) Index

### Creating a Composite Index

```sql
CREATE INDEX ON table_name(col_a, col_b);
```

### Query Using Leftmost Column

```sql
EXPLAIN ANALYZE SELECT c FROM test WHERE col_a = 70;
```

- **Result**: Uses Composite Index
- **Explanation**: The index is built left-to-right, so filtering on `col_a` (the leftmost column) allows efficient use of the composite index.

### Query Using Right Column Only

```sql
EXPLAIN ANALYZE SELECT c FROM test WHERE col_b = 100;
```

- **Result**: Parallel Sequential Scan
- **Explanation**: The composite index cannot be used because the filter is on `col_b`, which is not the leftmost column. The database resorts to a sequential scan.

### Query Using Both Columns

```sql
EXPLAIN ANALYZE SELECT c FROM test WHERE col_a = 70 AND col_b = 80;
```

- **Result**: Uses Composite Index
- **Explanation**: The query filters on both `col_a` and `col_b`, allowing full utilization of the composite index for efficient data retrieval.

### Query with OR Condition

```sql
EXPLAIN ANALYZE SELECT c FROM test WHERE col_a = 70 OR col_b = 80;
```

- **Result**: Parallel Sequential Scan
- **Explanation**: The `OR` condition prevents the use of the composite index, as it cannot efficiently handle non-leftmost column filters in this context. A sequential scan is used instead.

### Query on Right Column with Bitmap Scan

```sql
EXPLAIN ANALYZE SELECT c FROM test WHERE col_b = 100;
```

- **Result**: Bitmap Index Scan + Bitmap Heap Scan
- **Explanation**: If a query filters only on `col_b` and a composite index on `(col_a, col_b)` exists, the database may use a bitmap index scan on the index, followed by a bitmap heap scan to retrieve the data.

## Key Takeaways

- **Single-Column Indexes**: Useful for queries filtering on a single column but may require table access for non-indexed columns.
- **Covering Indexes**: Use `INCLUDE` to add non-key columns, enabling index-only scans for better performance.
- **Composite Indexes**: Built left-to-right; queries must filter on the leftmost column(s) to use the index effectively.
- **Query Conditions**:
    - `AND` conditions on composite index columns work well.
    - `OR` conditions or filters on non-leftmost columns often lead to sequential scans.
- **Bitmap Scans**: Used when filtering on non-leftmost columns in a composite index, combining index and heap scans.