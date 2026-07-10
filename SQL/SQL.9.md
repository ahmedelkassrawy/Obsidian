# SQL Indexes, Tables, Merge, and Views Study Notes

This document covers SQL indexes, tables (local, global, and table variables), `MERGE` statements, and views (including indexed views and DML operations). It includes examples and explanations formatted for easy study in Obsidian, based on provided SQL scripts. All examples assume execution on May 19, 2025, at 11:06 PM EEST.

## Indexes

Indexes improve query performance by allowing faster data retrieval.

### Types of Indexes

- **Clustered Index**: Defines the physical order of data in a table (one per table).
- **Nonclustered Index**: Separate structure with pointers to data (multiple allowed).

### Examples

#### Clustered Index

```sql
CREATE CLUSTERED INDEX myindex ON Student(st_fname);
```

- **Explanation**: Creates a clustered index on `st_fname`, physically sorting the `Student` table by first name.
- **Note**: Only one clustered index per table, as it dictates physical storage.

#### Nonclustered Index

```sql
CREATE NONCLUSTERED INDEX myindex ON Student(st_fname);
```

- **Explanation**: Creates a nonclustered index on `st_fname`, storing pointers to rows.

#### Indexes with Constraints

```sql
CREATE TABLE test22
(
    id INT PRIMARY KEY,
    name VARCHAR(20),
    age INT UNIQUE
);
```

- **Explanation**:
    - `PRIMARY KEY`: Automatically creates a clustered index on `id`.
    - `UNIQUE`: Creates a nonclustered index on `age`.

### Tools for Index Optimization

- **SQL Server Profiler**: Monitors query performance to identify frequently searched columns.
- **SQL Server Tuning Advisor**: Recommends indexes based on workload analysis.

> [!tip] Index Best Practices
> 
> - Use clustered indexes on frequently queried or sorted columns (e.g., primary keys).
> - Use nonclustered indexes for columns in `WHERE`, `JOIN`, or `ORDER BY`.
> - Avoid over-indexing to minimize storage and maintenance overhead.

> [!warning] Index Considerations
> 
> - Indexes slow down `INSERT`, `UPDATE`, and `DELETE` due to index maintenance.
> - Drop redundant indexes to optimize performance.

## Tables

SQL supports different table types: local temporary, global temporary, and table variables.

### Examples

#### Local Temporary Table

```sql
CREATE TABLE #exam 
(
    eid INT,
    edate DATE,
    numofQ INT
);
```

- **Explanation**: Creates a local temporary table `#exam`, accessible only in the current session. Dropped when the session ends.

#### Global Temporary Table

```sql
CREATE TABLE ##exam 
(
    eid INT,
    edate DATE,
    numofQ INT
);
```

- **Explanation**: Creates a global temporary table `##exam`, accessible across sessions. Dropped when the last session referencing it ends.

#### Table Variable

```sql
DECLARE @t TABLE (x INT);
INSERT INTO @t VALUES (1);
SELECT * FROM @t;
```

- **Explanation**: Declares a table variable `@t` with one column (`x`), inserts a value, and selects it. Stored in memory, scoped to the batch.

### Table Types Summary

|Type|Scope|Lifetime|Storage|
|---|---|---|---|
|Local Temp (#table)|Current session|Until session ends|TempDB|
|Global Temp (##table)|All sessions|Until last session ends|TempDB|
|Table Variable (@t)|Current batch|Until batch ends|Memory|

> [!note] Table Usage
> 
> - Use table variables for small datasets due to memory storage.
> - Use temporary tables for larger datasets or cross-batch operations.
> - Global temp tables are rare, used for multi-session data sharing.

## Merge Statements

The `MERGE` statement performs `INSERT`, `UPDATE`, or `DELETE` operations based on matching conditions between a source and target table.

### Examples

#### Basic Merge

```sql
MERGE INTO LastTransaction AS T
USING DailyTransaction AS S
ON T.id = S.did
WHEN MATCHED THEN
    UPDATE SET T.myvalue = S.dval
WHEN NOT MATCHED THEN 
    INSERT VALUES (S.did, S.dname, S.dval);
```

- **Explanation**:
    - **Target**: `LastTransaction` (T).
    - **Source**: `DailyTransaction` (S).
    - **Condition**: Matches on `T.id = S.did`.
    - **Actions**: Updates `T.myvalue` if matched; inserts new rows if not matched.

#### Advanced Merge

```sql
MERGE INTO LastTransaction AS T
USING DailyTransaction AS S
ON T.id = S.did
WHEN MATCHED AND S.dval > T.myvalue THEN
    UPDATE SET T.myvalue = S.dval
WHEN NOT MATCHED BY TARGET THEN  
    INSERT VALUES (S.did, S.dname, S.dval)
WHEN NOT MATCHED BY SOURCE THEN DELETE;
```

- **Explanation**:
    - **MATCHED**: Updates `T.myvalue` only if `S.dval > T.myvalue`.
    - **NOT MATCHED BY TARGET**: Inserts new rows from `S`.
    - **NOT MATCHED BY SOURCE**: Deletes rows in `T` not present in `S`.
- **Use Case**: Synchronize tables, e.g., updating transaction logs.

> [!success] Merge Benefits
> 
> - Combines multiple DML operations in one statement.
> - Ideal for ETL processes or data synchronization.
> - Reduces code complexity compared to separate `INSERT`, `UPDATE`, `DELETE`.

## Views

Views are virtual tables based on a query, simplifying data access or enforcing security.

### Examples

#### Basic View

```sql
CREATE VIEW Vstuds 
AS
    SELECT * 
    FROM Student;
```

- **Explanation**: Creates a view `Vstuds` showing all `Student` columns.

#### View with UNION

```sql
CREATE VIEW vall 
AS 
    SELECT * FROM vcairo 
    UNION ALL
    SELECT * FROM valex;
```

- **Explanation**: Combines rows from `vcairo` and `valex` views.

#### Schema Transfer

```sql
ALTER SCHEMA hr TRANSFER vall;
```

- **Explanation**: Moves the `vall` view to the `hr` schema.

#### View with DML

```sql
ALTER VIEW Vcairo(sid, sname, sadd)
AS 
    SELECT st_id, st_fname, st_address
    FROM Student
    WHERE st_address = 'cairo';

INSERT INTO Vcairo
VALUES (321, 'ali', 'cairo');
```

- **Explanation**: Defines a view for Cairo students; inserts a row into the underlying `Student` table.

#### View with CHECK OPTION

```sql
ALTER VIEW Vcairo(sid, sname, sadd)
AS
    SELECT st_id, st_fname, st_address
    FROM Student
    WHERE St_Address = 'cairo'
    WITH CHECK OPTION;
```

- **Explanation**: Ensures DML operations on `Vcairo` maintain `st_address = 'cairo'`. Inserts with other addresses fail.

#### Indexed View

```sql
CREATE VIEW vdata
WITH SCHEMABINDING
AS 
    SELECT ins_name, salary
    FROM dbo.Instructor
    WHERE dept_id = 10;
```

- **Explanation**: Creates an indexed view that materializes data for `dept_id = 10`. Requires `SCHEMABINDING` to prevent schema changes.

#### Schema Name Usage

Schema names (e.g., `dbo`) are required for:

- Scalar functions (e.g., `dbo.getsname`).
- Indexed views (e.g., `dbo.vdata`).
- Cross-server or cross-database table references.

### View DML Limitations

- **INSERT/UPDATE**: Allowed if affecting one table and columns are updatable.
- **DELETE**: Not allowed for multi-table views.
- **CHECK OPTION**: Enforces view’s `WHERE` clause in DML.

> [!tip] View Best Practices
> 
> - Use views to simplify queries or restrict data access.
> - Use `CHECK OPTION` to enforce data integrity in DML.
> - Indexed views improve performance but restrict schema changes.

> [!warning] View Notes
> 
> - DML on views updates the underlying table, not the view’s data.
> - Indexed views require `SCHEMABINDING` and limit table modifications.

## Key Takeaways

> [!summary] Study Tips
> 
> - **Indexes**: Use clustered for primary keys, nonclustered for frequent filters.
> - **Tables**: Choose table variables for small, temporary data; temp tables for larger sets.
> - **Merge**: Streamline ETL with conditional `INSERT`, `UPDATE`, `DELETE`.
> - **Views**: Simplify queries; use `CHECK OPTION` for DML integrity, indexed views for performance.
> - Use Profiler/Tuning Advisor to optimize index strategies.
> - Test DML on views to ensure correct table updates.

> [!question] Practice Questions
> 
> 1. How would you create a nonclustered index on `Student(st_address, st_age)`?
> 2. Write a `MERGE` statement to sync student grades between two tables.
> 3. Create a view for instructors with salaries above 3000, with `CHECK OPTION`.
> 4. How would you use a table variable to store top 5 students by age?