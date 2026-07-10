Every DB contains mainly two things Frontend and Storage Engine
Frontend
- API
- Data Format

Storage Engine
- Storage
- Indexes 
- Data files
- Transactions
- WAL

# MongoDB Architecture and SQL vs. NoSQL

## Overview

This guide covers the internal architecture of MongoDB, its evolution from the MMAPv1 storage engine to WiredTiger and clustered collections (introduced in version 5.3), and the key differences between SQL and NoSQL databases. It’s based on a transcript discussing database internals, focusing on storage engines, data formats, and APIs.

> [!info] Key Takeaways
> 
> - **SQL vs. NoSQL**: SQL uses structured tables and rows with SQL queries; NoSQL uses flexible data formats (e.g., documents in MongoDB) with custom APIs.
> - **MongoDB Evolution**: Moved from MMAPv1 (offset-based, global locks) to WiredTiger (document-level locking, compression) to clustered collections (efficient ID-based lookups).
> - **Storage Engine**: Manages data persistence, indexing, transactions, and locking, independent of the database’s front-end API.

## SQL vs. NoSQL: The Core Difference

- **Two Main Components of a Database**:
    - **Front-End (API)**: How applications interact with the database (e.g., SQL queries for relational databases, `get/set` for MongoDB).
    - **Storage Engine**: How data is stored on disk, indexed, and managed (e.g., pages, bytes, transactions).
- **SQL Databases**:
    - **Data Format**: Tables with rows and columns, rigid schema.
    - **API**: Structured Query Language (SQL) for querying (e.g., `SELECT * FROM table`).
    - **Example**: MySQL, PostgreSQL.
    - **Design**: Built in the 1960s–70s for structured data, assuming tables are universal.
- **NoSQL Databases**:
    - **Data Format**: Flexible, schemaless (e.g., JSON documents in MongoDB, graphs, key-value).
    - **API**: Custom APIs (e.g., MongoDB’s `find()`, `insert()`), no SQL.
    - **Motivation**: Emerged in the 2000s for web applications needing flexible, schema-free data (e.g., JSON for web APIs).
    - **Examples**: MongoDB (documents), Redis (key-value), Neo4j (graphs).
- **Key Distinction**:
    - SQL: Fixed schema, table-based, SQL-based queries.
    - NoSQL: Schemaless, diverse data formats (documents, graphs), custom APIs.
    - Storage engine is agnostic to data format; it stores bytes in pages (e.g., 8KB in PostgreSQL, 16KB in MySQL).

> [!note] Why NoSQL?  
> NoSQL databases like MongoDB reduce friction for developers by allowing flexible, schema-free storage, aligning with modern web apps using JSON.

## MongoDB Architecture Evolution

MongoDB’s internal architecture has evolved significantly, particularly in its storage engine, which handles data persistence, indexing, and concurrency.

### 1. MMAPv1 Storage Engine (Pre-4.2)

- **Overview**: MongoDB’s original storage engine, deprecated due to inefficiencies.
- **Data Storage**:
    - Stored documents in data files as a sequence of JSON objects (bytes).
    - Used **offset-based addressing**: Each document had a unique `_id` mapped to a 64-bit pointer (32 bits for file name, 32 bits for offset within the file).
    - Document size stored to know how many bytes to read.
- **Indexing**:
    - Used B-tree indexes to map `_id` to disk locations.
    - Single I/O to fetch a document (Big O(log n) for index traversal, O(1) for disk read).
- **Challenges**:
    - **Offset Issues**: Updating a document’s size (e.g., adding a field) shifted offsets, requiring updates to all subsequent offsets, causing inefficiencies.
    - **Locking**: Initially used a **global lock** per database, serializing all writes (even across collections). Later improved to **collection-level locking** (still coarse-grained).
    - **Scalability**: Large indexes couldn’t fit in memory, leading to disk swaps and slower performance.
- **Use Case**: Fast for read-only workloads, problematic for writes due to offset and locking issues.

> [!example] MMAPv1 Lookup
> 
> ```python
> # Find document by _id
> # B-tree index: _id -> (file_name, offset)
> # OS reads file at offset for document_size bytes
> document = db.collection.find({"_id": "123"})
> ```

### 2. WiredTiger Storage Engine (Post-2014, Version 3.2+)

- **Overview**: MongoDB acquired WiredTiger in 2014, replacing MMAPv1 for better performance and features.
- **Key Features**:
    - **Document-Level Locking**: Allows concurrent updates to different documents in the same collection (unlike MMAPv1’s collection-level locks).
    - **Compression**: Compresses JSON documents to fit more data per page, reducing I/O (e.g., 1 I/O fetches 20 compressed documents vs. 3 uncompressed).
    - **Clustered B+ Tree**: Stores data in a B+ tree where leaf pages contain full documents, not just pointers.
- **Data Storage**:
    - Uses a **hidden record ID** (internal 64-bit identifier) instead of disk offsets.
    - Documents are stored in a clustered B+ tree, where the leaf pages hold the actual data.
    - **Primary Index**: Maps user-facing `_id` to record ID.
    - **Secondary Indexes**: Point to record ID, requiring two lookups for `_id` queries (Big O(log n) + Big O(log n)).
- **Advantages**:
    - Compression reduces I/O, improving performance.
    - Document-level locking supports concurrent writes.
    - B+ tree links leaf pages, enabling efficient range queries.
- **Drawbacks**:
    - **Double Lookup**: `_id` queries require two B+ tree traversals (`_id` → record ID → document), doubling I/O compared to MMAPv1’s single lookup.
    - **Index Overhead**: Primary and secondary indexes both point to record ID, increasing memory and I/O usage.

> [!example] WiredTiger Lookup
> 
> ```python
> # Find document by _id
> # Step 1: B+ tree (_id -> record_id)
> # Step 2: B+ tree (record_id -> document in clustered index)
> document = db.collection.find({"_id": "123"})
> ```

### 3. Clustered Collections (Version 5.3, July 2022)

- **Overview**: A new feature allowing collections to use the `_id` field as the clustered index, eliminating the hidden record ID.
- **Key Features**:
    - **Clustered Index**: The `_id` field directly indexes the B+ tree, where leaf pages store full documents.
    - **Single Lookup**: Queries by `_id` require one B+ tree traversal (Big O(log n)), improving performance.
    - **Optional**: Collections can opt into clustering; non-clustered collections retain the record ID approach.
- **Advantages**:
    - Faster `_id` queries (single lookup vs. double in WiredTiger).
    - Efficient range queries, as documents are ordered by `_id` in the B+ tree.
    - Similar to MySQL’s clustered index model, where the primary key organizes the data.
- **Challenges**:
    - **Secondary Indexes**: Point to `_id` instead of a smaller record ID (8 bytes). If `_id` is large (e.g., MongoDB’s default 12-byte ObjectID or user-defined UUIDs), secondary indexes grow, increasing memory and I/O.
    - **Trade-Off**: Larger `_id` values in secondary indexes can bloat storage, similar to MySQL’s issues with large primary keys.

> [!example] Clustered Collection Lookup
> 
> ```python
> # Create clustered collection
> db.create_collection("my_collection", clusteredIndex={"key": "_id", "unique": true})
> # Single B+ tree lookup for _id
> document = db.my_collection.find({"_id": "123"})
> ```

### Storage Engine Internals

- **Pages and I/O**:
    - Data is stored in fixed-size pages (e.g., 8KB in PostgreSQL, 16KB in MySQL, configurable in MongoDB).
    - Disk writes occur in whole pages, not bytes, for efficiency (no byte-level addressability on disk, unlike RAM).
    - **Dirty Pages**: Changes are written to RAM (marked dirty), then flushed to disk in batches to minimize I/O.
- **Write-Ahead Log (WAL)/Journaling**:
    - Logs changes to disk before applying to data files to ensure durability.
    - Example: Update salary from 10,000 to 10,050 → logged as a small journal entry.
    - On crash, WAL is replayed from the last checkpoint to restore data.
- **Indexes**:
    - **B-Tree/B+ Tree**: Used for fast lookups (Big O(log n)). Leaf pages in B+ trees are linked for efficient range queries.
    - **Clustered Index**: Data is stored in the index’s leaf pages (WiredTiger, clustered collections).
    - **Secondary Indexes**: Point to the primary key or record ID, adding overhead if the key is large.
- **Transactions**:
    - Ensure atomicity, consistency, isolation, and durability (ACID).
    - Handled by the storage engine, which manages locks and WAL.
- **Locking**:
    - **MMAPv1**: Global lock (initially), then collection-level lock (coarse-grained).
    - **WiredTiger**: Document-level locking, allowing concurrent updates to different documents.
    - **Advanced**: Some databases (e.g., YugabyteDB) offer column-level locking, but MongoDB uses document-level.

> [!tip] Why Clustered Collections?  
> Clustered collections optimize `_id` lookups, making MongoDB’s performance comparable to MySQL for primary key queries, but large `_id` values can bloat secondary indexes.

## MongoDB `_id` Field

- **Default**: 12-byte ObjectID (4 bytes timestamp, 5 bytes random, 3 bytes counter) for uniqueness across machines.
- **Customizable**: Users can set any value for `_id`, but large values (e.g., UUIDs) increase secondary index size.
- **Impact on Clustered Collections**: Since `_id` is the clustered index, large values increase storage and I/O for secondary indexes.

