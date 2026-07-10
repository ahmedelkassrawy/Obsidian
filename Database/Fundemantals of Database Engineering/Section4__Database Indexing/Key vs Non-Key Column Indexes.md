**indexes are default ordered**
## Key Column Indexes

- **Definition**: Indexes on columns with constraints like **primary key**, **unique key**, or **foreign key**.
- **Purpose**:
    - Enforce **uniqueness** (primary/unique keys) or **referential integrity** (foreign keys).
    - Optimize queries (e.g., `WHERE`, `JOIN`, `ORDER BY`) on key columns.
- **Characteristics**:
    - **Automatic**: Created when defining primary/unique keys (e.g., `PRIMARY KEY` or `UNIQUE`).
    - **No NULLs** in primary keys; unique keys may allow NULLs (database-dependent).
    - Typically **B-tree** for efficient lookups.
    - Cannot contain duplicates (for primary/unique keys).
- **Example**:
    
    ```sql
    CREATE TABLE users (
        user_id INT PRIMARY KEY, -- Auto-indexed
        email VARCHAR(100) UNIQUE -- Unique index
    );
    ```
    
- **Use Case**: Fast lookups/joins on `user_id` or `email`, ensuring no duplicate emails.

## Non-Key Column Indexes

- **Definition**: Indexes on columns without constraints, created for query performance.
- **Purpose**:
    - Speed up `SELECT`, `WHERE`, `JOIN`, `GROUP BY` on non-constrained columns.
    - Can include **covering columns** to avoid table access (e.g., SQL Server’s `INCLUDE`).
- **Characteristics**:
    - **Manual**: Explicitly created (e.g., `CREATE INDEX`).
    - Allows **NULLs** and **duplicates**.
    - Types: **B-tree**, **hash**, **GIN**, etc., based on query needs.
    - Flexible for any frequently queried column.
- ### **When to Use This Index**
	- Create this index if:
    - Queries frequently filter or sort on g (e.g., WHERE g = 'A' or ORDER BY g).
    - Queries often select id alongside g.
    - The students table is large, making table scans costly.
- **Example**:
    
    ```sql
    CREATE TABLE orders (
        order_id INT PRIMARY KEY,
        customer_id INT,
        order_date DATE
    );
    CREATE INDEX idx_customer ON orders(customer_id); -- Non-key index
    ```
    
    With included columns (SQL Server):
    
    ```sql
    CREATE INDEX g_idx ON students(g) INCLUDE (id);
    ```
    - **Without the Index**: A query like SELECT id FROM students WHERE g = 'A' might scan the entire table, which is slow for large datasets.
	- **With the Index**: The g_idx index lets the database jump to rows where g = 'A' and grab id from the index directly.
- **Use Case**: Optimize queries like:
    
    ```sql
    SELECT id FROM students WHERE g = 'A';
    ```
    

## Covering Indexes (Non-Key)

- **Definition**: Non-key index that includes extra columns to "cover" query needs.
- **Purpose**: Retrieve all query data (e.g., `SELECT` columns) from the index, avoiding table lookups.
- **Example**:
    
    ```sql
    CREATE INDEX idx_customer_date ON orders(customer_id, order_date) INCLUDE (total_amount);
    ```
    
    - **Key Columns**: `customer_id`, `order_date` (for `WHERE`, `ORDER BY`).
    - **Included Column**: `total_amount` (for `SELECT`).
    - Query: `SELECT total_amount FROM orders WHERE customer_id = 123 ORDER BY order_date;`
- **Benefit**: Faster execution by reducing I/O.

## Key Differences

|**Aspect**|**Key Column Index**|**Non-Key Column Index**|
|---|---|---|
|**Purpose**|Constraints + performance|Performance only|
|**Uniqueness**|Enforces uniqueness|No uniqueness enforced|
|**Creation**|Automatic for keys|Manual|
|**NULLs/Duplicates**|No NULLs (primary); unique key varies|Allows NULLs/duplicates|
|**Use Case**|Joins, constrained lookups|Frequent searches on any column|

## Trade-Offs

- **Pros**:
    - Both improve query speed.
    - Key indexes ensure data integrity.
    - Non-key indexes (with `INCLUDE`) can cover queries fully.
- **Cons**:
    - Increase **storage** (indexes store data).
    - Slow **INSERT/UPDATE/DELETE** due to index maintenance.
    - Over-indexing harms performance; analyze queries first.

## Notes

- **Key Indexes**: Use for columns needing uniqueness (e.g., `user_id`) or joins (e.g., foreign keys).
- **Non-Key Indexes**: Use for frequent filters (e.g., `WHERE status = 'active'`) or sorts.
- **Covering Indexes**: Add `INCLUDE` (SQL Server) for columns only in `SELECT` to make queries faster.
- Check database support (e.g., SQL Server’s `INCLUDE` vs. MySQL’s multi-column indexes).

## Example Queries

- Key Index:
    
    ```sql
    SELECT * FROM users WHERE user_id = 101;
    ```
    
- Non-Key Index:
    
    ```sql
    SELECT id, g FROM students WHERE g = 'A';
    ```
    
- Covering Index:
    
    ```sql
    SELECT id FROM students WHERE g = 'B'; -- Uses g_idx with INCLUDE (id)
    ```
    

---

**Tags**: #Database #Indexing #SQL #Performance