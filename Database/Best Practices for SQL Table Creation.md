##  Best Practices for SQL Table Creation on Application Startup

## Overview

This study addresses a question about whether it's a good practice to run a `CREATE TABLE IF NOT EXISTS` command on application startup in a Node.js application connected to a PostgreSQL database. The discussion focuses on security, permission management, and production-readiness.

## Question Context

- **Source**: Comment by user "Shark Beak" on a Node.js and PostgreSQL video.
- **Setup**: Node.js application connecting to a PostgreSQL database.
- **Question**: Is it a good idea to run `CREATE TABLE IF NOT EXISTS` on application startup to ensure the table exists before the application runs?

## Key Points

- **General Answer**: Running `CREATE TABLE IF NOT EXISTS` on startup is acceptable for non-production environments (e.g., scripts, local development) but is **not recommended** for production due to security and permission concerns.
- **Why It’s Problematic in Production**:
    - The user executing the `CREATE TABLE` command becomes the table owner, granting them full privileges (e.g., `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `DROP`).
    - In a web application, if the same user handles Data Manipulation Language (DML) operations (e.g., `INSERT`, `UPDATE`), an SQL injection attack could allow malicious actions like `DROP TABLE`.
    - Example of SQL injection risk: `SELECT * FROM employees WHERE name = 'x'; DROP TABLE employees; --'`.
- **Security Risks**:
    - Anonymous web users interact with the database through the application user.
    - If the application user has full table privileges, an attacker exploiting SQL injection could destroy the table or data.
- **Production Best Practices**:
    - Separate **schema creation** (Data Definition Language, DDL) from application runtime.
    - Use distinct database users for different purposes to enforce the **principle of least privilege**.
    - Implement connection pooling and assign specific permissions based on application routes.
## Recommended Approach

1. **Schema Creation**:
    
    - Create the database schema (e.g., tables, indexes) using a **dedicated script** run by a **schema owner user** (e.g., `app_schema`).
    - Example:
        
        ```sql
        -- Run as app_schema user
        CREATE TABLE employees (
          id SERIAL PRIMARY KEY,
          name TEXT NOT NULL
        );
        ```
        
    - Execute this script during deployment or setup, not at application runtime.
2. **Application User**:
    
    - Create a separate database user (e.g., `app_user`) for the application to perform DML operations.
    - Grant only necessary permissions to `app_user`:
        
        ```sql
        -- Grant specific permissions
        GRANT SELECT, INSERT, UPDATE ON employees TO app_user;
        ```
        
    - Avoid granting `DROP` or `CREATE` privileges to `app_user`.
3. **Connection Pooling**:
    
    - Use connection pooling to manage database connections efficiently.
    - Create separate connection pools for different application routes based on their needs:
        - **Read-only routes**: Use a user with `SELECT` permissions only (e.g., `read_only_user`).
        - **Write routes**: Use a user with `INSERT`, `UPDATE`, or `DELETE` permissions as needed (e.g., `write_user`).
    - Example:
        
        ```sql
        -- Create read-only user
        CREATE USER read_only_user WITH PASSWORD 'secure_password';
        GRANT SELECT ON employees TO read_only_user;
        
        -- Create write user
        CREATE USER write_user WITH PASSWORD 'secure_password';
        GRANT INSERT, UPDATE ON employees TO write_user;
        ```
        
4. **Benefits of This Approach**:
    
    - **Security**: Limits the damage from SQL injection by restricting user privileges.
    - **Scalability**: Connection pooling optimizes resource usage.
    - **Maintainability**: Separating schema creation from runtime logic simplifies debugging and deployment.

## Non-Production Use Case

- **When `CREATE TABLE IF NOT EXISTS` is Fine**:
    - For scripts or local development where no external users access the application.
    - For idempotent scripts that can run multiple times without causing issues (e.g., setup scripts for testing).
- **Example Use Case**:
    - Running a script to initialize a database for a standalone application with no web exposure.
    - The `CREATE TABLE IF NOT EXISTS` ensures the table is created without errors if it already exists.

## Code Example (Node.js)

```javascript
// Example of separate schema setup (run once during deployment)
const { Pool } = require('pg');
const schemaPool = new Pool({
  user: 'app_schema',
  password: 'schema_password',
  database: 'mydb',
  host: 'localhost',
  port: 5432
});

schemaPool.query(`
  CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
  )
`).then(() => schemaPool.end());

// Application connection pool (runtime)
const appPool = new Pool({
  user: 'app_user',
  password: 'app_password',
  database: 'mydb',
  host: 'localhost',
  port: 5432
});

// Read-only pool
const readPool = new Pool({
  user: 'read_only_user',
  password: 'read_password',
  database: 'mydb',
  host: 'localhost',
  port: 5432
});

// Example query
appPool.query('INSERT INTO employees (name) VALUES ($1)', ['John Doe']);
readPool.query('SELECT * FROM employees');
```

## Key Takeaways

- **Avoid DDL in Application Runtime**: Do not run `CREATE TABLE` or other DDL commands in production application code.
- **Use Least Privilege**: Assign specific permissions to database users based on their role (read, write, schema management).
- **Separate Users**: Use different users for schema creation (`app_schema`) and application operations (`app_user`, `read_only_user`).
- **Connection Pooling**: Implement pools for different routes to optimize performance and security.
- **Idempotent Scripts**: For non-production scripts, `CREATE TABLE IF NOT EXISTS` is useful for idempotency.

