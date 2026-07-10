## Choosing Optimal Data Types in MySQL
## General Rules for Selecting Data Types

1. **Smaller is Usually Better**
    
    - Use the smallest data type that can correctly represent your data to save disk space, memory, and CPU cycles.
    - Be cautious: choosing a type too small may require schema changes later, which can be cumbersome in high-volume databases.
    - Avoid oversized types unless necessary to accommodate future growth.
2. **Simple is Good**
    
    - Simpler data types (e.g., integers) require fewer CPU cycles than complex types (e.g., strings).
    - Example: Store IPv4 addresses as 32-bit unsigned integers using `INET_ATON()` and `INET_NTOA()` instead of strings for better efficiency, unless storing IPs is incidental.
3. **Avoid NULL if Possible**
    
    - Nullable columns complicate query optimization, indexes, and comparisons.
    - Some storage engines (e.g., InnoDB) use minimal space for NULL (1 bit), but others may use more (1 byte).
    - Specify `NOT NULL` when NULL isn’t needed, but don’t overhaul existing schemas solely for this.

## MySQL Data Type Categories

### Whole Numbers

- **Types**: `TINYINT`, `SMALLINT`, `MEDIUMINT`, `INT`, `BIGINT`
- **Storage**: 8, 16, 24, 32, 64 bits respectively.
- **Signed vs. Unsigned**:
    - Signed `TINYINT`: -128 to 127
    - Unsigned `TINYINT`: 0 to 255
    - Use `UNSIGNED` to double the positive range if negative values aren’t needed.
- **Notes**:
    - MySQL uses `BIGINT` for internal computations (e.g., `SUM`) to avoid overflows, and `DECIMAL` or `DOUBLE` for others (e.g., `AVG`).
    - Display width (e.g., `INT(11)`) only affects display in tools, not storage or range.

### Real Numbers

- **Types**:
    - `FLOAT` (4 bytes, approximate math)
    - `DOUBLE` (8 bytes, higher precision, approximate math)
    - `DECIMAL` (exact math, configurable precision)
- **Precision**:
    - Example: `DECIMAL(18,9)` stores 18 digits, 9 after the decimal.
    - Choose precision based on application needs to optimize storage.
- **Use Case**:
    - Use `DECIMAL` for exact calculations (e.g., financial data).
    - Use `FLOAT` or `DOUBLE` for approximate calculations with less storage.

### String Types

- **CHAR**:
    - Fixed-length strings, space-efficient for short, uniform data (e.g., MD5 hashes).
    - Strips trailing spaces, no length storage overhead.
- **VARCHAR**:
    - Variable-length strings, uses 1-2 bytes for length (1 if max length ≤ 255, 2 otherwise).
    - Suitable when max length exceeds average length, but updates may cause fragmentation.
- **BLOB and TEXT**:
    - For large data (e.g., `TINYTEXT`, `MEDIUMTEXT`, `LONGBLOB`).
    - Stored externally, using 1-4 bytes per row for location.
    - Sorting uses `max_sort_length` bytes, and they can’t be indexed.
    - Avoid unless necessary due to disk-based temporary tables and sorting.
- **ENUM**:
    - Stores predefined values as integers (1-2 bytes based on cardinality).
    - Efficient for finite sets (e.g., 50 US states), but sorting uses definition order, not lexicographical.
    - Conversion overhead (lookup table) can impact performance in joins.

### Date and Time

- **DATETIME**:
    - Stores dates from 1001 to 9999 in `YYYYMMDDHHMMSS` format (8 bytes).
    - Straightforward, no special features.
- **TIMESTAMP**:
    - Stores seconds since 1970-01-01 (UNIX epoch), up to 2038 (4 bytes).
    - Supports timezone information per connection.
    - Use `DATETIME` for standard formats, handle timezone logic in the application.

### Bit-Packed

- **BIT**: Stores boolean or bitwise data, space-efficient.
- **SET**: Stores multiple values from a predefined set.
- **Use Case**: Efficient for permissions (e.g., MySQL’s ACL).

## Choosing Identifiers

- **Consistency**: Use the same data type (including `UNSIGNED`) for identifiers across related tables to avoid performance issues in joins.
- **Simplicity**: Prefer integers for identifiers due to `AUTO_INCREMENT` support and faster comparisons.
- **Size**: Use the smallest type (e.g., `TINYINT` for 50 states), but account for future growth.
- **Avoid**:
    - `ENUM`/`SET` due to conversion overhead.
    - Strings (e.g., UUIDs) due to space, slower comparisons, and index fragmentation.
    - For UUIDs, use `BINARY(16)` with `UNHEX()` to store as 16-byte numbers.

## Schema Design Gotchas in MySQL

- **Too Many Columns**:
    - Wide tables (hundreds of columns) increase CPU usage due to row buffer conversions, especially with InnoDB.
    - Impacts normalization vs. denormalization decisions.
- **Too Many Joins**:
    - Entity-Attribute-Value (EAV) designs lead to excessive joins, limited to 61 tables in MySQL.
    - Keep joins minimal for performance.
- **Overusing ENUM**:
    - Adding values requires `ALTER TABLE`, which is slow for large tables.
- **Overusing NULL**:
    - Impacts query optimization; use default values (e.g., 0) when possible, but avoid “magic” values.

## Normalization vs. Denormalization

### Normalized Schema

- **Pros**:
    - Faster updates (single data source).
    - Space-efficient, fewer duplicates.
    - Smaller tables fit better in memory.
    - No need for `DISTINCT` or `GROUP BY`.
    - Deleting records doesn’t lose related entities.
- **Cons**:
    - Joins required for non-trivial queries, increasing retrieval cost.

### Denormalized Schema

- **Pros**:
    - Faster retrieval (no joins).
    - Efficient indexing (e.g., compound indexes on combined columns).
- **Cons**:
    - Slower updates (multiple records to change).
    - More storage due to duplicates.

### Example: Forum App

- **Normalized Query**:
    
    ```sql
    SELECT message_text, user_name
    FROM message
    INNER JOIN user ON message.user_id=user.id
    WHERE user.account_type='premium'
    ORDER BY message.published DESC LIMIT 10;
    ```
    
    - Inefficient due to index scans or file sorts.
- **Denormalized Query**:
    
    ```sql
    SELECT message_text, user_name
    FROM user_messages
    WHERE account_type='premium'
    ORDER BY published DESC
    LIMIT 10;
    ```
    
    - Uses compound index `(account_type, published)` for efficiency.

### Best of Both Worlds

- **Partial Denormalization**: Duplicate specific columns (e.g., `account_type`) using triggers to sync changes.
- **Cache Tables**: Store denormalized data for retrieval, sync periodically.
- **Summary Tables**: Store aggregated data (e.g., message counts) for frequent `GROUP BY` queries.
- **Tolerate Staleness**: Useful for cache/summary tables if delays are acceptable.

## Schema Evolution

- **ALTER TABLE**:
    - Can be slow or infeasible for large tables, requiring double storage.
    - Implemented by creating a new table, copying data, and swapping.
- **Mitigation**:
    - Use shadow copies (build new table, swap, drop old).
    - Perform on non-production servers.
    - Use third-party tools for easier management.

## Conclusion

Choosing optimal data types and schema designs in MySQL requires balancing storage, performance, and future scalability. Follow the principles of simplicity, minimal size, and avoiding NULL, while carefully considering normalization and denormalization trade-offs. Plan for schema evolution to minimize costly `ALTER TABLE` operations.

## References

- MySQL 8 Documentation
- Official MySQL ALTER TABLE Documentation