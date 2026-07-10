## Sequential Table Scan (Seq Scan)

- **What it does**: Reads every row in the table sequentially, checking each for the query condition.
- **How it works**:
    - No index is used.
    - Scans the entire table from start to end.
- **When used**:
    - No suitable index exists.
    - Query filters a large portion of the table (e.g., `SELECT * FROM table` or `WHERE column LIKE '%value%'`).
    - Small tables where indexing overhead outweighs benefits.
- **Performance**:
    - **Slow** for large tables, as it reads all data.
    - Cost proportional to table size (e.g., `cost=0.00..289025` for 1.2B rows).
- **Example**:
    
    ```sql
    EXPLAIN SELECT * FROM employees WHERE name LIKE '%Zs%';
    ```
    
    Output: `Seq Scan on employees`.

## Index Scan

- **What it does**: Uses an index to find specific rows, then fetches those rows from the table.
- **How it works**:
    - Traverses the index (e.g., B-tree) to locate row pointers.
    - Accesses the table (heap) for matching rows.
- **When used**:
    - Query filters a small, specific subset of rows (e.g., `WHERE id = 2000`).
    - Index exists on the filtered column (e.g., primary key or indexed column).
- **Performance**:
    - **Fast** for selective queries, as it minimizes table access.
    - Cost depends on index lookup and heap fetches (e.g., low cost for few rows).
    - Less efficient if many rows are returned (index overhead + heap access).
- **Example**:
    
    ```sql
    EXPLAIN ANALYZE SELECT id FROM employees WHERE id = 2000;
    ```
    
    Output: `Index Only Scan using employees_pkey on employees` (if index covers all columns, else `Index Scan`).

## Bitmap Index Scan

- **What it does**: Uses an index to build a bitmap of matching rows, then scans the table for those rows.
- **How it works**:
    - Scans the index to mark matching row locations in a bitmap.
    - Table is accessed in physical order for rows marked in the bitmap.
    - Often followed by a **Bitmap Heap Scan** to fetch data.
- **When used**:
    - Query returns a moderate number of rows (more than Index Scan but less than Seq Scan).
    - Multiple indexes are combined (e.g., `WHERE col1 = X AND col2 = Y`).
    - Conditions like `WHERE name LIKE 'Zs%'` with an index.
- **Performance**:
    - **Balanced**: Faster than Seq Scan for selective queries, slower than Index Scan for very few rows.
    - Efficient for disk access, as it reads table pages in order (unlike random access in Index Scan).
    - Less effective for `LIKE '%Zs%'`, as leading wildcards limit index efficiency.
- **Example**:
    
    ```sql
    EXPLAIN ANALYZE SELECT id, name FROM employees WHERE name LIKE 'Zs%';
    ```
    
    Output: `Bitmap Index Scan on employees_name`.

## Comparison Table

|**Scan Type**|**Uses Index**|**Rows Returned**|**Speed**|**Use Case**|
|---|---|---|---|---|
|**Sequential Scan**|No|Many/All|Slow (full table read)|No index, large data fraction, small table|
|**Index Scan**|Yes|Few|Fast (targeted lookups)|Precise filters (e.g., `id = 2000`)|
|**Bitmap Index Scan**|Yes|Moderate|Medium (bitmap + heap scan)|Moderate selectivity, multiple conditions|

## Key Insights

- **Seq Scan**: Avoid for large tables by creating indexes on filtered columns.
- **Index Scan**: Ideal for highly selective queries but costly if fetching many rows.
- **Bitmap Index Scan**: Bridges the gap; good for queries where Index Scan is too random and Seq Scan is too broad.
- **Optimization Tips**:
    - Create indexes on columns used in `WHERE`, `JOIN`, or `ORDER BY`.
    - For `LIKE '%pattern%'`, use trigram indexes (`pg_trgm`) or full-text search.
    - Use `EXPLAIN ANALYZE` to confirm scan type and performance.

# Database Query Plan Explained

## Query

```sql
SELECT name FROM grades WHERE g > 95 AND id < 10000;
```

## Step-by-Step Query Execution Plan

1. **Bitmap Index Scan on `g` (Index: `g`)**
    
    - **What Happens**: The database uses the index on the `g` column to find rows where `g > 95`.
    - **Details**: It scans the index `g` and creates a bitmap (a compact representation of matching rows).
    - **Cost**: 0.00..3808.31
    - **Rows**: 205,850 rows match the condition `g > 95`.
    - **Width**: 0 (bitmap, no actual data fetched yet).
    - **Purpose**: Efficiently identifies rows satisfying `g > 95` without scanning the entire table.
2. **Bitmap Index Scan on `grades_pkey` (Index: Primary Key on `id`)**
    
    - **What Happens**: The database uses the primary key index on the `id` column to find rows where `id < 10000`.
    - **Details**: It scans the `grades_pkey` index and creates another bitmap for matching rows.
    - **Cost**: 0.00..180.21
    - **Rows**: 9,570 rows match the condition `id < 10000`.
    - **Width**: 0 (bitmap, no data fetched yet).
    - **Purpose**: Quickly identifies rows satisfying `id < 10000` using the index.
3. **BitmapAnd Operation**
    
    - **What Happens**: The database performs a logical AND operation on the two bitmaps (from `g > 95` and `id < 10000`) to find rows that satisfy both conditions.
    - **Details**: Combines the bitmaps to produce a new bitmap representing rows that meet both criteria.
    - **Cost**: 3988.96..3988.96
    - **Rows**: 394 rows satisfy both conditions.
    - **Width**: 0 (still a bitmap).
    - **Purpose**: Narrows down the result set to rows matching both `g > 95` AND `id < 10000`.
4. **Bitmap Heap Scan**
    
    - **What Happens**: The database uses the combined bitmap to fetch the actual rows from the `grades` table.
    - **Details**: It accesses the table using the bitmap to locate the rows, then retrieves the `name` column for those rows.
    - **Cost**: 3988.96..5479.62
    - **Rows**: 394 rows are fetched.
    - **Width**: 4 (size of the `name` column data).
    - **Purpose**: Retrieves the actual data (`name`) for the rows identified by the bitmap.

## Final Result

- **Total Rows Returned**: 7 rows.
- **Efficiency Insight**: The bitmap operations allow the database to minimize disk I/O by identifying matching rows before accessing the table. Once the relevant pages are fetched, the rows are accessed from memory, reducing additional costs.

## Summary

- The query uses indexes to efficiently filter rows (`g > 95` and `id < 10000`).
- Bitmaps are used to combine conditions and minimize table access.
- Only the necessary rows are fetched, resulting