# InnoDB Storage Engine

## Overview
- **Full Name/Pronunciation**: Referred to as "A.B." (likely InnoDB, a transactional database storage engine).
- **Key Feature**: Transactional support (unlike MyISAM, which lacks transactions).
- **Purpose**: Provides ACID compliance for reliable data operations.
- **Replaces MyISAM**: Often recommended as a replacement, but not always; depends on use case (e.g., MyISAM for read-heavy, non-transactional workloads).

## Underlying Structure
- **B+ Tree Based**: Similar to B-Tree but with slight differences; still a balanced tree structure.
- **Primary Key Requirement**:
  - Mandatory in InnoDB (creates a sequential one if not specified).
  - In MyISAM, no primary key required; everything is treated as an index (primary key is just a unique index).
- **Indexing Mechanism**:
  - Primary key points directly to the row (disk offset).
  - Secondary indexes point to the primary key, not directly to the row.
    - This creates extra jumps (round trips) to access the row.
    - Beneficial if querying only primary and secondary keys (avoids full row fetch).
  - In MyISAM, all indexes (including secondary) point directly to the row.

## Data Handling and Performance
- **Queries and Best Practices**:
  - Avoid `SELECT *` (hurts performance; fetches unnecessary data).
  - Be mindful of what you're querying in WHERE clauses.
  - Too many or too few indexes are problematic; balance is key.
  - Understand database internals as a software/database engineer for optimal querying.
- **Inserts/Updates/Deletes**: Transactional, with row-level handling.
- **Use Case Considerations**:
  - InnoDB for transactional needs (e.g., banking operations).
  - MyISAM for read-heavy tables with minimal updates and no transactions (faster inserts in some scenarios).
  - Not a blanket replacement; MyISAM has features where InnoDB may underperform.
- **Appreciation Note**: Learning more about these engines increases respect for their creators; always think critically about technology choices (e.g., don't dismiss older tech like Kerberos without reason).

## Transactional Support
- **ACID Compliant**: Supports Atomicity, Consistency, Isolation, and Durability.
- **Transactions**: Enables safe operations like atomic debits/credits.
- **Foreign Keys**: Supported (links tables for integrity).
  - Speaker's Opinion: Prefers handling relationships in application layer, not via foreign keys.

## Advanced Features
- **Tablespaces**: Concept for organizing storage (e.g., grouping tables by drive or space; similar to Oracle/PostgreSQL/MySQL).
  - Useful for storage arrangement, though potentially a bad idea in some cases.
- **Row-Level Locking**:
  - Locks specific rows during operations (e.g., to serialize updates).
  - Prevents concurrent edits on that row only.
  - Better for concurrency than MyISAM's table-level locking.
- **Spatial Operations**: Supported (unlike early MyISAM; may have been added later to MyISAM).

## History and Ownership
- **Default Engine**: For MySQL (after v5.5), MariaDB, and PerconaDB (speaker uncertain on PerconaDB).
- **Owned by Oracle**: Leads to community concerns.
- **Forks**: MariaDB created XtraDB as a fork of InnoDB (to address ownership issues and add enhancements).

## When to Use InnoDB
- Ideal for applications needing transactions, concurrency, and data integrity.
- Default choice, but evaluate: Doesn't mean it's always the best; think about your specific needs (e.g., read-only tables might prefer MyISAM).
- Speaker's Advice: Always have a reasoned approach; no blanket statements like "never use MyISAM."

## Notes for Study
- **Pros**:
  - Transactional (ACID, foreign keys).
  - Row-level locking for better concurrency.
  - Mandatory primary key for structure.
  - Tablespaces and spatial support.
  - Handles updates/deletes without MyISAM's fragmentation issues (via indirect secondary indexing).
- **Cons**:
  - Extra jumps for secondary indexes (slower in some queries vs. MyISAM's direct pointing).
  - Owned by Oracle (community forks exist).
  - Not ideal for all use cases (e.g., pure read-heavy without transactions).
- **Comparison to MyISAM**:
  - InnoDB: Transactions, row-locking, indirect secondary indexes.
  - MyISAM: No transactions, table-locking, direct indexes (faster reads but prone to corruption/fragmentation).