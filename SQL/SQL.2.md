# SQL Subqueries, DML, and Functions Study Notes

This document covers SQL subqueries, UNION family operators, Data Manipulation Language (DML) statements, built-in functions, and adhoc queries. It includes examples and explanations formatted for easy study in Obsidian, based on provided SQL scripts.

## Subqueries

Subqueries are nested queries within a main query, used to return data that the outer query processes. They can appear in `SELECT`, `WHERE`, `FROM`, or DML statements.

### Examples of Subqueries

#### Filter Students by Age

```sql
SELECT *
FROM Student
WHERE St_Age < (SELECT AVG(St_Age) FROM Student);
```

- **Explanation**: Returns all columns from `Student` where the student's age is less than the average age of all students.
- **Subquery**: `(SELECT AVG(St_Age) FROM Student)` computes the average age.

#### Departments with Students

```sql
SELECT dept_name 
FROM Department
WHERE dept_id IN (SELECT DISTINCT(dept_id)
                  FROM Student 
                  WHERE dept_id IS NOT NULL);
```

- **Explanation**: Retrieves department names where there are students enrolled (non-null `dept_id`).
- **Subquery**: `(SELECT DISTINCT(dept_id) FROM Student WHERE dept_id IS NOT NULL)` gets unique department IDs from `Student`.
- **Alternative (faster)**: Using an `INNER JOIN`:

```sql
SELECT DISTINCT dept_name
FROM Student s INNER JOIN Department D
ON D.dept_id = s.dept_id;
```

- **Why faster?**: Joins are often optimized better by SQL Server than subqueries with `IN`.

#### Subquery with DML

```sql
DELETE FROM stud_course 
WHERE st_id IN (SELECT st_id FROM Student WHERE St_Address = 'cairo');
```

- **Explanation**: Deletes records from `stud_course` for students living in Cairo.
- **Subquery**: `(SELECT st_id FROM Student WHERE St_Address = 'cairo')` identifies student IDs to delete.

> [!tip] Subquery Tips
> 
> - Use subqueries for dynamic filtering (e.g., comparing against aggregates like `AVG`).
> - Replace `IN` subqueries with `JOIN` for better performance when possible.
> - Ensure subqueries return the expected number of rows (e.g., single value for comparisons like `<`).

## UNION Family Operators

The UNION family (`UNION ALL`, `UNION`, `INTERSECT`, `EXCEPT`) combines results from multiple `SELECT` statements. Columns must have compatible data types and the same number of columns.

### Definitions

|Operator|Description|
|---|---|
|**UNION ALL**|Combines all rows from both queries, including duplicates.|
|**UNION**|Combines all rows, removing duplicates.|
|**INTERSECT**|Returns only rows common to both queries.|
|**EXCEPT**|Returns rows in the first query but not in the second.|

### Examples

#### UNION ALL

```sql
SELECT st_fname AS Names
FROM Student
UNION ALL
SELECT ins_name 
FROM Instructor;
```

- **Explanation**: Combines student first names and instructor names into a single column `Names`, keeping duplicates.
- **Note**: `AS Names` aliases the output column for clarity.

```sql
SELECT st_fname, st_id 
FROM Student
UNION ALL
SELECT ins_name, ins_id 
FROM Instructor;
```

- **Explanation**: Combines student names/IDs with instructor names/IDs, keeping duplicates. Each query returns two columns.

#### INTERSECT

```sql
SELECT st_fname
FROM Student
INTERSECT 
SELECT ins_name 
FROM Instructor;
```

- **Explanation**: Returns names that appear in both `Student.st_fname` and `Instructor.ins_name`.
- **Use case**: Find names shared between students and instructors.

> [!warning] UNION Family Notes
> 
> - `UNION ALL` is faster than `UNION` because it doesn’t remove duplicates.
> - Ensure column data types match (e.g., `st_fname` and `ins_name` must be compatible).
> - `INTERSECT` and `EXCEPT` are less common but useful for specific set operations.

## Data Manipulation Language (DML)

DML statements modify data in tables: `INSERT`, `UPDATE`, `DELETE`.

### Examples

#### DELETE

```sql
DELETE FROM Department 
WHERE dept_id = 20;
```

- **Explanation**: Removes the department with `dept_id = 20`.
- **Caution**: Ensure no foreign key constraints prevent deletion.

#### UPDATE

```sql
UPDATE Department 
SET dept_id = 4000 
WHERE dept_id = 20;
```

- **Explanation**: Changes `dept_id` from 20 to 4000 for the matching department.
- **Note**: If `dept_id` is referenced by a foreign key with `ON UPDATE CASCADE`, related tables update automatically.

> [!important] DML Best Practices
> 
> - Always use `WHERE` to avoid affecting unintended rows.
> - Check foreign key constraints before `DELETE` or `UPDATE`.
> - Test DML in a transaction (`BEGIN TRAN`, `ROLLBACK`) to verify effects.

## Built-in Functions

SQL Server provides functions for data manipulation, aggregation, and system information.

### Common Functions

|Function|Description|
|---|---|
|`GETDATE()`|Returns the current date and time.|
|`ISNULL(x, y)`|Returns `y` if `x` is `NULL`, else `x`.|
|`COALESCE(x, y, ...)`|Returns the first non-`NULL` value.|
|`CONCAT(str1, str2, ...)`|Concatenates strings.|
|`CONVERT(type, expr)`|Converts `expr` to the specified data type.|
|`YEAR(date)`|Extracts the year from a date.|
|`MONTH(date)`|Extracts the month from a date.|

> [!note] Function Usage
> 
> - Use `ISNULL` for simple null replacement, `COALESCE` for multiple options.
> - `CONVERT` is useful for formatting (e.g., `CONVERT(VARCHAR, GETDATE(), 103)` for `dd/mm/yyyy`).

## Adhoc Queries

Adhoc queries retrieve system or string-based information using built-in functions or system variables.

### Examples

```sql
SELECT SUBSTRING(st_fname, 1, 3) FROM Student; -- e.g., 'ahm' for 'Ahmed'
```

- **Explanation**: Extracts the first three characters of `st_fname`.

```sql
SELECT DB_NAME(); -- Returns the current database name
SELECT SUSER_NAME(); -- Returns the current server user
SELECT @@VERSION; -- Returns the SQL Server version
```

- **Explanation**:
    - `DB_NAME()`: Useful for scripts that need the current database context.
    - `SUSER_NAME()`: Identifies the logged-in user for auditing.
    - `@@VERSION`: Provides version details for compatibility checks.

> [!success] Adhoc Query Uses
> 
> - Debugging: Verify database or user context.
> - Reporting: Extract substrings or system info for logs.
> - Scripting: Use in dynamic SQL for environment-specific logic.

## Key Takeaways

> [!summary] Study Tips
> 
> - **Subqueries**: Use for dynamic filtering; consider `JOIN` for performance.
> - **UNION Family**: Choose `UNION ALL` for speed unless duplicates must be removed.
> - **DML**: Always specify `WHERE` and check constraints.
> - **Functions**: Leverage `ISNULL`, `COALESCE`, and date functions for robust queries.
> - **Adhoc Queries**: Use for system info or string manipulation.

> [!question] Practice Questions
> 
> 1. How would you rewrite the department subquery using `EXISTS` instead of `IN`?
> 2. What’s the difference between `UNION ALL` and `UNION` in terms of performance and output?
> 3. How would you use `COALESCE` to handle nulls in a `SELECT` query?
> 4. Write an adhoc query to extract the first two characters of `dept_name`.