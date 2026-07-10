This guide demonstrates how to create a partitioned table in PostgreSQL, create child partitions, attach them, and manage indexes.
## Step 1: Create the Parent Table

Create a table `grades_parts` with partitioning by range on the `g` column.

```sql
CREATE TABLE grades_parts (
    id SERIAL NOT NULL,
    g INT NOT NULL
) PARTITION BY RANGE(g);
```

- `id SERIAL NOT NULL`: Auto-incrementing primary key.
- `g INT NOT NULL`: Integer column for grades, used as the partition key.
- `PARTITION BY RANGE(g)`: Partitions the table based on ranges of the `g` column.

## Step 2: Create Child Partition Tables

Create four child tables to hold specific ranges of grades, inheriting the structure of the parent table.

```sql
CREATE TABLE g0035 (LIKE grades_parts INCLUDING INDEXES);
CREATE TABLE g3560 (LIKE grades_parts INCLUDING INDEXES);
CREATE TABLE g6080 (LIKE grades_parts INCLUDING INDEXES);
CREATE TABLE g80100 (LIKE grades_parts INCLUDING INDEXES);
```

- `LIKE grades_parts`: Copies the structure of `grades_parts`.
- `INCLUDING INDEXES`: Ensures any indexes defined on the parent are also created on the child tables.

## Step 3: Attach Partitions

Attach each child table to the parent table, specifying the range of `g` values each partition will hold.

```sql
ALTER TABLE grades_parts ATTACH PARTITION g0035 FOR VALUES FROM (0) TO (35);
ALTER TABLE grades_parts ATTACH PARTITION g3560 FOR VALUES FROM (35) TO (60);
ALTER TABLE grades_parts ATTACH PARTITION g6080 FOR VALUES FROM (60) TO (80);
ALTER TABLE grades_parts ATTACH PARTITION g80100 FOR VALUES FROM (80) TO (100);
```

- `FOR VALUES FROM (start) TO (end)`: Defines the range of `g` values for each partition.
- Ranges are exclusive of the upper bound (e.g., `g0035` includes `g` from 0 to 34).

## Step 4: Query a Partition

Query the maximum value of `g` in the `g3560` partition (grades 35–59).

```sql
SELECT MAX(g) FROM g3560;
```

- This query only scans the `g3560` partition, improving performance for range-based queries.

## Step 5: Create an Index on the Parent Table

Create an index on the `g` column of the parent table, which automatically applies to all partitions.

```sql
CREATE INDEX grades_parts_idx ON grades_parts(g);
```

- The index is propagated to all child partitions because they were created with `INCLUDING INDEXES`.
- This improves query performance for searches or range queries on `g`.

## Key Notes

- **Partitioning Benefits**: Improves query performance by limiting scans to specific partitions and allows easier data management (e.g., dropping old partitions).
- **Index Propagation**: Indexes on the parent table are automatically created on child partitions if `INCLUDING INDEXES` is used.
- **Range Partitioning**: Ensure ranges are non-overlapping and cover all possible values to avoid errors.
- **Use Case**: Ideal for managing large datasets, like grades, where data can be logically divided into ranges.

## Example Workflow

1. Insert a grade: `INSERT INTO grades_parts (g) VALUES (45);`
    - This inserts into `g3560` (range 35–60).
2. Query: `SELECT * FROM grades_parts WHERE g > 50;`
    - Only scans `g6080` and `g80100` partitions.
3. Check max grade in a partition: `SELECT MAX(g) FROM g3560;`

This structure is efficient for large datasets with range-based queries.