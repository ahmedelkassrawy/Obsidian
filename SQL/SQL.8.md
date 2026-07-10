# SQL Variables, Functions, and Windowing Study Notes

This document covers SQL variables (local and global), control of flow statements, batches, transactions, scripts, functions (scalar, inline table, multi-statement), windowing functions, exercises, and dynamic SQL. It includes examples and explanations formatted for easy study in Obsidian, based on provided SQL scripts. All date-related examples reflect execution on May 19, 2025, at 11:04 PM EEST.

## Declaring and Using Variables

Variables store temporary values for use in queries.

### Examples

#### Basic Variable

```sql
DECLARE @x INT = 100;
SELECT @x;
```

- **Explanation**: Declares an integer variable `@x` with value 100 and displays it.

#### Variable with Subquery

```sql
DECLARE @x INT = (SELECT AVG(St_Age) FROM Student);
SELECT @x;
```

- **Explanation**: Sets `@x` to the average `St_Age` from `Student`.

#### Assigning from SELECT

```sql
DECLARE @y INT;
SELECT @y = st_age FROM Student WHERE st_id = 6;
SELECT @y;
```

- **Explanation**: Assigns `st_age` for `st_id = 6` to `@y`. If multiple rows are returned (e.g., `WHERE st_address = 'alex'`), `@y` takes the last row’s value.

#### Multiple Variables

```sql
DECLARE @y INT, @name VARCHAR(20);
SELECT @y = st_age, @name = st_fname 
FROM Student
WHERE st_id = 7;
SELECT @y, @name;
```

- **Explanation**: Assigns `st_age` and `st_fname` for `st_id = 7` to `@y` and `@name`.

#### Variable in UPDATE

```sql
DECLARE @z INT;
UPDATE Student 
SET st_fname = 'ali', @z = dept_id
WHERE st_id = 7;
SELECT @z;
```

- **Explanation**: Updates `st_fname` and assigns `dept_id` to `@z` in one query.

#### Table Variable

```sql
DECLARE @t TABLE (x INT);
INSERT INTO @t
SELECT st_id FROM Student WHERE st_address = 'alex';
SELECT COUNT(*) FROM @t;
```

- **Explanation**: Declares a table variable `@t` with one column (`x`), inserts `st_id` values for students from 'alex', and counts the rows.

#### Dynamic TOP

```sql
DECLARE @x INT = 5;
SELECT TOP(@x) * FROM Student;
```

- **Explanation**: Uses `@x` to dynamically set the number of rows (5) returned by `TOP`.

#### Dynamic Query

```sql
DECLARE @col VARCHAR(20) = '*', @tab VARCHAR(20) = 'instructor';
EXECUTE ('SELECT ' + @col + ' FROM ' + @tab);
```

- **Explanation**: Constructs and executes a dynamic query to select all columns from `instructor`.

> [!warning] Variable Notes
> 
> - Variables are session-scoped and cleared when the session ends.
> - Table variables are memory-based, suitable for small datasets.
> - Dynamic queries risk SQL injection; use `sp_executesql` with parameters for safety.

## Global Variables

Global variables (prefixed with `@@`) provide system-level information.

### Examples

```sql
SELECT @@SERVERNAME; -- Server name
SELECT @@VERSION; -- SQL Server version
SELECT @@ROWCOUNT; -- Rows affected by last statement
SELECT @@ERROR; -- Error code of last statement
SELECT @@IDENTITY; -- Last inserted identity value
```

- **Explanation**:
    - `@@ROWCOUNT`: Useful after DML to check affected rows.
    - `@@ERROR`: Non-zero indicates an error.
    - `@@IDENTITY`: Retrieves the last identity value inserted.

> [!note] Global Variable Uses
> 
> - Use in control of flow to handle query outcomes.
> - `@@ERROR` is legacy; prefer `TRY-CATCH` for error handling.

## Control of Flow Statements

Control of flow statements manage query execution logic.

### Examples

#### IF-ELSE

```sql
UPDATE Student 
SET st_age += 1;
SELECT @x = @@ROWCOUNT;
IF @x > 0 
    BEGIN
        SELECT 'multi rows affected';
    END
ELSE
    BEGIN
        SELECT 'no rows affected';
    END;
```

- **Explanation**: Increments `st_age`, checks `@@ROWCOUNT`, and displays a message.

#### IF EXISTS

```sql
IF EXISTS(SELECT name FROM sys.tables WHERE name = 'students')
    SELECT 'table is existed';
ELSE
    CREATE TABLE students (id INT, name VARCHAR(20));
```

- **Explanation**: Creates `students` table if it doesn’t exist.

#### IF NOT EXISTS

```sql
IF NOT EXISTS(SELECT dept_id FROM Student WHERE dept_id = 20)
    AND NOT EXISTS(SELECT dept_id FROM Instructor WHERE dept_id = 20)
        DELETE FROM Department WHERE dept_id = 20;
ELSE
    SELECT 'table has relationship';
```

- **Explanation**: Deletes `dept_id = 20` if no students or instructors reference it.

#### TRY-CATCH

```sql
BEGIN TRY
    DELETE FROM Department WHERE Dept_Id = 20;
END TRY 
BEGIN CATCH 
    SELECT 'error';
    SELECT ERROR_LINE(), ERROR_MESSAGE(), ERROR_NUMBER();
END CATCH;
```

- **Explanation**: Attempts deletion, catches errors, and displays error details.

#### WHILE Loop

```sql
DECLARE @x INT = 10;
WHILE @x <= 20
    BEGIN 
        SET @x += 1;
        IF @x = 14
            CONTINUE;
        IF @x = 16
            BREAK;
        SELECT @x;
    END;
```

- **Explanation**: Loops from 11 to 15, skips 14 (`CONTINUE`), stops at 16 (`BREAK`).

> [!tip] Control of Flow Tips
> 
> - Use `BEGIN` and `END` to group statements.
> - `TRY-CATCH` is modern error handling; use over `@@ERROR`.
> - Avoid infinite loops in `WHILE` with clear exit conditions.

## Batch, Transaction, Script

- **Batch**: A group of queries executed together (e.g., highlighted and run).
- **Script**: Queries, often separated by `GO`, including metadata changes.
- **Transaction**: A set of queries executed as a single unit, ensuring atomicity.

### Example: Transaction

```sql
BEGIN TRY
    BEGIN TRANSACTION 
        INSERT INTO child VALUES(1);
        INSERT INTO child VALUES(2);
        INSERT INTO child VALUES(5);
    COMMIT;
END TRY
BEGIN CATCH
    ROLLBACK;
END CATCH;
```

- **Explanation**: Inserts three rows; commits if all succeed, rolls back on error.

> [!important] Transaction Best Practices
> 
> - Use `TRY-CATCH` to handle errors.
> - Minimize transaction duration to avoid locking.
> - `GO` separates batches, not part of transactions.

## Functions

SQL functions encapsulate logic, returning scalar values or tables.

### Scalar Function

```sql
CREATE FUNCTION getsname(@id INT)
RETURNS VARCHAR(20)
BEGIN 
    DECLARE @name VARCHAR(20);
    SELECT @name = st_fname FROM Student WHERE st_id = @id;
    RETURN @name;
END;

SELECT dbo.getsname(1);
```

- **Explanation**: Returns the first name for a given `st_id`. Requires schema prefix (`dbo`).

### Inline Table Function

```sql
CREATE FUNCTION getlist(@did INT)
RETURNS```sql
RETURNS TABLE
AS 
RETURN (
    SELECT ins_name, salary * 12
    FROM Instructor WHERE dept_id = @did
);

SELECT * FROM getlist(10);
```

- **Explanation**: Returns a table of instructor names and annual salaries for a department.

### Multi-Statement Table Function

```sql
CREATE FUNCTION getstuds(@format VARCHAR(20))
RETURNS @t TABLE (id INT, ename VARCHAR(20))
AS 
BEGIN 
    IF @format = 'first' 
        INSERT INTO @t 
        SELECT st_id, St_Fname FROM Student;
    ELSE IF @format = 'last'
        INSERT INTO @t 
        SELECT st_id, St_Lname FROM Student;
    ELSE IF @format = 'full'
        INSERT INTO @t
        SELECT st_id, St_Fname + ' ' + St_Lname FROM Student;
    RETURN;
END;
```

- **Explanation**: Returns a table with student IDs and names based on the format ('first', 'last', 'full').

## Windowing Functions

Windowing functions operate over a set of rows (window) defined by `OVER`.

### Examples

#### LAG and LEAD

```sql
SELECT sname, grade,
    X = LAG(grade) OVER(ORDER BY grade),
    y = LEAD(grade) OVER(ORDER BY grade)
FROM grades;
```

- **Explanation**: `LAG` gets the previous grade, `LEAD` gets the next grade, ordered by `grade`.

#### Partitioned LAG and LEAD

```sql
SELECT sname, grade, cname,
    prod_prev = LAG(grade) OVER (PARTITION BY cname ORDER BY grade),
    prod_next = LEAD(grade) OVER (PARTITION BY cname ORDER BY grade)
FROM grades;
```

- **Explanation**: Applies `LAG` and `LEAD` within each `cname` partition.

#### FIRST_VALUE and LAST_VALUE

```sql
SELECT sname, grade,
    prod_prev = LAG(sname) OVER (ORDER BY grade),
    prod_next = LEAD(sname) OVER(ORDER BY grade),
    first = FIRST_VALUE(sname) OVER (ORDER BY grade),
    last = LAST_VALUE(sname) OVER (ORDER BY grade)
FROM grades;
```

- **Explanation**: Retrieves previous/next names and first/last names in the grade-ordered window.

## Exercises

### Scalar Function: Get Month Name

```sql
CREATE FUNCTION getmonth(@date DATE)
RETURNS VARCHAR(20)
AS
BEGIN 
    DECLARE @monthname VARCHAR(20);
    SET @monthname = DATENAME(MONTH, @date);
    RETURN @monthname;
END;

SELECT dbo.getmonth('2023-10-05') AS monthname; -- Returns 'October'
```

### Table Function: Student Info

```sql
CREATE FUNCTION getstudentinfo(@stud_no INT)
RETURNS @resultttable TABLE(dept_name VARCHAR(20), stu_full VARCHAR(50))
AS
BEGIN 
    INSERT INTO @resultttable(dept_name, stu_full)
    SELECT Department.Dept_Name, Student.St_Fname + ' ' + Student.St_Lname AS full_name
    FROM Department JOIN Student
    ON Department.Dept_Id = Student.Dept_Id
    WHERE Student.St_Id = @stud_no;
    RETURN;
END;

SELECT * FROM dbo.getstudentinfo(10);
```

- **Explanation**: Returns a table with department name and full name for a student.

### Scalar Function: Null Check

```sql
CREATE FUNCTION getzft(@stud_no INT)
RETURNS VARCHAR(50)
AS
BEGIN
    DECLARE @fname VARCHAR(20), @lname VARCHAR(20);
    DECLARE @result VARCHAR(50);
    SELECT @fname = St_Fname, @lname = St_Lname
    FROM Student
    WHERE St_Id = @stud_no;
    IF @fname IS NULL AND @lname IS NULL
        SET @result = 'First name & last name are null';
    ELSE IF @fname IS NULL
        SET @result = 'First name is null';
    ELSE IF @lname IS NULL
        SET @result = 'Last name is null';
    ELSE
        SET @result = 'First name and last name are not null';
    RETURN @result;
END;
```

- **Explanation**: Checks if student names are null and returns a descriptive message.

### Table Function: Name Selector

```sql
CREATE FUNCTION getzft2(@string VARCHAR(20))
RETURNS @ResultTable TABLE (Name VARCHAR(40))
AS
BEGIN
    DECLARE @result VARCHAR(40);
    IF @string = 'first name'
        SELECT TOP (1) @result = ISNULL(Student.St_Fname, 'Unknown')
        FROM Student;
    ELSE IF @string = 'last name'
        SELECT TOP (1) @result = ISNULL(Student.St_Lname, 'Unknown')
        FROM Student;
    ELSE IF @string = 'full name'
        SELECT TOP (1) @result = ISNULL(Student.St_Fname + ' ' + Student.St_Lname, 'Unknown')
        FROM Student;
    INSERT INTO @ResultTable (Name)
    VALUES (@result);
    RETURN;
END;
```

- **Explanation**: Returns a table with one name based on the input ('first name', 'last name', 'full name').

## Dynamic SQL

Dynamic SQL constructs queries as strings for execution.

### Example

```sql
DECLARE @Columns NVARCHAR(MAX) = 'st_id,st_fname';
DECLARE @TableName NVARCHAR(MAX) = 'Student';
DECLARE @SQLQuery NVARCHAR(MAX);
SET @SQLQuery = 'SELECT ' + @Columns + ' FROM ' + @TableName;
EXEC sp_executesql @SQLQuery;
```

- **Explanation**: Dynamically selects `st_id` and `st_fname` from `Student`.

> [!warning] Dynamic SQL Risks
> 
> - Vulnerable to SQL injection; use parameterized queries with `sp_executesql`.
> - Test thoroughly to ensure valid query construction.

## Key Takeaways

> [!summary] Study Tips
> 
> - **Variables**: Use for temporary storage; table variables for small datasets.
> - **Control of Flow**: Use `TRY-CATCH` and `IF EXISTS` for robust logic.
> - **Functions**: Choose scalar for single values, table functions for result sets.
> - **Windowing**: Use `LAG`, `LEAD`, etc., for row comparisons within windows.
> - **Dynamic SQL**: Use cautiously with proper parameterization.
> - Test functions and dynamic queries with edge cases (e.g., NULLs, invalid IDs).

> [!question] Practice Questions
> 
> 1. Write a scalar function to calculate a student’s age based on `St_BirthDate`.
> 2. Create a table function to return students with grades above a given threshold.
> 3. How would you use `LAG` to find grade differences between consecutive students?
> 4. Write a dynamic SQL query to select columns based on a variable table name and filter condition.