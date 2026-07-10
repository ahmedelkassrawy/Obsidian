# SQLite Database

## Overview
- **Pronunciation**: Referred to as "Skylight" (likely "SQLite").
- **Type**: Embedded database/storage engine for local data storage.
- **Popularity**: Extremely popular and widely used; embedded in browsers, software, operating systems (e.g., by default in Windows; possibly Linux – speaker uncertain).
- **Key Use Case**: Local, single-user database; ideal for applications needing a lightweight, file-based DB without a server.

## History and Creation
- **Creator**: D. Richard Hipp (transcript mentions "Dwayne Richard Hipp" with a humorous reference to "Dwayne Johnson" aka "The Rock").
- **Year**: Created in 2000.
- **Motivation**: To provide a simple local database alternative to direct file I/O (e.g., avoiding `file.write()` for structured data).
- **Evolution**:
  - Became a "beast" of an embedded database.
  - Uses B-Tree by default for storage.
  - Attempted LSM Tree Implementation: Richard tried adding LSM as an extension (due to LSM's rising popularity), but saw limited performance gains because of SQLite's intertwined architecture.
    - LSM can still be used as an extension if desired.
  - Reference: Article on this (speaker plans to link below in video).

## Architecture and Design
- **Embedded Nature**: Not a client-server DBMS; it's a local file-based database.
  - No TCP ports or multi-user server setup.
  - Better for single-user scenarios; for multi-user, use full DBMS like MySQL or PostgreSQL.
- **Comparison to MySQL**: MySQL separates database and storage engine (swappable), which is smarter for flexibility. SQLite's engine is more integrated, making changes like switching to LSM less effective.
- **PostgreSQL-Like**: Syntax and features resemble PostgreSQL.
- **Concurrency**:
  - Supports concurrent reads.
  - Supports concurrent writes (using operating system features – "badass" per speaker).
- **Locking**: Table-level locking only (no row-level locking).
  - Makes sense for local use: No need for row-level in single-user environments.

## Features
- **ACID Compliance**: Full ACID support (Atomicity, Consistency, Isolation, Durability).
  - Allows transactions even in local setups.
- **Transactions**: Supported; attractive for reliable local operations.
- **WebSQL**: Browser console feature based on SQLite (potential future video topic).

## When to Use SQLite
- **Pros**:
  - Lightweight and embedded.
  - Everywhere: Browsers, OS, apps.
  - ACID transactions locally.
  - Concurrent read/write support.
- **Cons**:
  - Table-level locking (not ideal for high-concurrency, but fine locally).
  - Not for multi-user/client-server needs.
  - Performance tweaks (e.g., LSM) may not yield big gains due to architecture.
- **Use Cases**: Local data storage in apps, browsers; not for networked, multi-user databases.
