## What is SQL OFFSET?

- **Definition**: `OFFSET` instructs the database to **skip a specified number of rows before returning results**, used with `LIMIT` to fetch a specific page of data.
- **Example**: For page 10 with 10 rows per page:
    
    ```sql
    SELECT title FROM news
    ORDER BY id DESC
    LIMIT 10 OFFSET 100;
    ```
    
    - Skips 100 rows, returns the next 10 (rows 101–110).
- **Mechanism**: The database fetches all rows up to `OFFSET + LIMIT` (e.g., 110 rows), then discards the first `OFFSET` rows (100), returning only the `LIMIT` rows (10).
- Fetch -> Discard the OFFSET rows -> Return the  LIMIT rows only (3 operations more)

## Why OFFSET is Slow

- **Performance Issue**:
    - **Row Fetching**: The database scans and fetches all rows from the start up to `OFFSET + LIMIT`, even if only `LIMIT` rows are needed.
    - **Example**:
        - `OFFSET 1000, LIMIT 10`: Fetches 1010 rows, discards 1000, returns 10.
        - `OFFSET 100000, LIMIT 10`: Fetches 100010 rows, discards 100000, returns 10.
    - **Impact**: As `OFFSET` increases, the database performs more work, increasing CPU and I/O costs.
        - PostgreSQL example: `OFFSET 100000` took 79ms (cached), but first runs could take seconds.
        - For `OFFSET 1000000`, it took 620ms (cached), up to 6 seconds on a cold start.
- **Locking (Other Databases)**:
    - In SQL Server, **large `OFFSET` queries may trigger lock escalation**, impacting concurrency.
    - PostgreSQL avoids lock escalation but still suffers from excessive row scanning.
- **Inefficiency**: The database cannot optimize by skipping rows directly; it must process all rows up to the offset.

## Additional Problem: Duplicate Rows

- **Issue**: Data changes (e.g., new row insertions) during paging can shift rows, causing duplicates.
- **Scenario**:
    - User requests page 11 (`OFFSET 110, LIMIT 10`).
    - A new row is inserted, shifting the result set.
    - Row 101 (previously read on page 10) may reappear in page 11’s result set.
- **Impact**: Users see duplicate data, degrading application reliability.

## Practical Demonstration (PostgreSQL)

- **Setup**: Table `news` with columns `id` (indexed, auto-incrementing), `title`, etc.
- **Queries Tested**:
    - **OFFSET 0, LIMIT 10**:
        - Execution: 0.2ms, fetched 10 rows.
        - Used backward index scan (`ORDER BY id DESC`).
    - **OFFSET 1000, LIMIT 10**:
        - Execution: 1ms, fetched 1010 rows, discarded 1000.
    - **OFFSET 100000, LIMIT 10**:
        - Execution: 79ms (cached), fetched 100010 rows, discarded 100000.
    - **OFFSET 1000000, LIMIT 10**:
        - Execution: 620ms (cached), ~6s on cold start, fetched 1000010 rows.
- **Observation**: Higher `OFFSET` values drastically increase row fetching and processing time.

## Alternative: Keyset Pagination (Seek Method)

- **Concept**: Uses a unique, indexed column (e.g., `id`) to fetch the next page based on the last row’s value, avoiding `OFFSET`.
- **Example**:
    
    ```sql
    SELECT id, title
    FROM news
    WHERE id < {last_id}
    ORDER BY id DESC
    LIMIT 10;
    ```
    
    - First page: Fetch first 10 rows.
    - Next page: Use the last `id` from the previous page as a filter.
- **Execution**:
    - Query returns 10 rows directly using the index.
    - Example: For “page 1000” equivalent, filter by `id < {last_id}`, still fetches only 10 rows.
    - Execution time: ~instantaneous (e.g., 89 rows processed vs. 100010 with `OFFSET`).
- **Mechanism**:
    - Leverages the index on `id` for efficient filtering.
    - `LIMIT 10` ensures only the required rows are fetched.
    - Backward index scan applies the filter (`WHERE id < {last_id}`) before fetching, minimizing I/O.

## Benefits of Keyset Pagination

- **Performance**:
    - Fetches only the needed rows (e.g., 10 vs. 100010).
    - Scales well for large datasets, even for “deep” pages (e.g., page 1000).
    - Reduces CPU and I/O costs.
- **Consistency**:
    - Avoids duplicate rows since it uses a stable key (`id`) rather than row counts.
    - Insensitive to data changes (inserts/deletes) as long as the key is unique.
- **Simplicity**:
    - Requires the application to track the last `id` (or key) per page.
    - Can support forward/backward navigation by adjusting the `WHERE` condition (e.g., `id > {last_id}` for forward).

## Implementation Notes

- **Application Logic**:
    - Return the `id` with each row to the client.
    - Client sends the last `id` in the next API request (e.g., `GET /news?last_id=123`).
- **Index Requirement**: Ensure the column used for pagination (`id`) is indexed for optimal performance.
- **SQL Variations**:
    - Use `LIMIT 10` or `FETCH FIRST 10 ROWS ONLY` (equivalent).
    - Avoid `OFFSET` or two-parameter `LIMIT` (e.g., `LIMIT 1000, 10`), which behaves like `OFFSET`.

## Key Takeaways

- **Avoid `OFFSET`**: It’s inefficient for large datasets due to excessive row fetching and discarding.
- **Use Keyset Pagination**: Leverages indexes and unique keys for fast, consistent paging.
- **Understand Your Database**: Test and analyze query performance (e.g., using `EXPLAIN ANALYZE` in PostgreSQL).
- **Follow Best Practices**: Read resources like "Use The Index, Luke" for deeper database optimization insights.

## Tags

#SQL #Pagination #OFFSET #KeysetPagination #DatabasePerformance #PostgreSQL #Indexing