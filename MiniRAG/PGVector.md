```python
pip install -qU langchain-postgres
```

```docker
docker run --name pgvector-container -e POSTGRES_USER=langchain -e POSTGRES_PASSWORD=langchain -e POSTGRES_DB=langchain -p 6024:5432 -d pgvector/pgvector:pg16
```

```python
from langchain_postgres import PGVector

# See docker command above to launch a postgres instance with pgvector enabled.
connection = "postgresql+psycopg://langchain:langchain@localhost:6024/langchain"  # Uses psycopg3!
collection_name = "my_docs"

vector_store = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)
```
---
## Async PGVector
The provided Python code is an asynchronous method `setup_db` that sets up a PostgreSQL database using the `asyncpg` library. Below, I’ll identify the database-related functions used in the code and explain what they do:

### Functions Used for Database Operations

1. **`asyncpg.connect`**  
   - **Purpose**: Establishes an asynchronous connection to a PostgreSQL database.
   - **Usage in Code**: 
     ```python
     conn = await asyncpg.connect(
         host=self.url.host,
         port=self.url.port,
         user=self.url.username,
         password=self.url.password,
         database='postgres'
     )
     ```
   - **What it does**: Creates a connection to the default PostgreSQL database (`postgres`) using the provided credentials (host, port, username, password). The `await` keyword is used because this is an asynchronous operation, meaning it doesn’t block the execution while waiting for the connection to be established. The connection object (`conn`) is used for subsequent database operations.
   - **Parameters**:
     - `host`: The database server’s hostname or IP address.
     - `port`: The port number for the database server (typically 5432 for PostgreSQL).
     - `user`: The database username.
     - `password`: The database password.
     - `database`: The name of the database to connect to (here, `'postgres'`).

2. **`conn.fetchval`**  
   - **Purpose**: Executes a query and returns a single value from the result.
   - **Usage in Code**:
     ```python
     exists = await conn.fetchval(
         "SELECT 1 FROM pg_database WHERE datname = $1", 
         self.db_name
     )
     ```
   - **What it does**: Runs a SQL query to check if a database with the name stored in `self.db_name` exists in the `pg_database` system catalog. The query returns `1` if the database exists, or `None` if it doesn’t. The `$1` is a placeholder for the parameter `self.db_name`, which is safely passed to prevent SQL injection. The `await` keyword is used because this is an asynchronous operation.
   - **Parameters**:
     - Query string: `"SELECT 1 FROM pg_database WHERE datname = $1"` checks for the existence of a database.
     - `self.db_name`: The name of the database to check for.

3. **`conn.execute`**  
   - **Purpose**: Executes a SQL command that doesn’t return data (e.g., `CREATE`, `INSERT`, `UPDATE`).
   - **Usage in Code**:
     ```python
     await conn.execute(f'CREATE DATABASE {self.db_name}')
     ```
   - **What it does**: Runs a `CREATE DATABASE` command to create a new database with the name stored in `self.db_name` if it doesn’t already exist. The `await` keyword is used for asynchronous execution. Note: The use of an f-string here could pose a SQL injection risk if `self.db_name` isn’t sanitized, though database names in PostgreSQL have strict rules that mitigate this risk.
   - **Parameters**:
     - Command string: `f'CREATE DATABASE {self.db_name}'` is the SQL command to create the database.

4. **`conn.close`**  
   - **Purpose**: Closes the database connection.
   - **Usage in Code**:
     ```python
     await conn.close()
     ```
   - **What it does**: Terminates the connection to the PostgreSQL database, releasing resources. This is called in the `finally` block to ensure the connection is closed regardless of whether the database creation succeeds or fails. The `await` keyword is used because closing the connection is an asynchronous operation.

---
## Async Code

### Async Database Functions in the Provided Code

The code uses SQLAlchemy's asynchronous features, specifically through the `AsyncSession` object and the `create_async_engine` function. Here are the key async database-related functions and operations:

1. **`create_async_engine`**  
   - **Purpose**: Creates an asynchronous SQLAlchemy engine for PostgreSQL using the `asyncpg` driver.
   - **Usage in Code**:
     ```python
     async_engine = create_async_engine(db_url, echo=False)
     ```
   - **What it does**: Initializes an async engine that manages connections to the PostgreSQL database. The `db_url` is derived from the application settings, with the scheme modified to use `postgresql+asyncpg://` for async operations. The `echo=False` parameter disables SQL statement logging. The engine is used to create a session factory (`AsyncSessionLocal`) for database interactions.
   - **Parameters**:
     - `db_url`: The database URL (e.g., `postgresql+asyncpg://user:password@host:port/dbname`).
     - `echo`: Controls whether SQL statements are logged (set to `False` here).

2. **`async_sessionmaker`**  
   - **Purpose**: Creates a factory for generating asynchronous SQLAlchemy sessions.
   - **Usage in Code**:
     ```python
     AsyncSessionLocal = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
     ```
   - **What it does**: Configures a session factory (`AsyncSessionLocal`) that produces `AsyncSession` objects for interacting with the database asynchronously. The `class_=AsyncSession` specifies that the sessions are async, and `expire_on_commit=False` ensures that objects remain usable after a transaction is committed (avoiding automatic expiration of attributes).
   - **Parameters**:
     - `async_engine`: The async engine created by `create_async_engine`.
     - `class_`: The type of session to create (`AsyncSession` for async operations).
     - `expire_on_commit`: Controls whether objects expire after a commit (set to `False` here).

3. **`AsyncSession.execute`**  
   - **Purpose**: Executes a SQL query asynchronously and returns the result.
   - **Usage in Code** (examples):
     ```python
     result = await db.execute(select(Auth).filter(Auth.username == username))  # In get_current_user
     result = await db.execute(select(Auth).filter(Auth.username == user.username))  # In register
     result = await db.execute(select(Auth).filter(Auth.username == form_data.username))  # In login
     ```
   - **What it does**: Runs a SQLAlchemy `select` query asynchronously to fetch data from the database. The query is constructed using SQLAlchemy’s ORM (e.g., `select(Auth).filter(...)`) to retrieve `Auth` model records based on a username filter. The `await` keyword is used because the operation is asynchronous. The result is a `Result` object that can be further processed (e.g., with `scalar_one_or_none`).
   - **Parameters**:
     - Query: A SQLAlchemy query object (e.g., `select(Auth).filter(...)`).
   - **Returns**: A `Result` object containing the query results.

4. **`Result.scalar_one_or_none`**  
   - **Purpose**: Retrieves a single scalar value or object from a query result, or `None` if no result is found.
   - **Usage in Code** (examples):
     ```python
     user = result.scalar_one_or_none()  # In get_current_user, register, login
     ```
   - **What it does**: Processes the result of an `execute` call to return a single row (as an object or `None`). If more than one row is returned, it raises an exception. This is used to fetch a single `Auth` model instance (or `None`) based on the username filter in the query.
   - **Parameters**: None (operates on the `Result` object).
   - **Returns**: A single ORM object (e.g., an `Auth` instance) or `None`.

5. **`AsyncSession.add`**  
   - **Purpose**: Adds an object to the session for insertion into the database.
   - **Usage in Code**:
     ```python
     db.add(new_user)  # In register
     ```
   - **What it does**: Marks a new `Auth` model instance (`new_user`) for insertion into the database. The object is staged in the session and will be persisted when the session is committed.
   - **Parameters**:
     - Object: The ORM object to add (e.g., `new_user`, an instance of the `Auth` model).

6. **`AsyncSession.commit`**  
   - **Purpose**: Commits the current transaction, persisting changes to the database.
   - **Usage in Code**:
     ```python
     await db.commit()  # In register
     ```
   - **What it does**: Asynchronously commits all changes (e.g., insertions from `add`) in the session to the database. This finalizes the creation of a new user in the `register` endpoint. The `await` keyword is used for async execution.
   - **Parameters**: None.

7. **`AsyncSession.refresh`**  
   - **Purpose**: Refreshes an ORM object with the latest data from the database.
   - **Usage in Code**:
     ```python
     await db.refresh(new_user)  # In register
     ```
   - **What it does**: Asynchronously reloads the `new_user` object from the database to ensure it reflects the latest state (e.g., auto-generated fields like `id` or `created_at`). This is useful after committing a new object to retrieve database-generated values. The `await` keyword is used for async execution.
   - **Parameters**:
     - Object: The ORM object to refresh (e.g., `new_user`).

8. **`AsyncSession.close`**  
   - **Purpose**: Closes the asynchronous session, releasing resources.
   - **Usage in Code**:
     ```python
     await session.close()  # In get_async_db
     ```
   - **What it does**: Asynchronously closes the `AsyncSession` object, releasing database connections back to the connection pool. This is called in the `finally` block of the `get_async_db` dependency to ensure proper cleanup after each request. The `await` keyword is used for async execution.
   - **Parameters**: None.

### Comparison with `setup_db` Functions (from Previous Code)

The `setup_db` method from your earlier question uses the `asyncpg` library directly, while the FastAPI code uses SQLAlchemy’s async features with `asyncpg` as the underlying driver. Below, I compare the async database functions between the two snippets:

| **Function/Operation**         | **Setup_db (asyncpg)**                                                                                                      | **FastAPI Code (SQLAlchemy Async)**                                                                                                      | **Differences**                                                                                                                                                                                 |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Connecting to DB**           | `asyncpg.connect`: Establishes a direct async connection to PostgreSQL using host, port, user, password, and database name. | `create_async_engine`: Creates an async SQLAlchemy engine, which manages a pool of connections. Used indirectly via `AsyncSessionLocal`. | `asyncpg.connect` is low-level, creating a single connection. `create_async_engine` is higher-level, managing a connection pool for multiple sessions. SQLAlchemy abstracts connection details. |
| **Session Management**         | Not applicable (uses raw connection object).                                                                                | `async_sessionmaker`: Creates a factory for `AsyncSession` objects, which manage transactions and ORM operations.                        | `setup_db` doesn’t use sessions, working directly with connections. SQLAlchemy’s `AsyncSession` provides ORM support and transaction management.                                                |
| **Executing Queries**          | `conn.fetchval`: Executes a query and returns a single value.                                                               | `AsyncSession.execute`: Executes a SQLAlchemy query (e.g., `select`) and returns a `Result` object.                                      | `fetchval` is specific to scalar values and uses raw SQL with placeholders. `execute` supports SQLAlchemy’s ORM queries, offering more flexibility (e.g., filtering via Python syntax).         |
| **Fetching Results**           | `conn.fetchval`: Returns a single scalar value or `None`.                                                                   | `Result.scalar_one_or_none`: Returns a single ORM object or `None`.                                                                      | `fetchval` returns raw data (e.g., `1` or `None`). `scalar_one_or_none` returns a mapped ORM object (e.g., `Auth` instance) or `None`, leveraging SQLAlchemy’s ORM.                             |
| **Executing Commands**         | `conn.execute`: Runs a non-select SQL command (e.g., `CREATE DATABASE`).                                                    | `AsyncSession.add` / `AsyncSession.commit`: Stages and persists ORM objects (e.g., inserting a new user).                                | `conn.execute` runs raw SQL commands directly. `add`/`commit` work with ORM objects, abstracting SQL and handling object state.                                                                 |
| **Refreshing Data**            | Not applicable (no equivalent in `setup_db`).                                                                               | `AsyncSession.refresh`: Reloads an ORM object with fresh database data.                                                                  | `setup_db` doesn’t use ORM, so no need for refreshing. `refresh` is specific to SQLAlchemy’s ORM for syncing object state.                                                                      |
| **Closing Connection/Session** | `conn.close`: Closes the raw database connection.                                                                           | `AsyncSession.close`: Closes the async session, releasing the connection to the pool.                                                    | Both close resources, but `conn.close` terminates a single connection, while `AsyncSession.close` releases a session’s connection back to the engine’s pool.                                    |


---
### Common Methods for `Result` Objects
The `Result` object (e.g., `sqlalchemy.engine.Result` in Core or ORM query results) provides several methods to fetch data. Here are the key ones:

1. **Fetching Single Rows or Scalars**
   - `result.scalar_one()`: Retrieves exactly one scalar value from the query. Raises `NoResultFound` if no rows are returned or `MultipleResultsFound` if more than one row is returned.
     ```python
     value = result.scalar_one()  # Expects exactly one row, returns a single value
     ```
     
   - `result.one()`: Retrieves exactly one row as a `Row` object (or ORM object). Raises `NoResultFound` or `MultipleResultsFound` if the result doesn’t contain exactly one row.
     ```python
     row = result.one()  # Returns a single Row or ORM object
     ```
   - `result.one_or_none()`: Retrieves one row or `None` if no rows are found. Raises `MultipleResultsFound` if more than one row is returned.
     ```python
     row = result.one_or_none()  # Returns a Row/ORM object or None
     ```
   - `result.scalar()`: Retrieves the first column of the first row as a scalar value, or `None` if no rows are found. Does not enforce uniqueness.
     ```python
     value = result.scalar()  # First column of first row, or None
     ```

2. **Fetching Multiple Rows**
   - `result.all()`: Returns all rows as a list of `Row` objects (or ORM objects in ORM queries).
     ```python
     rows = result.all()  # Returns list of all rows
     ```
   - `result.fetchall()`: Similar to `all()`, retrieves all rows as a list of `Row` objects. More common in Core queries.
     ```python
     rows = result.fetchall()  # Returns list of all rows
     ```
   - `result.fetchmany(size)`: Fetches the specified number of rows (`size`) as a list. Useful for processing large result sets in chunks.
     ```python
     rows = result.fetchmany(100)  # Fetches up to 100 rows
     ```

3. **Fetching the First Row**
   - `result.first()`: Returns the first row as a `Row` object (or ORM object) or `None` if no rows are found.
     ```python
     row = result.first()  # First row or None
     ```

4. **Iterating Over Results**
   - `result.__iter__()`: Allows iteration over the result set, yielding one `Row` (or ORM object) at a time.
     ```python
     for row in result:
         print(row)  # Iterate over rows
     ```

5. **Accessing Columns and Metadata**
   - `result.keys()`: Returns a list of column names (or aliases) in the result set.
     ```python
     columns = result.keys()  # List of column names
     ```
   - `result.mappings()`: Converts the result into a sequence of dictionaries, where each row is a dictionary mapping column names to values.
     ```python
     for row_dict in result.mappings():
         print(row_dict)  # Each row as a dict
     ```

6. **Row-Specific Methods**
   When iterating or fetching rows, each row is a `Row` object (in Core) or an ORM object (in ORM). `Row` objects have their own methods:
   - `row._mapping`: Access row data as a dictionary.
     ```python
     row = result.first()
     row_dict = row._mapping  # Dictionary of column names to values
     ```
   - `row._asdict()`: Returns the row as a dictionary (similar to `_mapping`).
     ```python
     row_dict = row._asdict()  # Row as dictionary
     ```
   - `row._tuple()`: Returns the row as a tuple of values.
     ```python
     row_tuple = row._tuple()  # Row as tuple
     ```

7. **Partitioning and Yielding**
   - `result.partitions(size)`: Splits the result into partitions of `size` rows, yielding lists of rows for memory-efficient processing.
     ```python
     for partition in result.partitions(100):
         process(partition)  # Process 100 rows at a time
     ```
   - `result.yield_per(size)`: Configures the result to yield `size` rows at a time when iterating, useful for large datasets (Core-specific, used with database-specific settings).
     ```python
     result.yield_per(100)  # Yield 100 rows at a time during iteration
     ```

8. **Unique Results**
   - `result.unique()`: Ensures that rows are unique based on their values (useful for ORM queries with duplicate rows due to joins).
     ```python
     unique_result = result.unique()  # Deduplicates rows
     ```

9. **Closing the Result**
   - `result.close()`: Closes the result cursor, releasing database resources. This is often unnecessary in modern SQLAlchemy as results are automatically closed in many contexts, but it’s good practice for large result sets in Core queries.
     ```python
     result.close()  # Explicitly close the cursor
     ```

10. **Checking Result Status**
    - `result.returns_rows`: Boolean indicating if the result contains rows (e.g., `SELECT` queries return `True`, while `INSERT`/`UPDATE` may return `False`).
      ```python
      has_rows = result.returns_rows  # True if result has rows
      ```
    - `result.rowcount`: Returns the number of rows affected (for `INSERT`, `UPDATE`, `DELETE`) or rows matched (for `SELECT` in some databases).
      ```python
      count = result.rowcount  # Number of rows affected or matched
      ```

### ORM-Specific Methods
If you’re using SQLAlchemy’s ORM (e.g., `session.execute()` or `session.scalars()`), the `result` object may be a `Result` specialized for ORM queries, such as `ChunkedIteratorResult` for `session.execute()` or `ScalarResult` for `session.scalars()`. Additional methods include:

- `result.scalars()`: Returns a `ScalarResult` object, which yields scalar values (typically the first column or ORM objects) instead of full rows.
  ```python
  scalar_result = result.scalars()  # Yields scalar values
  for value in scalar_result:
      print(value)
  ```
- `result.unique()`: As mentioned, ensures unique ORM objects, especially useful when joins cause duplicates.
  ```python
  unique_objects = result.unique().all()  # List of unique ORM objects
  ```

### Core vs. ORM Considerations
- **Core Queries**: When using `engine.execute()` or `connection.execute()`, the `result` is typically a `CursorResult`. Methods like `fetchall()`, `fetchmany()`, and `rowcount` are more commonly used.
- **ORM Queries**: When using `session.execute()` or `session.scalars()`, the `result` is often a `Result` or `ScalarResult`, and methods like `scalar_one()`, `one_or_none()`, and `scalars()` are more relevant.
- **Context Managers**: Results are often used in context managers, which automatically handle closing:
  ```python
  with engine.execute(query) as result:
      rows = result.fetchall()
  ```
