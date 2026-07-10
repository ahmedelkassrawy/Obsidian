# MyISAM Storage Engine

## Overview
- **Full Name**: Indexed Sequential Access Method (MyISAM).
- **Key Feature**: Everything is indexed; indexes point directly to the row on disk (via offsets).
- **Advantages**: Fast access and searches.
- **Disadvantages**: Can be problematic due to direct pointing, leading to issues with updates/deletes.

## Underlying Structure
- **B-Tree Based**: A computer science data structure for storing data on disk.
  - Allows very fast searches.
  - "B" likely stands for "Balanced Tree" (not binary tree, as it supports multiple nodes).
  - You can specify the number of nodes.
- Separate video planned on B-Trees vs. LSM Trees.

## Data Handling
- **Indexes and Data**: Indexes point directly to the disk offset where the row exists.
- **Inserts**: Fast, as they append to the end of the file (easy to find the end).
- **Updates/Deletes**: Problematic and slow.
  - Cause fragmentation.
  - Change row sizes, which alters offsets.
  - Requires updating all indexes pointing to that row (expensive operation).

## Transactional Support
- **No Built-in Transactions**: Does not support ACID properties natively.
  - Cannot perform atomic operations like debiting one account and crediting another in a single transaction.
  - Dangerous for applications like banking.
- **Workaround**: Atomicity can be built at the database layer (possible but not inherent to MyISAM).
- **Practical Demo**: Upcoming video will show lack of transaction support.

## History and Ownership
- **Origins**: Created by a Swedish company (possibly Sleepycat, but uncertain).
- **Acquisitions**:
  - Bought by Sun Microsystems.
  - Then Oracle acquired Sun, gaining ownership of MyISAM, MySQL, etc.
- **Community Response**: Once Oracle took over, people started forking MySQL to create alternatives (e.g., MariaDB, PerconaDB).
  - Open source, but ownership changes led to dissatisfaction.

## Reliability Issues
- **Corruption on Crashes**: Tables can corrupt during long inserts/updates if the database crashes.
  - Personal experience: Faced this with LAMP stack (Linux/Apache/MySQL/PHP) or similar (e.g., WAMP on Windows).
  - Indexes pointing directly to rows make it vulnerable; any out-of-sync updates lead to issues.
- **Repair**: There's a repair utility to fix corrupted tables.
- **Why Prone to Corruption**: Multiple indexes must be updated; any failure disrupts the structure.

## Locking Mechanism
- **Table-Level Locking**: Locks the entire table during writes.
  - Prevents concurrent edits, even on unrelated rows.
  - Slows down writes with multiple users.
- **No Row-Level Locking**: Cannot lock just a specific row.
- **Comparison**: InnoDB supports row-level locking.

## Usage and Evolution in MySQL
- **Supported Databases**: MySQL, MariaDB, PerconaDB (all MySQL-compatible).
- **Default Engine**: Was the default in MySQL until version 5.5.
- **Shift to InnoDB**: After 5.5, InnoDB became default due to better features:
  - Transaction support.
  - Row-level locking.
  - Foreign keys.
  - Pushes advanced functionality to the storage engine level for easier database building.

## When to Use MyISAM
- Suitable for read-heavy workloads with fast inserts (no transactions needed).
- Avoid for write-heavy or transaction-critical applications.

## Notes for Study
- **Pros**:
  - Fast inserts (append-only).
  - Fast searches via B-Tree indexes.
- **Cons**:
  - Slow updates/deletes due to index updates and fragmentation.
  - No transactions/ACID.
  - Table-level locking.
  - Prone to corruption.
- **Alternatives**: Switch to InnoDB for modern needs.