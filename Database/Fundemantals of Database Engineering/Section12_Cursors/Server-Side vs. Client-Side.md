# Server-Side vs. Client-Side Cursors in PostgreSQL with Python

## Overview
- **Context**: Demonstrates the differences between server-side and client-side cursors in PostgreSQL when used with Python.
- **Database Setup**: Example uses a PostgreSQL database (`hussain_db`) with a table (`employees`) populated with 1 million rows.
- **Purpose**: Compare performance and behavior of server-side and client-side cursors when querying large datasets (e.g., fetching 50 rows from a million-row table).

## Definitions
- **Client-Side Cursor**:
  - Executes a query and fetches all results to the client (Python application) over the network.
  - The client stores the results in memory, which can be resource-intensive for large datasets.

- **Server-Side Cursor**:
  - Creates a cursor on the database server, storing results there.
  - Client fetches results incrementally (e.g., 10 or 50 rows at a time), reducing client memory usage and network load.
  - Requires a transaction and is stateful (tied to a specific connection).

## Setup: Populating the Table
To demonstrate cursors, a table (`employees`) is populated with 1 million rows using a Python script.

### Code: `insert_1000000.py`
```python
import psycopg2

# Establish connection
connection = psycopg2.connect(
    host="hussain_mac",
    database="hussain_db",
    user="postgres",
    password="postgres",
    port="5432"
)

# Create a cursor
cursor = connection.cursor()

# Insert 1 million rows
for i in range(1000000):
    cursor.execute("INSERT INTO employees (id, name) VALUES (%s, %s)", (i, f"test_{i}"))

# Commit changes
connection.commit()

# Close cursor and connection
cursor.close()
connection.close()
```

### Notes
- **Connection Details**: Uses default PostgreSQL port (5432), database `hussain_db`, and credentials `postgres`/`postgres`.
- **Insert Loop**: Inserts 1 million rows with `id` (sequential) and `name` (e.g., `test_0`, `test_1`, ...).
- **Commit**: Ensures changes are saved; without `commit()`, changes would roll back.
- **Performance Note**: Simple loop-based insert is not optimal (bulk inserts are faster), but sufficient for demo purposes.
- **Verification**: After running, a `SELECT COUNT(*) FROM employees` confirms 1 million rows.

## Client-Side Cursor
- **Behavior**: Executes the query and fetches all results to the client, even if only a subset (e.g., 50 rows) is needed.
- **Performance**: High memory and network usage for large result sets.

### Code: `client_cursor.py`
```python
import psycopg2
import time

# Establish connection
connection = psycopg2.connect(
    host="hussain_mac",
    database="hussain_db",
    user="postgres",
    password="postgres",
    port="5432"
)

# Measure cursor creation time
start_time = time.time()
cursor = connection.cursor()  # Client-side cursor (default, no name)
cursor_time = (time.time() - start_time) * 1000  # Convert to milliseconds

print(f"Cursor established in {cursor_time:.2f} milliseconds")

# Measure query execution time
start_time = time.time()
cursor.execute("SELECT * FROM employees")  # Executes and fetches all rows to client
execute_time = (time.time() - start_time) * 1000

print(f"Execute query in {execute_time:.2f} milliseconds")

# Fetch first 50 rows
start_time = time.time()
rows = cursor.fetchmany(50)  # Fetch only 50 rows
fetch_time = (time.time() - start_time) * 1000

print(f"Fetch first 50 rows in {fetch_time:.2f} milliseconds")

# Close cursor and connection
cursor.close()
connection.close()
```

### Results (Example)
- **Cursor Creation**: ~0.02 ms (negligible, just declares the cursor).
- **Execute Query**: ~845 ms (fetches all 1 million rows to client memory).
- **Fetch 50 Rows**: ~0 ms (fast, as results are already on the client).
- **Memory Impact**: Client holds 1 million rows as a tuple (not an array, so memory allocation is optimized but still significant).

## Server-Side Cursor
- **Behavior**: Creates a named cursor on the server, executes the query lazily, and fetches results incrementally.
- **Performance**: Lower client memory usage, but requires round trips to the server for each fetch.

### Code: `server_cursor.py`
```python
import psycopg2
import time

# Establish connection
connection = psycopg2.connect(
    host="hussain_mac",
    database="hussain_db",
    user="postgres",
    password="postgres",
    port="5432"
)

# Measure cursor creation time
start_time = time.time()
cursor = connection.cursor(name="server_cursor")  # Server-side cursor (named)
cursor_time = (time.time() - start_time) * 1000

print(f"Cursor established in {cursor_time:.2f} milliseconds")

# Measure query execution time
start_time = time.time()
cursor.execute("SELECT * FROM employees")  # Query plan prepared, not fully executed
execute_time = (time.time() - start_time) * 1000

print(f"Execute query in {execute_time:.2f} milliseconds")

# Fetch first 50 rows
start_time = time.time()
rows = cursor.fetchmany(50)  # Fetch 50 rows from server
fetch_time = (time.time() - start_time) * 1000

print(f"Fetch first 50 rows in {fetch_time:.2f} milliseconds")

# Close cursor and connection
cursor.close()
connection.close()
```

### Results (Example)
- **Cursor Creation**: ~0.02 ms (negligible, declares cursor on server).
- **Execute Query**: ~3 ms (prepares query plan, doesn’t fetch all rows).
- **Fetch 50 Rows**: ~2 ms (slower than client-side due to network round trip, but only fetches 50 rows).
- **Looping**: Fetching subsequent batches (e.g., 50 rows at a time) takes ~2 ms per fetch.

## Pros and Cons

### Client-Side Cursor
- **Pros**:
  - Minimizes server overhead; server only executes the query and sends results.
  - Once results are fetched, subsequent operations (e.g., `fetchmany(50)`) are fast since data is local.

- **Cons**:
  - High network bandwidth usage (e.g., transferring 1 million rows).
  - High client memory usage (must store all rows, potentially infeasible).
  - Bad practice for unbounded queries (e.g., `SELECT *` without `WHERE` or `LIMIT`).

### Server-Side Cursor
- **Pros**:
  - Reduces client memory usage (fetches small batches, e.g., 50 rows).
  - Reduces network bandwidth (only requested rows are sent).
  - Ideal for processing large datasets incrementally (e.g., ETL, MapReduce).
  - Example: Process 1000 rows at a time, perform operations, and discard.
  
- **Cons**:
  - Stateful operation (tied to a transaction and connection).
    - Not suitable for stateless web applications (different requests may hit different servers).
    - Advanced DevOps (e.g., proxies) needed to pin requests to the same transaction.
  - Server overhead: Maintains cursor state, which can strain the database if many clients create cursors.
  - Risk of cursor leaks (if not closed properly), potentially overwhelming the database.
  - Long-running transactions may block DDL operations or writes.

## Recommendations
- **Client-Side Cursors**:
  - Use for small result sets or when memory/network bandwidth is not a concern.
  - Always use `WHERE` clauses or `LIMIT` to bound queries (avoid `SELECT *`).
  - Preferred by speaker for diligence and simplicity in controlled environments.
  
- **Server-Side Cursors**:
  - Use for large datasets processed incrementally (e.g., ETL, streaming).
  - Be cautious to avoid leaks (always close cursors and commit/rollback transactions).
  - Not ideal for web applications due to statefulness; consider stateless `LIMIT`/`OFFSET` for paging (though less efficient).
  
- **Best Practices**:
  - Avoid unbounded queries (`SELECT *`).
  - Simulate server-side behavior with `LIMIT`/`OFFSET` for stateless applications.
  - Monitor server resources when using server-side cursors to prevent overload.

## Notes for Study
- **Key Insight**: Client-side cursors fetch all data to the client (high memory/network cost), while server-side cursors keep data on the server and fetch incrementally (lower client cost but stateful).

- **Performance Takeaway**:
  - Client-side: Slow query execution (~845 ms for 1M rows), fast fetches (~0 ms).
  - Server-side: Fast query execution (~3 ms), slightly slower fetches (~2 ms per 50 rows).

- **Use Case Examples**:
  - Client-side: Quick queries with small results or local processing.
  - Server-side: Processing millions of rows in batches (e.g., ETL, streaming to WebSocket/gRPC).

- **Python Library**: Uses `psycopg2` for PostgreSQL connectivity.
