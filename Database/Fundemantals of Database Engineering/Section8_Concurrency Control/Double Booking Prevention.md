## Overview
## Original Approach: `SELECT ... FOR UPDATE`

- **Method**: Uses `SELECT ... FOR UPDATE` to explicitly lock a row, ensuring serialized transactions.
- **Purpose**: Prevents two users from booking the same seat by acquiring an exclusive lock until the transaction commits.
- **Advantages**:
    - Provides full control over transaction isolation.
    - Ensures predictable behavior across databases.

## Alternative Approach: Direct `UPDATE`

- **Method**: Issues an `UPDATE` statement with a condition (`WHERE id=1 AND is_booked=0`) to book a seat, then checks the result.
- **How It Works**:
    - **Transaction Example**:
        - Transaction 1: Updates seat (ID=1) to `is_booked=1` for user Hussein, implicitly acquiring an exclusive lock.
        - Transaction 2: Attempts to update the same seat for user Rick but is blocked due to the lock.
        - When Transaction 1 commits, PostgreSQL refreshes the row data in Transaction 2, sees `is_booked=1`, and prevents the update.
    - **Key Mechanism**: Relies on PostgreSQL’s row-level locking and `READ COMMITTED` isolation level, which refreshes row data after a commit.
- **Dependencies**:
    - Works in PostgreSQL due to its lock management and heap storage of lock information.
    - May not work consistently in other databases (e.g., MySQL, SQL Server) due to different implementations.

## Key Technical Insights

- **Locking**:
    - `UPDATE` implicitly acquires an **exclusive lock**, unlike the explicit lock in `SELECT ... FOR UPDATE`.
    - PostgreSQL stores lock information in the row itself, checked when accessing the heap.
- **Isolation Levels**:
    - `READ COMMITTED` allows Transaction 2 to see updated row values after Transaction 1 commits, preventing double booking.
    - Other isolation levels or databases may yield different results.
- **Indexing**:
    - Queries use a B-tree index to locate the row (`id=1`), but heap access reveals lock status and updated values.
    - Combined indexes (e.g., on `id` and `is_booked`) could alter behavior, potentially bypassing heap checks.
- **Database Implementation**:
    - Behavior depends on database internals (e.g., PostgreSQL refreshes row data, but MySQL/SQL Server may not).
    - Engineers must understand these nuances to ensure reliability.

## Comparison of Approaches

|Aspect|`SELECT ... FOR UPDATE`|Direct `UPDATE`|
|---|---|---|
|**Control**|High (explicit locking, flexible)|Low (relies on implicit database behavior)|
|**Predictability**|Consistent across databases|Database-dependent|
|**Efficiency**|May take unnecessary locks|Potentially more efficient (fewer queries)|
|**Complexity**|Suitable for complex transactions|Limited to simple updates|

## Instructor’s Philosophy

- **Pessimistic vs. Optimistic Concurrency**:
    - Prefers pessimistic control (locking) to avoid transaction retries and ensure predictable outcomes.
    - Contrasts with optimistic control (e.g., NoSQL databases), which detects conflicts at commit time.

## Conclusion

- The `UPDATE` approach works in PostgreSQL but is less reliable across databases due to implementation differences.
- `SELECT ... FOR UPDATE` is safer and more versatile, especially for complex transactions.
- Engineers should dig into database internals, ask critical questions, and avoid taking behavior at face value to build robust systems.

## Tags

#Database #DoubleBooking #Concurrency #PostgreSQL #Locking #IsolationLevels #DatabaseEngineering