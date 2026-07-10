**Two-Phase Locking (2PL)** is a concurrency control mechanism used in database systems to ensure serializability of transactions. It consists of two phases:

1. **Growing Phase**: A transaction acquires all the locks it needs without releasing any.
2. **Shrinking Phase**: The transaction releases all locks without acquiring new ones.

This ensures that transactions do not interfere with each other, preventing issues like double booking.

### Example of Double Booking with Two-Phase Locking

**Scenario**: Consider an airline reservation system with a single seat (Seat 1A) available on a flight. Two customers, Alice and Bob, attempt to book Seat 1A simultaneously through two transactions, T1 (Alice) and T2 (Bob). Without proper concurrency control, both might book the same seat, causing a double booking. Two-Phase Locking prevents this.

#### Without Two-Phase Locking (Double Booking Issue)
- T1 checks if Seat 1A is available (it is).
- T2 checks if Seat 1A is available (still appears available).
- T1 books Seat 1A (marks it as reserved).
- T2 also books Seat 1A (overwrites T1’s reservation).
- **Result**: Seat 1A is double-booked for Alice and Bob.

#### With Two-Phase Locking
Each transaction must acquire a lock on Seat 1A before accessing it. Assume a shared lock (S) for reading and an exclusive lock (X) for writing.

1. **T1 (Alice’s Transaction)**:
   - **Growing Phase**:
     - Requests a shared lock (S) on Seat 1A to check availability. Lock granted.
     - Sees Seat 1A is available.
     - Requests an exclusive lock (X) on Seat 1A to book it. Lock granted (upgrades S to X).
     - Marks Seat 1A as reserved for Alice.
   - **Shrinking Phase**:
     - Commits the transaction and releases all locks (S and X).

2. **T2 (Bob’s Transaction)**:
   - **Growing Phase**:
     - Requests a shared lock (S) on Seat 1A to check availability.
     - Since T1 holds an exclusive lock (X), T2 is blocked and waits.
     - Only after T1 commits and releases the lock can T2 proceed.
     - T2 acquires the shared lock, checks Seat 1A, and finds it reserved.
     - T2 cannot book Seat 1A and aborts or tries another seat.
   - **Shrinking Phase**:
     - T2 releases any locks it acquired.

#### Outcome
- T1 successfully books Seat 1A.
- T2 is prevented from booking the same seat because 2PL ensures T2 cannot access Seat 1A until T1 completes.
- **No double booking occurs**.

### Key Points
- **Lock Types**: Shared locks allow multiple transactions to read; exclusive locks ensure only one transaction can write.
- **Prevention of Double Booking**: 2PL ensures that once a transaction locks a resource for writing (e.g., booking a seat), no other transaction can access it until the lock is released.
- **Potential Drawback**: 2PL can lead to deadlocks (e.g., if T1 and T2 lock different seats and wait for each other). Deadlock detection or prevention mechanisms are needed.

This example illustrates how 2PL maintains data consistency in concurrent environments like booking systems.
# Preventing Double Booking in SQL

## Scenario

An airline reservation system has a table `seats` with columns `seat_number` and `is_reserved`. Two transactions (T1 and T2) attempt to book the same seat (`seat_1A`). We'll use SQL to enforce Two-Phase Locking (2PL) and prevent double booking.

## Table Setup

```sql
CREATE TABLE seats (
    seat_number VARCHAR(10) PRIMARY KEY,
    is_reserved BOOLEAN DEFAULT FALSE
);
INSERT INTO seats (seat_number, is_reserved) VALUES ('seat_1A', FALSE);
```

## Applying 2PL in SQL

We simulate two transactions (T1 and T2) trying to book `seat_1A`. We use a transaction with explicit locking and a `SERIALIZABLE` isolation level to enforce 2PL.

### Transaction T1 (Alice’s Booking)

```sql
BEGIN;
-- Set isolation level to SERIALIZABLE to ensure strict 2PL
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- Growing Phase: Acquire a shared lock to check availability
SELECT is_reserved FROM seats WHERE seat_number = 'seat_1A' FOR SHARE; -- Explicit shared lock (optional, ensures read lock)
-- Check if seat is available
SELECT is_reserved FROM seats WHERE seat_number = 'seat_1A' AND is_reserved = FALSE;
-- Growing Phase: Acquire an exclusive lock to reserve the seat
UPDATE seats SET is_reserved = TRUE WHERE seat_number = 'seat_1A' AND is_reserved = FALSE;
-- Shrinking Phase: Commit to release all locks
COMMIT;
```

### Transaction T2 (Bob’s Booking, Running Concurrently)

```sql
BEGIN;
-- Set isolation level to SERIALIZABLE
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- Growing Phase: Attempt to acquire a shared lock
SELECT is_reserved FROM seats WHERE seat_number = 'seat_1A' FOR SHARE;
-- If T1 hasn’t committed, T2 waits due to T1’s exclusive lock
-- Once T1 commits, T2 sees the seat is reserved
SELECT is_reserved FROM seats WHERE seat_number = 'seat_1A' AND is_reserved = FALSE;
-- No rows returned (seat is reserved), so T2 cannot book
-- Optionally, T2 can try another seat or abort
ROLLBACK;
```

## How 2PL is Enforced

1. **Growing Phase**:
    - The `SELECT ... FOR SHARE` or `FOR UPDATE` acquires a shared or exclusive lock early.
    - The `UPDATE` statement implicitly acquires an exclusive lock on the row being modified.
    - With `SERIALIZABLE` isolation, the database ensures that all necessary locks (even range locks for phantom reads) are acquired before proceeding.
2. **Shrinking Phase**:
    - Locks are held until the `COMMIT` or `ROLLBACK` is executed.
    - The database automatically releases all locks at the end of the transaction, ensuring no new locks are acquired after releasing any.
3. **Concurrency Control**:
    - If T2 tries to access `seat_1A` while T1 holds an exclusive lock (from the `UPDATE`), T2 is blocked until T1 commits or rolls back.
    - If T1 reserves the seat, T2 sees `is_reserved = TRUE` and cannot book it, preventing double booking.

## Key SQL Features for 2PL

- **Transaction Isolation Levels**:
    - `SERIALIZABLE`: Ensures strict 2PL by locking all accessed resources (rows, ranges) until the transaction ends. Best for preventing double booking.
    - `REPEATABLE READ`: Prevents non-repeatable reads but may allow phantom reads. Still suitable for many 2PL scenarios.
    - Use `SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;` at the start of the transaction.
- **Explicit Locking**:
    - `SELECT ... FOR UPDATE`: Acquires an exclusive lock on selected rows, preventing other transactions from reading or writing them.
    - `SELECT ... FOR SHARE`: Acquires a shared lock, allowing reads but preventing writes by others.
    - Example: `SELECT * FROM seats WHERE seat_number = 'seat_1A' FOR UPDATE;`

## Summary

To apply 2PL in SQL:

1. Use `BEGIN`, `COMMIT`, and `ROLLBACK` to define transactions.
2. Set `SERIALIZABLE` or use `FOR UPDATE`/`FOR SHARE` to enforce locks.
3. Ensure locks are held until commit (handled by the database).
4. Handle deadlocks and serialization failures in your application logic.