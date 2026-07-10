# SQL TOP, NEWID, Execution Order, and DDL Study Notes

This document covers SQL `TOP`, `NEWID()`, query execution order, database objects, and Data Definition Language (DDL) operations. It includes examples and explanations formatted for easy study in Obsidian, based on provided SQL scripts.

## TOP Clause

The `TOP` clause limits the number of rows returned by a query. It can be used with or without `WITH TIES` to handle duplicates in the `ORDER BY` column.

### Examples of TOP

#### Basic TOP

```sql
SELECT TOP(3) st_fname
FROM Student;
```

- **Explanation**: Returns the first 3 student first names from the `Student` table, in the order they are stored (unless `ORDER BY` is specified).

#### TOP with Filter

```sql
SELECT TOP(3) st_fname
FROM Student
WHERE st_address = 'alex';
```

- **Explanation**: Returns the first 3 student first names where `st_address` is 'alex'.

#### TOP vs. Aggregate

```sql
SELECT MAX(salary) 
FROM Instructor;
```

- **Explanation**: Returns a single value (the highest salary). Compare to:

```sql
SELECT TOP(2) Salary
FROM Instructor
ORDER BY Salary DESC;
```

- **Explanation**: Returns the top 2 salaries in descending order (highest to lowest).

#### TOP with TIES

```sql
SELECT TOP(7) WITH TIES * 
FROM Student 
ORDER BY st_age DESC;
```

- **Explanation**: Returns the top 7 students by `st_age` (descending). If the 7th age has duplicates, all matching rows are included.
- **Key Point**: `WITH TIES` ensures rows with the same value in the `ORDER BY` column as the last row are included, potentially returning more than 7 rows.

> [!tip] TOP Notes
> 
> - Without `ORDER BY`, `TOP` returns rows in an arbitrary order.
> - `WITH TIES` requires `ORDER BY` and is useful for including duplicates.
> - Use `TOP` instead of aggregates like `MAX` when you need multiple rows.

## NEWID()

`NEWID()` generates a **Globally Unique Identifier (GUID)**, a 128-bit value guaranteed to be unique across systems.

### Examples of NEWID()

#### Basic NEWID()

```sql
SELECT NEWID();
```

- **Explanation**: Returns a random GUID, e.g., `6F9619FF-8B86-D011-B42D-00C04FC964FF`.

#### NEWID() in Table Creation

```sql
CREATE TABLE ExampleTable (
    ID UNIQUEIDENTIFIER DEFAULT NEWID(),
    Name NVARCHAR(50)
);

INSERT INTO ExampleTable (Name) VALUES ('John');
INSERT INTO ExampleTable (Name) VALUES ('Alice');
```

- **Resulting Table**:
    
    |ID|Name|
    |---|---|
    |6F9619FF-8B86-D011-B42D-00C04FC964FF|John|
    |A7B9C1D2-E3F4-4567-89AB-CDEF01234567|Alice|
    
- **Explanation**: The `ID` column uses `NEWID()` as a default, automatically generating unique GUIDs for each row.
    

#### NEWID() for Randomization

```sql
SELECT *, NEWID()
FROM Student;
```

- **Explanation**: Adds a new column with a unique GUID for each row.

```sql
SELECT TOP(3) * 
FROM Student
ORDER BY NEWID();
```

- **Explanation**: Returns 3 random rows from `Student` by ordering by a random GUID.

> [!success] NEWID() Uses
> 
> - **Primary Keys**: Use for unique identifiers across distributed systems.
> - **Randomization**: `ORDER BY NEWID()` shuffles rows for random sampling.
> - **Caution**: GUIDs are larger than `INT`, so they use more storage.

## Execution Order

SQL queries follow a specific logical execution order, which affects how aliases and conditions work.

### Execution Order

1. **FROM**
2. **JOIN**
3. **ON**
4. **WHERE**
5. **GROUP BY**
6. **HAVING** (with aggregates)
7. **SELECT** (including `DISTINCT` and aggregates)
8. **ORDER BY**
9. **TOP**

### Examples

#### Valid Query

```sql
SELECT st_fname + ' ' + st_lname AS fullname
FROM Student 
ORDER BY fullname;
```

- **Explanation**: Works because `ORDER BY` executes after `SELECT`, so the alias `fullname` is available.

#### Invalid Query

```sql
SELECT st_fname + ' ' + st_lname AS fullname
FROM Student 
WHERE fullname = 'ahmed ali';
```

- **Explanation**: Fails because `WHERE` executes before `SELECT`, so the alias `fullname` is not yet defined.
- **Workaround**: Use the expression directly:

```sql
SELECT st_fname + ' ' + st_lname AS fullname
FROM Student 
WHERE st_fname + ' ' + st_lname = 'ahmed ali';
```

> [!warning] Execution Order Pitfalls
> 
> - Avoid using `SELECT` aliases in `WHERE` or `GROUP BY`.
> - Use subqueries or CTEs to reference computed values in earlier clauses.

## Database Objects

Database objects include tables, views, functions, stored procedures (SP), and rules. Objects are referenced using a four-part naming convention: `[ServerName].[DBName].[SchemaName].[ObjectName]`.

### Examples

#### Accessing Objects

```sql
SELECT *
FROM [DESKTOP-QFMC1MC].ITI.dbo.Student;
```

- **Explanation**: Retrieves all columns from the `Student` table in the `ITI` database on the `DESKTOP-QFMC1MC` server.

#### Cross-Database Query

```sql
SELECT * 
FROM Company_SD.dbo.Project;
```

- **Explanation**: Accesses the `Project` table in the `Company_SD` database.

#### Cross-Database UNION

```sql
SELECT dname 
FROM Company_SD.dbo.Departments
UNION ALL
SELECT dept_name 
FROM Department;
```

- **Explanation**: Combines department names from two different databases (`Company_SD` and the current database).

> [!note] Object Naming
> 
> - Default schema is `dbo` if not specified.
> - Use fully qualified names for clarity in cross-server or cross-database queries.
> - Ensure permissions allow access to referenced objects.

## Data Definition Language (DDL)

DDL statements define or modify database structures, such as creating or copying tables.

### Examples

#### Copy Table with Data

```sql
SELECT * INTO table2
FROM Student;
```

- **Explanation**: Creates a new table `table2` with the same structure and data as `Student`.
- **Note**: Does not copy constraints, indexes, or triggers.

#### Copy Table Structure Only

```sql
SELECT * INTO tab4
FROM Student
WHERE 1 = 2;
```

- **Explanation**: Creates an empty table `tab4` with the same structure as `Student`. The `WHERE 1 = 2` condition ensures no rows are copied.

#### Insert with Values

```sql
INSERT INTO tab3
VALUES (66, 'ali');
```

- **Explanation**: Inserts a single row into `tab3`, assuming `tab3` has columns compatible with `(st_id, st_fname)`.

#### Insert Based on Select

```sql
INSERT INTO tab3
SELECT st_id, st_fname FROM Student;
```

- **Explanation**: Copies `st_id` and `st_fname` from `Student` into `tab3`.

> [!important] DDL Best Practices
> 
> - Use `SELECT INTO` for quick table creation, but manually add constraints if needed.
> - Verify column compatibility before `INSERT ... SELECT`.
> - Test DDL in a transaction to avoid unintended changes.

## Key Takeaways

> [!summary] Study Tips
> 
> - **TOP**: Use with `ORDER BY` for predictable results; `WITH TIES` handles duplicates.
> - **NEWID()**: Ideal for unique IDs or randomization, but consider storage overhead.
> - **Execution Order**: Understand the sequence to avoid alias errors.
> - **Objects**: Use fully qualified names for cross-database queries.
> - **DDL**: Leverage `SELECT INTO` for table creation and `INSERT ... SELECT` for bulk data transfer.

> [!question] Practice Questions
> 
> 1. How would you select the top 5 students by `st_age` with duplicates included?
> 2. Write a query using `NEWID()` to select a random student.
> 3. Why does `WHERE fullname = 'ahmed ali'` fail in the example above?
> 4. How would you copy the structure of `Instructor` into a new table without data?