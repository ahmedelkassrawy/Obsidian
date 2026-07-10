### **Q8: How many index lookups will the following query perform?**

**Query**: SELECT * FROM sales WHERE id = 5;

**Analysis**:

- The table has a clustered index on id (primary key), which means the data is physically stored in the order of id.
- The query filters on id = 5, so the database performs a **clustered index seek** to locate the row where id = 5.
- Since SELECT * retrieves all columns, and the clustered index leaf nodes contain the entire row (all columns), no additional lookups are needed.
- Only **1 index operation** (the clustered index seek) is performed.

**Answer**: **1 index lookup**.

### **Q9: How many index lookups will the following query perform?**

**Query**: SELECT * FROM sales WHERE rental_date = '2021-01-01';

**Analysis**:

- There is a non-clustered B-tree index on rental_date.
- The query filters on rental_date = '2021-01-01', so the database performs a **non-clustered index seek** on the rental_date index to find matching rows. This index contains rental_date and references to the clustered index key (id).
- SELECT * requires all columns (id, rental_date, inventory_id, customer_id), but the non-clustered index on rental_date only contains rental_date and id.
- To retrieve the remaining columns (inventory_id, customer_id), the database performs a **key lookup** (clustered index seek) for each matching row using the id values from the non-clustered index.
- Total lookups:
    - **1 non-clustered index seek** on rental_date.
    - **N clustered index seeks** (key lookups), where N is the number of rows matching rental_date = '2021-01-01'.
- Since the question asks for a general number and doesn’t specify row count, let’s assume a single row matches for simplicity (a common assumption in such questions).

**Answer**: **2 index lookups** (1 non-clustered index seek + 1 key lookup for a single row).

---

### **Q10: How many index lookups will the following query perform?**

**Query**: SELECT inventory_id FROM sales WHERE rental_date = '2021-01-01';

**Analysis**:

- - The non-clustered index is **(rental_date, inventory_id)**.
- **Both** the filter (`rental_date`) and the selected column (`inventory_id`) are in the **secondary index itself**!
- **No need for key lookup** at all.

**Answer**: **1 index lookups** 

---

### **Q11: Does the following query need extra optimizations?**

**Query**: SELECT rental_date FROM sales WHERE inventory_id = 126;

**Analysis**:

- There is a non-clustered index on inventory_id.
- The query filters on inventory_id = 126, so the database performs a **non-clustered index seek** on inventory_id to find matching rows.
- The query selects rental_date, which is not in the inventory_id index (it only has inventory_id and id).
- A **key lookup** in the clustered index is needed to fetch rental_date.
- This key lookup is an extra step that can be optimized. If the index on inventory_id were modified to include rental_date (e.g., using INCLUDE in SQL Server or a covering index in MySQL), the key lookup could be avoided, making the query more efficient.

**Answer**: **Yes**, the query needs extra optimization (e.g., create a covering index on inventory_id that includes rental_date).

---

### **Q12: How many index lookups will the following query perform?**

**Query**: SELECT * FROM sales WHERE inventory_id = 126 AND rental_date = '2021-01-01';

**Analysis**:

- The query has a WHERE clause with inventory_id = 126 AND rental_date = '2021-01-01'.
- There are non-clustered indexes on both inventory_id and rental_date.
- The database query optimizer will likely choose one of the indexes to start with (let’s say the inventory_id index, as it’s often more selective for equality conditions):
    - **Non-clustered index seek** on inventory_id = 126 to find matching rows.
    - For each matching row, the database checks the rental_date = '2021-01-01' condition. Since rental_date is not in the inventory_id index, it performs a **key lookup** in the clustered index to fetch rental_date (and the other columns for SELECT *).
- Alternatively, if the optimizer uses the rental_date index first, the process is similar: a seek on rental_date, then a key lookup to check inventory_id and fetch other columns.
- Either way, the steps are:
    - **1 non-clustered index seek** on one of the indexes.
    - **N clustered index seeks** (key lookups) for N matching rows to fetch all columns and evaluate the second condition.
- Assuming a single row matches for simplicity.

**Answer**: **2 index lookups** (1 non-clustered index seek + 1 key lookup for a single row).

---
Thread -> Each thread has its **own stack space** but **share** (global variables , heap and code segment)

Processes -> DON'T share data where each process has its own address space, heap, stack, global variables, code (even if its the same program each has its own memory copy)
**Processes can share data** if we **explicitly** set it up, using **Inter-Process Communication (IPC)** mechanisms

- `COUNT(*)` = counts **everything** (nulls, non-nulls, etc).
- `COUNT(column_name)` = counts **only non-null** values.
- `COUNT(DISTINCT column_name)` = counts **distinct non-null** values.
- No rows? Both return **0**.

| Feature            | Stored Procedure                                                                                             | Transaction                                                                                           |
| ------------------ | ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| **Definition**     | A **named** saved program in the database that contains SQL statements and control logic (IFs, loops, etc.). | A **unit of work** that groups SQL operations together — they succeed or fail as a whole.             |
| **Purpose**        | **Organize and reuse logic** (e.g., complex calculations, reports, business rules).                          | **Ensure atomicity** — all operations succeed or none do (ACID property).                             |
| **Control**        | Controls **logic and flow** of SQL execution (can even have multiple transactions inside).                   | Controls **data integrity** — ensures database stays consistent even on failure.                      |
| **Scope**          | Stored procedure may contain **0, 1, or multiple** transactions.                                             | A transaction **wraps around** a set of SQL statements (can be inside or outside a stored procedure). |
| **Usage**          | You create it once (`CREATE PROCEDURE`) and **call** it many times (`CALL procedure_name`).                  | You **start** (`BEGIN`), **end** (`COMMIT`) or **cancel** (`ROLLBACK`) each transaction.              |
| **Atomic?**        | No, unless you program it to use transactions inside.                                                        | Yes, **atomic** by design. All or nothing.                                                            |
| **Visibility**     | Stored procedures are database **objects** (listed in the system catalog).                                   | Transactions are **runtime events**, not stored.                                                      |
| **Error Handling** | Can have custom error handlers inside the procedure.                                                         | If error inside a transaction — usually leads to a **ROLLBACK**.                                      |
A stored procedure is like a **machine** you build to automate tasks.
If two stored procedures update the same tables in different orders — deadlocks can happen.