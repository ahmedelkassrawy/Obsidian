## Best Practices for SQL Connection Pooling and Permissions in a Node.js/PostgreSQL To-Do App

## Overview

This study covers best practices for securing database interactions in a Node.js application with a PostgreSQL backend, focusing on connection pooling and user permissions. The example uses a simple to-do application with REST API routes for reading, creating, and deleting to-dos, highlighting common mistakes and their solutions.

## Application Context

- **Application**: Simple to-do app with:
    - **Frontend**: HTML5 interface for adding and deleting to-dos.
    - **Backend**: Node.js with PostgreSQL (using `pg` library).
    - **Database**: `todos` table with columns `id` (SERIAL PRIMARY KEY) and `text` (TEXT).
    - **Routes**:
        - Read: `SELECT * FROM todos`.
        - Create: `INSERT INTO todos (text) VALUES ($1)`.
        - Delete: `DELETE FROM todos WHERE id = $1`.
- **Issues Identified**:
    - Using an admin user (`postgres`) with full privileges for all operations.
    - Hardcoding database credentials in code.
    - Unbounded queries (e.g., `SELECT * FROM todos` without `LIMIT`).
    - Lack of proper error handling for user feedback.
    - Insufficient permission granularity for database users.

## Key Concepts

1. **Connection Pooling**:
    
    - **Purpose**: Manages multiple database connections to handle concurrent queries efficiently.
    - **Why Use Pooling**:
        - Avoids issues with single TCP connections where query order cannot be guaranteed due to pipelining.
        - Allows reserving a connection for a query and releasing it back to the pool after completion.
    - **Implementation**: Using the `pg` library’s `Pool` class in Node.js.
    - **Configuration**: Pools can be configured with a minimum/maximum number of connections based on workload (e.g., more connections for read-heavy routes).
2. **Principle of Least Privilege**:
    
    - Assign specific permissions to database users based on their role (e.g., read, insert, delete).
    - Prevents catastrophic actions (e.g., `DROP TABLE`) via SQL injection.
    - Example: A read-only user cannot modify data, reducing damage from potential attacks.
3. **Security Risks of Admin User**:
    
    - Using the `postgres` admin user for application queries grants full privileges (e.g., `DROP`, `CREATE`).
    - SQL injection could allow attackers to destroy the database (e.g., `SELECT * FROM todos WHERE id = 1; DROP TABLE todos;`).
4. **Sequences and Permissions**:
    
    - SERIAL columns (e.g., `id`) rely on a sequence to generate unique values.
    - Insert operations require `USAGE` permission on the sequence, not just `SELECT` or `INSERT` on the table.
    - Example: `GRANT USAGE ON SEQUENCE todos_id_seq TO db_create;`.

## Experiment and Fixes

### Initial Issues

- **Admin User**: The app used the `postgres` user for all operations, posing a security risk.
- **Hardcoded Credentials**: Passwords were hardcoded in the code, increasing exposure risk.
- **Unbounded Query**: `SELECT * FROM todos` could return millions of rows, causing performance issues.
- **Error Handling**: Errors were not properly communicated to the client, leading to poor user experience.
- **Permission Errors**:
    - Insert failed due to missing `USAGE` permission on the sequence.
    - Delete failed because the user lacked `SELECT` permission to identify rows.

### Solutions Implemented

1. **Separate Connection Pools**:
    
    - Created three pools for different routes:
        - `db_read_pool`: For reading to-dos (`SELECT`).
        - `db_create_pool`: For inserting to-dos (`INSERT`).
        - `db_delete_pool`: For deleting to-dos (`DELETE`).
    - Each pool uses a distinct database user with limited permissions.
2. **Database User Creation**:
    
    - Created three users with specific roles:
        
        ```sql
        -- Read-only user
        CREATE ROLE db_read WITH LOGIN PASSWORD 'db_read';
        GRANT SELECT ON todos TO db_read;
        
        -- Create user
        CREATE ROLE db_create WITH LOGIN PASSWORD 'db_create';
        GRANT INSERT ON todos TO db_create;
        GRANT USAGE ON SEQUENCE todos_id_seq TO db_create;
        
        -- Delete user
        CREATE ROLE db_delete WITH LOGIN PASSWORD 'db_delete';
        GRANT DELETE, SELECT ON todos TO db_delete;
        ```
        
    - **Notes**:
        - `db_read`: Only `SELECT` permission for reading.
        - `db_create`: `INSERT` on table and `USAGE` on sequence (required for SERIAL column).
        - `db_delete`: `DELETE` and `SELECT` (to identify rows for deletion).
        - Users are not superusers and cannot create databases or roles.
3. **Table Ownership**:
    
    - The `todos` table is owned by the `postgres` user to prevent application users from having excessive privileges.
    - Example:
        
        ```sql
        -- Table creation (run by postgres user)
        CREATE TABLE todos (
          id SERIAL PRIMARY KEY,
          text TEXT NOT NULL
        );
        ```
        
4. **Error Handling**:
    
    - Avoided exposing raw database errors to clients to prevent leaking sensitive information (e.g., source code, line numbers).
    - Returned generic success/failure responses (e.g., `true`/`false`) and logged errors server-side.
    - Client-side fix: Updated the frontend to display failure messages when delete operations fail.
5. **Sequence Permission Fix**:
    
    - Insert failure occurred because `db_create` lacked `USAGE` permission on the `todos_id_seq` sequence.
    - Fixed by granting:
        
        ```sql
        GRANT USAGE ON SEQUENCE todos_id_seq TO db_create;
        ```
        
    - **Lesson**: `SELECT` on a sequence is not enough; `USAGE` is required to generate the next value.
6. **Delete Permission Fix**:
    
    - Delete failure occurred because `db_delete` needed `SELECT` to identify rows.
    - Fixed by granting:
        
        ```sql
        GRANT SELECT ON todos TO db_delete;
        ```
        

## Code Example (Node.js)

```javascript
const { Pool } = require('pg');

// Read pool
const db_read_pool = new Pool({
  user: 'db_read',
  password: 'db_read',
  database: 'todos_db',
  host: 'localhost',
  port: 5432
});

// Create pool
const db_create_pool = new Pool({
  user: 'db_create',
  password: 'db_create',
  database: 'todos_db',
  host: 'localhost',
  port: 5432
});

// Delete pool
const db_delete_pool = new Pool({
  user: 'db_delete',
  password: 'db_delete',
  database: 'todos_db',
  host: 'localhost',
  port: 5432
});

// Read to-dos
async function readTodos() {
  try {
    const result = await db_read_pool.query('SELECT id, text FROM todos LIMIT 10');
    return result.rows;
  } catch (e) {
    console.error(e);
    return false;
  }
}

// Create to-do
async function createTodo(text) {
  try {
    await db_create_pool.query('INSERT INTO todos (text) VALUES ($1)', [text]);
    return true;
  } catch (e) {
    console.error(e);
    return false;
  }
}

// Delete to-do
async function deleteTodo(id) {
  try {
    await db_delete_pool.query('DELETE FROM todos WHERE id = $1', [id]);
    return true;
  } catch (e) {
    console.error(e);
    return false;
  }
}

// Initialize pools
async function connectPools() {
  await Promise.all([
    db_read_pool.connect(),
    db_create_pool.connect(),
    db_delete_pool.connect()
  ]);
}

// Client-side (example)
document.getElementById('delete-btn').addEventListener('click', async () => {
  const response = await fetch(`/api/todos/${id}`, { method: 'DELETE' });
  const result = await response.json();
  if (!result.success) {
    alert('Failed to delete to-do');
  }
});
```

## Best Practices Highlighted

1. **Avoid Admin Users in Applications**:
    
    - Never use the `postgres` user for application queries.
    - Use dedicated users with minimal permissions.
2. **Use Connection Pooling**:
    
    - Create separate pools for different operations (read, write, delete).
    - Configure pool size based on workload (e.g., more connections for reads).
3. **Secure Credentials**:
    
    - Store database credentials in environment variables or a key vault, not in source code.
    - Example:
        
        ```javascript
        require('dotenv').config();
        const db_read_pool = new Pool({
          user: process.env.DB_READ_USER,
          password: process.env.DB_READ_PASSWORD,
          database: process.env.DB_NAME,
          host: process.env.DB_HOST,
          port: process.env.DB_PORT
        });
        ```
        
4. **Bound Queries**:
    
    - Always use `LIMIT` or pagination for `SELECT` queries to avoid fetching millions of rows.
    - Example: `SELECT * FROM todos LIMIT 10 OFFSET 0`.
5. **SQL Injection Prevention**:
    
    - Use parameterized queries (e.g., `$1`) to sanitize inputs.
    - Example: `INSERT INTO todos (text) VALUES ($1)`.
6. **Error Handling**:
    
    - Log errors server-side but return generic responses to clients.
    - Example: Return `{ success: false }` instead of raw error details.
7. **Sequence Permissions**:
    
    - Grant `USAGE` on sequences for users performing `INSERT` on tables with SERIAL columns.
    - Example: `GRANT USAGE ON SEQUENCE todos_id_seq TO db_create;`.

## Lessons Learned

- **Permission Granularity**: Assigning specific permissions (e.g., `SELECT`, `INSERT`, `DELETE`) to separate users enhances security.
- **Sequence Gotcha**: Inserting into a table with a SERIAL column requires `USAGE` on the sequence, not just `INSERT` on the table.
- **Client Feedback**: Proper error handling improves user experience by clearly indicating operation failures.
- **Debugging**: Tools like PgAdmin and breakpoints are essential for diagnosing permission issues.

## Questions for Further Study

- How do you configure connection pool sizes for high-traffic applications?
- What are the trade-offs of using multiple database users vs. a single user with role-based access?
- How can environment variables or key vaults be integrated into a Node.js application securely?
- What are the performance implications of sequences in high-concurrency environments?
- How do you implement pagination effectively for large datasets?