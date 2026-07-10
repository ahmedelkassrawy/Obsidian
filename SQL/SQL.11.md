# SQL Cursors, Identity, Inserts, Snapshots, and SQLCLR Study Notes

This document covers SQL cursors, identity columns, insert operations, database snapshots, and SQL Common Language Runtime (SQLCLR). It includes examples and explanations formatted for easy study in Obsidian, based on provided SQL scripts. All date-related examples reflect execution on May 19, 2025, at 11:09 PM EEST.

## Cursors

Cursors allow row-by-row processing of query results, acting like a for loop over a result set.

### Examples

#### Basic Cursor

```sql
DECLARE c1 CURSOR 
FOR SELECT st_id, st_fname 
    FROM Student
    WHERE St_Address = 'cairo'
FOR READ ONLY;

DECLARE @id INT, @name VARCHAR(20);
OPEN c1;
FETCH c1 INTO @id, @name;
WHILE @@FETCH_STATUS = 0
    BEGIN 
        SELECT @id, @name;
        FETCH c1 INTO @id, @name;
    END;
CLOSE c1;
DEALLOCATE c1;
```

- **Explanation**: Iterates over Cairo students, selecting `st_id` and `st_fname` for each row.
- **Steps**:
    - Declare cursor with query.
    - Open cursor to initialize.
    - Fetch rows into variables.
    - Loop until `@@FETCH_STATUS != 0`.
    - Close and deallocate to free resources.

#### Concatenating Names

```sql
DECLARE c1 CURSOR 
FOR SELECT st_fname
    FROM Student
    WHERE st_fname IS NOT NULL
FOR READ ONLY;

DECLARE @name VARCHAR(20), @allnames VARCHAR(300) = '';
OPEN c1;
FETCH c1 INTO @name;
WHILE @@FETCH_STATUS = 0
    BEGIN
        SET @allnames = CONCAT(@allnames, ',', @name);
        FETCH c1 INTO @name;
    END;
SELECT @allnames;
CLOSE c1;
DEALLOCATE c1;
```

- **Explanation**: Concatenates non-null `st_fname` values into a comma-separated string (e.g., `,Ahmed,Amr,Mona`).

#### Update Cursor

```sql
DECLARE c1 CURSOR 
FOR SELECT salary 
    FROM Instructor
FOR UPDATE;

DECLARE @sal INT;
OPEN c1;
FETCH c1 INTO @sal;
WHILE @@FETCH_STATUS = 0
    BEGIN
        IF @sal >= 3000
            UPDATE Instructor
            SET salary = @sal * 1.20
            WHERE CURRENT OF c1;
        ELSE
            UPDATE Instructor
            SET salary = @sal * 1.10
            WHERE CURRENT OF c1;
        FETCH c1 INTO @sal;
    END;
CLOSE c1;
DEALLOCATE c1;
```

- **Explanation**: Updates `salary` (20% increase if ≥ 3000, 10% otherwise) using `WHERE CURRENT OF c1` to target the current row.

> [!warning] Cursor Notes
> 
> - Cursors are slow for large datasets; prefer set-based operations when possible.
> - Use `FOR READ ONLY` for queries, `FOR UPDATE` for modifications.
> - Always `CLOSE` and `DEALLOCATE` to free resources.

> [!tip] Cursor Tips
> 
> - Use cursors for row-specific logic (e.g., conditional updates).
> - Minimize cursor scope to improve performance.

## Identity Columns

Identity columns auto-generate sequential values, typically used for primary keys.

### Example

```sql
CREATE TABLE dbo.T1 (
    column_1 INT,
    column_2 VARCHAR(30),
    column_3 INT IDENTITY PRIMARY KEY
);

INSERT INTO T1 VALUES (1, 'Row #1');
INSERT INTO T1 (column_2) VALUES ('Row #2');

DELETE FROM T1 WHERE column_3 BETWEEN 3 AND 8;

SET IDENTITY_INSERT T1 ON;
INSERT INTO T1 (column_1, column_2, column_3) VALUES (1, 'Row #1', 4);
SET IDENTITY_INSERT T1 OFF;

SELECT column_1, column_2, column_3 FROM T1;

DROP TABLE T1;
```

- **Explanation**:
    - `column_3 INT IDENTITY`: Auto-increments (e.g., 1, 2, 3, ...).
    - `DELETE`: Creates gaps in identity values (e.g., 2 to 9).
    - `SET IDENTITY_INSERT ON`: Allows explicit identity values (e.g., `4`).
    - Gaps persist after deletions; identity does not reset automatically.

> [!note] Identity Notes
> 
> - Use for unique, sequential IDs.
> - Gaps are normal after deletions or failed inserts.
> - `SET IDENTITY_INSERT ON` is session-specific and requires explicit column lists.

## Insert Operations

`INSERT` statements add data to tables, with multiple approaches.

### Examples

#### Simple Insert

```sql
INSERT INTO employee (id, name, age)
VALUES (1, 'John Doe', 30);
```

- **Explanation**: Inserts one row with specified values.

#### Multi-Row Insert

```sql
INSERT INTO employee (id, name, age)
VALUES 
    (2, 'Jane Doe', 25),
    (3, 'Jim Beam', 40),
    (4, 'Jack Daniels', 35);
```

- **Explanation**: Inserts multiple rows in one statement.

#### Insert Based on Select

```sql
INSERT INTO employee (id, name, age)
SELECT id, name, age
FROM temp_employee
WHERE age > 30;
```

- **Explanation**: Inserts rows from a `SELECT` query result.

#### Insert Based on Execute

```sql
DECLARE @sql NVARCHAR(MAX);
SET @sql = 'SELECT id, name, age FROM temp_employee WHERE age > 30';
INSERT INTO employee (id, name, age)
EXEC sp_executesql @sql;
```

- **Explanation**: Inserts rows from a dynamic SQL query.

#### Bulk Insert

```sql
BULK INSERT employee
FROM 'd:\data.txt'
WITH (FIELDTERMINATOR = ',');
```

- **Explanation**: Imports data from a file, using a comma as the field separator.

### Insert Types Summary

|Type|Description|Use Case|
|---|---|---|
|Simple Insert|Single row with explicit values|Manual data entry|
|Multi-Row Insert|Multiple rows in one statement|Batch data entry|
|Insert Based on Select|Inserts query results|Data migration|
|Insert Based on Execute|Inserts from dynamic SQL|Dynamic data sources|
|Bulk Insert|Imports from a file|Large data imports|

> [!success] Insert Best Practices
> 
> - Use multi-row inserts for efficiency.
> - Validate data before bulk inserts to avoid errors.
> - Use `sp_executesql` for safe dynamic inserts.

## Database Snapshots

Database snapshots provide a read-only, point-in-time view of a database.

### Key Features

- **Read-Only**: Cannot modify data.
- **No Log File**: Lightweight, no transaction logs.
- **Point-in-Time**: Captures database state at creation.
- **Uses**: Reporting, recovery, testing.

### Examples

#### Create Snapshot

```sql
CREATE DATABASE itisnap
ON
(
    NAME = 'ITI',
    FILENAME = 'd:\itisnap.ss'
)
AS SNAPSHOT OF iti;
```

- **Explanation**: Creates a snapshot `itisnap` of the `ITI` database, stored at `d:\itisnap.ss`.

#### Query Snapshot

```sql
SELECT * FROM itisnap.dbo.student;
```

- **Explanation**: Queries the snapshot, unaffected by changes to `ITI`.

#### Restore from Snapshot

```sql
RESTORE DATABASE ITI
FROM DATABASE_SNAPSHOT = 'itisnap';
```

- **Explanation**: Reverts `ITI` to the state captured in `itisnap`.

### How Snapshots Work

- Snapshots use pointers to the source database’s data.
- Changes to the source database do not affect the snapshot.
- Snapshots store only changed pages, making them space-efficient.

> [!tip] Snapshot Uses
> 
> - **Reporting**: Run queries on static data.
> - **Recovery**: Revert database to a prior state.
> - **Testing**: Test changes without affecting the live database.

> [!warning] Snapshot Limitations
> 
> - Requires Enterprise Edition of SQL Server.
> - Cannot modify snapshot data.
> - Source database must be online.

## SQL Common Language Runtime (SQLCLR)

SQLCLR integrates .NET code (e.g., C#) with SQL Server for advanced functionality.

### Example

```sql
sp_configure 'clr_enabled', 1;
GO
RECONFIGURE;
```

- **Explanation**: Enables SQLCLR on the server. Further implementation (e.g., functions, types) is done in Visual Studio using C#.

### SQLCLR Uses

- **Functions**: Create custom scalar or table-valued functions.
- **Data Types**: Define new types (e.g., structs, classes).
- **Complex Logic**: Implement logic not easily done in T-SQL.
- **Performance**: C# can outperform T-SQL for certain computations.

> [!note] SQLCLR Notes
> 
> - Requires enabling via `sp_configure`.
> - Development occurs in Visual Studio, deployed to SQL Server.
> - Use for tasks like string manipulation or mathematical computations.

> [!warning] SQLCLR Considerations
> 
> - Security risks if not properly managed (use `SAFE` permission sets).
> - Overhead for simple tasks; prefer T-SQL when possible.

## Key Takeaways

> [!summary] Study Tips
> 
> - **Cursors**: Use sparingly for row-by-row processing; prefer set-based queries.
> - **Identity**: Manage gaps and explicit inserts with `SET IDENTITY_INSERT`.
> - **Inserts**: Choose the right method (simple, multi-row, bulk) for the task.
> - **Snapshots**: Ideal for point-in-time views, reporting, and recovery.
> - **SQLCLR**: Extend SQL with C# for complex logic, but weigh performance and security.
> - Test cursors and inserts with small datasets to verify behavior.
> - Use snapshots for quick recovery in testing environments.

> [!question] Practice Questions
> 
> 1. Write a cursor to concatenate `ins_name` from `Instructor` into a single string.
> 2. How would you insert a row into `T1` with an explicit `column_3` value of 10?
> 3. Create a snapshot of a `Company` database and query its `employee` table.
> 4. Outline a SQLCLR function to calculate the factorial of a number.