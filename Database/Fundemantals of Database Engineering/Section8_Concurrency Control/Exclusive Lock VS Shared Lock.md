### **Exclusive Lock (X Lock)**
- **Definition**: Grants exclusive access to a resource (e.g., a table or row) to a single transaction. No other transaction can read or write the locked resource until the lock is released.
- **Purpose**: Used for operations that modify data (e.g., INSERT, UPDATE, DELETE) to prevent concurrent modifications or reads that could lead to inconsistencies.
- **Example**:
  - Transaction T1 wants to update a customer's balance in a bank database.
    ```sql
    UPDATE accounts SET balance = balance - 100 WHERE account_id = 123;
    ```
    - T1 acquires an **exclusive lock** on the row for `account_id = 123`. No other transaction (e.g., T2) can read or modify this row until T1 commits or rolls back.
    - If T2 tries to read or update the same row, it waits until T1 releases the lock.

### **Shared Lock (S Lock)**
- **Definition**: Allows multiple transactions to read a resource simultaneously but prevents any transaction from modifying it. Write operations require an exclusive lock, so they wait until all shared locks are released.
- **Purpose**: Used for read-only operations (e.g., SELECT) to ensure data consistency while allowing concurrent reads.
- **Example**:
  - Transaction T1 and T2 both want to read the balance of a customer's account.
    ```sql
    SELECT balance FROM accounts WHERE account_id = 123;
    ```
    - Both T1 and T2 acquire a **shared lock** on the row for `account_id = 123`. They can read the data simultaneously.
    - If T3 tries to update the same row (requiring an exclusive lock), it waits until T1 and T2 release their shared locks.

### **Key Differences**
| **Aspect**            | **Shared Lock (S)**                     | **Exclusive Lock (X)**                  |
|-----------------------|----------------------------------------|----------------------------------------|
| **Access**            | Multiple transactions can read.        | Only one transaction can access (read/write). |
| **Operations**        | Read-only (e.g., SELECT).              | Read and write (e.g., UPDATE, INSERT). |
| **Concurrency**       | Allows concurrent reads.               | Blocks all other transactions.         |
| **Compatibility**     | Compatible with other shared locks.    | Incompatible with any lock (S or X).   |

### **Real-World Analogy**
- **Shared Lock**: Like borrowing a book from a library to read. Multiple people can read the same book (if multiple copies exist or they share), but no one can edit the book's content while it's being read.
- **Exclusive Lock**: Like checking out a book to edit its content (e.g., adding notes). Only one person can have it, and no one else can read or edit it until it's returned.

### **Lock Compatibility Matrix**
| **Requested \ Held** | **No Lock** | **Shared (S)** | **Exclusive (X)** |
|-----------------------|-------------|----------------|-------------------|
| **Shared (S)**        | ✅          | ✅             | ❌                |
| **Exclusive (X)**     | ✅          | ❌             | ❌                |

- ✅: Lock can be granted.
- ❌: Lock cannot be granted (transaction waits).

### **Practical Example in a Database**
- **Scenario**: A bank database with an `accounts` table.
  - **Transaction T1 (Read)**:
    ```sql
    BEGIN TRANSACTION;
    SELECT balance FROM accounts WHERE account_id = 123; -- Acquires shared lock
    COMMIT;
    ```
    - T1 gets a shared lock, allowing other transactions to read the same row.
  - **Transaction T2 (Update)**:
    ```sql
    BEGIN TRANSACTION;
    UPDATE accounts SET balance = balance + 50 WHERE account_id = 123; -- Requests exclusive lock
    COMMIT;
    ```
    - T2 requests an exclusive lock but waits if T1's shared lock is active. Once T1 commits, T2 gets the exclusive lock and updates the row.
  - **Transaction T3 (Read)**:
    ```sql
    SELECT balance FROM accounts WHERE account_id = 123; -- Acquires shared lock
    ```
    - T3 can read the row if T1 has a shared lock (compatible), but it waits if T2 has an exclusive lock.

### Quick Comparison

| Clause             | Lock Type     | Allows Other Reads?                  | Allows Other Writes? | Typical Use Case                    |
| ------------------ | ------------- | ------------------------------------ | -------------------- | ----------------------------------- |
| **FOR** **UPDATE** | Exclusive (X) | Limited (depends on isolation level) | No                   | Lock rows before updating/deleting  |
| **FOR SHARE**      | Shared (S)    | Yes                                  | No                   | Read rows and prevent modifications |


### **Deadlock Consideration**
- Locks can lead to deadlocks if not managed properly. For example:
  - T1 holds an exclusive lock on row A and waits for a shared lock on row B.
  - T2 holds a shared lock on row B and waits for an exclusive lock on row A.
  - **Result**: Deadlock. The database detects this and aborts one transaction.

A deadlock is a situation in computing where two or more processes or threads are unable to proceed because each is waiting for the other to release a resource, creating a cycle of dependencies.
example, Process A holds Resource 1 and waits for Resource 2, while Process B holds Resource 2 and waits for Resource 1, causing both to stall indefinitely.