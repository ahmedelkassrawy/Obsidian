# Database Cursors in PostgreSQL

## Overview
- **Purpose**: Handle large result sets efficiently by fetching data incrementally instead of all at once.
- **Context**: Useful when dealing with large tables (e.g., a `grades` table with 12 million student records).
- **Problem with Large Result Sets**:
  - Even with filters (e.g., grades between 90 and 100), you might still get millions of rows.
  - Executing `SELECT student_id FROM grades WHERE grade BETWEEN 90 AND 100`:
    - Requires a query execution plan, index usage, data fetching, and result compilation.
    - Results are sent over the network (e.g., via TCP, depending on the DB protocol).
    - Client must have enough memory to store all results, which can be infeasible (e.g., for 1 million rows).
  - This is inefficient and resource-intensive.

## What Are Database Cursors?
- **Definition**: Server-side cursors allow you to fetch query results incrementally from the database.
  - Instead of fetching all rows at once, you create a cursor and fetch rows as needed.
  - The database executes the query only when you fetch rows from the cursor.
- **Key Benefit**: Saves client-side memory and enables streaming or selective fetching.

## How to Use Cursors in PostgreSQL
Cursors must be used within a transaction. Below is an example of how to declare and use a cursor in PostgreSQL.

### Code Example
```SQL
-- Start a transaction
BEGIN;

-- Declare a cursor for the query
DECLARE cursor_c CURSOR FOR 
    SELECT student_id 
    FROM grades 
    WHERE grade BETWEEN 90 AND 100;

-- Fetch the first row from the cursor
FETCH NEXT FROM cursor_c;  -- Returns the first row

-- Fetch the next row
FETCH NEXT FROM cursor_c;  -- Returns the second row

-- Fetch the last row (if needed)
FETCH LAST FROM cursor_c;  -- May require scanning the entire result set

-- Close the cursor and end the transaction
CLOSE cursor_c;
COMMIT;
```

### Explanation
1. **Transaction**: Cursors require an active transaction (`BEGIN`).
2. **Declare Cursor**: The `DECLARE` statement creates a cursor (`cursor_c`) for the query but does not execute it yet.
   - The database prepares an execution plan but waits for fetch commands.
3. **Fetching**:
   - `FETCH NEXT FROM cursor_c`: Retrieves the next row in sequence.
   - `FETCH LAST FROM cursor_c`: Retrieves the last row (may require a full scan unless optimized by indexes).
   - Other options: `FETCH FIRST`, `FETCH PRIOR`, or fetch multiple rows (e.g., `FETCH 100 FROM cursor_c`).
4. **Close Cursor**: Frees resources when done.
5. **Index Usage**:
   - The database may use an index scan, bitmap index scan, or full table scan, depending on the query and indexes.
   - Backward index scans can optimize fetching the last row in some cases.

## Pros of Using Cursors
1. **Memory Efficiency**:
   - Saves client-side memory by fetching rows incrementally (e.g., 100 rows at a time).
   - Ideal for applications (e.g., Python, JavaScript, Go) processing large datasets piecemeal.
   - Example: Fetch 100 rows, process them, discard, then fetch the next 100.
2. **Streaming**:
   - Enables streaming results to other systems (e.g., WebSocket, gRPC connections).
   - Process rows as they arrive, reducing latency.
3. **Cancelability**:
   - Can cancel a cursor early (e.g., after processing 100,000 rows of 1 million).
   - Use `CLOSE cursor_c` and `ROLLBACK` to stop processing.
4. **Paging**:
   - Supports paging through large datasets, though stateful nature complicates web applications.
5. **Stored Procedures**:
   - Can be used in PL/pgSQL for advanced logic in stored procedures.

## Cons of Using Cursors
1. **Statefulness**:
   - Cursors are tied to a transaction, making them stateful.
   - Cannot share cursors across different database connections or processes.
   - Challenges for horizontally scaled web applications:
     - Each request may hit a different server, unaware of the cursor.
     - Advanced DevOps (e.g., proxies) can pin requests to the same transaction, but this is complex.
   - Stateful paging is less practical than stateless paging (e.g., `OFFSET`/`LIMIT`), though stateless queries repeat work and "insult" the database.
2. **Long-Running Transactions**:
   - Cursors require an open transaction, which can run for a long time.
   - Long-running transactions:
     - Prevent DDL operations (e.g., schema changes) on the table.
     - May block write operations due to shared locks.
     - Interfere with database maintenance (e.g., indexing).
3. **Performance Overhead**:
   - Fetching the last row (`FETCH LAST`) may require scanning the entire result set, depending on query and index efficiency.

## Practical Use Cases
- **Large Data Processing**:
  - Process millions of rows in a backend application without loading everything into memory.
  - Example: Python script fetching 100 rows at a time to process student grades.
- **Streaming Applications**:
  - Stream query results to a client (e.g., via WebSocket or gRPC).
- **Interview Context**:
  - When asked about sorting a billion rows, clarify data source (database vs. memory).
  - Suggest cursors for efficient processing instead of loading all rows into memory.
  - Example: Sort while fetching rows incrementally from a database.

## Notes for Study
- **Key Insight**: Cursors are ideal for handling large datasets incrementally, but their stateful nature limits scalability in web applications.
- **Best Practices**:
  - Use cursors within transactions.
  - Fetch small batches to manage memory.
  - Avoid long-running transactions to minimize database impact.
  - Consider stateless alternatives (e.g., `OFFSET`/`LIMIT`) for web paging, despite inefficiencies.
- **Comparison to Alternatives**:
  - Stateless queries (`OFFSET`/`LIMIT`): Repeat queries, less efficient but simpler for web apps.
  - Cursors: More efficient for sequential processing but harder to scale.
- **Future Content**: Potential video on cursor-based paging vs. stateless paging in web applications.
