# SQL Stored Procedures, Triggers, and XML Study Notes

This document covers SQL stored procedures (built-in and user-defined), triggers, output clauses, and XML output formatting. It includes examples and explanations formatted for easy study in Obsidian, based on provided SQL scripts. All date-related examples reflect execution on May 19, 2025, at 11:08 PM EEST.

## Stored Procedures

Stored procedures (SPs) are precompiled SQL scripts that encapsulate logic, improving performance and reusability.

### Types of Stored Procedures

- **Built-in SPs**: System-provided, e.g., `sp_bindrule`, `sp_rename`.
- **User-defined SPs**: Custom scripts created by users.
- **Triggers**: Special SPs that execute automatically on DML events (covered later).

### Examples

#### Basic Stored Procedure

```sql
CREATE PROC getst
AS
    SELECT * FROM Student;

EXEC getst;
```

- **Explanation**: Retrieves all columns from `Student`. Called using `EXEC` or procedure name.

#### Parameterized SP

```sql
CREATE PROC getstaddress @add VARCHAR(20)
AS
    SELECT st_id, st_fname, st_address
    FROM Student
    WHERE st_address = @add;

EXEC getstaddress 'alex';
```

- **Explanation**: Filters students by address provided via `@add`.

#### SP with TRY-CATCH

```sql
CREATE PROC instst @id INT, @name VARCHAR(20)
AS 
    BEGIN TRY
        INSERT INTO Student(st_id, St_Fname)
        VALUES (@id, @name);
    END TRY
    BEGIN CATCH
        SELECT 'Error';
    END CATCH;

EXEC instst 44, 'ali';
```

- **Explanation**: Inserts a student record, catches errors (e.g., duplicate `st_id`).

#### SP with Default Parameters

```sql
CREATE PROC sumdata @x INT, @y INT = 100
AS 
    SELECT @x + @y;

EXEC sumdata 3; -- Returns 103 (3 + 100)
EXEC sumdata 3, 9; -- Returns 12
EXEC sumdata @y = 9, @x = 4; -- Returns 13
```

- **Explanation**: Adds `@x` and `@y`, with `@y` defaulting to 100 if omitted.

#### SP with Range Filter

```sql
CREATE PROC getstbyage @age1 INT, @age2 INT
AS
    SELECT st_id, st_fname
    FROM Student
    WHERE st_age BETWEEN @age1 AND @age2;

EXEC getstbyage 23, 28;
```

- **Explanation**: Returns students with ages between `@age1` and `@age2`.

#### SP Output to Table

```sql
INSERT INTO tab4(st_id, st_fname)
EXEC getstbyage 23, 28;

DECLARE @t TABLE (x INT, y VARCHAR(20));
INSERT INTO @t 
EXEC getstbyage 23, 28;
SELECT COUNT(*) FROM @t;
```

- **Explanation**: Inserts SP results into a permanent table (`tab4`) or table variable (`@t`).

#### SP with Output Parameters

```sql
ALTER PROC getdata @id INT, @age INT OUTPUT, @name VARCHAR(20) OUTPUT
AS
    SELECT @age = st_age, @name = St_Fname 
    FROM Student
    WHERE st_id = @id;

DECLARE @x INT, @y VARCHAR(20);
EXEC getdata 3, @x OUTPUT, @y OUTPUT;
SELECT @x, @y;
```

- **Explanation**: Returns `st_age` and `st_fname` via output parameters, not `RETURN`.

#### Encrypted SP

```sql
CREATE PROC getdata @age INT OUTPUT, @name VARCHAR(20) OUTPUT
WITH ENCRYPTION
AS
    SELECT @age = st_age, @name = St_Fname 
    FROM Student
    WHERE st_id = @age;
```

- **Explanation**: Encrypts the SP definition to prevent viewing.

#### Dynamic SQL SP

```sql
ALTER PROC getalldata @col VARCHAR(20), @tab VARCHAR(20)
AS
    EXECUTE ('SELECT ' + @col + ' FROM ' + @tab);

EXEC getalldata '*', 'Student';
```

- **Explanation**: Constructs and executes a dynamic query based on input parameters.

### Parameter Types

|Parameter Type|Description|Example|
|---|---|---|
|Input Parameter|Passes value to SP|`@id INT`|
|Output Parameter|Returns value to caller|`@age INT OUTPUT`|
|Input-Output|Passes and returns modified value|`@age INT OUTPUT`|
|Return Parameter|Returns integer status code|`RETURN 0`|

> [!tip] Stored Procedure Tips
> 
> - Use output parameters for returning data, `RETURN` for status codes.
> - Parameterize dynamic SQL to prevent injection (use `sp_executesql`).
> - Default parameters simplify calls when values are optional.

> [!warning] SP Notes
> 
> - Encrypted SPs cannot be viewed or modified easily.
> - Test dynamic SQL for valid inputs to avoid runtime errors.

## Triggers

Triggers are implicit SPs that execute automatically in response to DML events (`INSERT`, `UPDATE`, `DELETE`).

### Characteristics

- Cannot be called directly.
- Cannot accept parameters.
- Attached to a table.
- Types: `AFTER` (post-event), `INSTEAD OF` (replaces event).

### Examples

#### AFTER INSERT Trigger

```sql
CREATE TRIGGER t1
ON Student 
AFTER INSERT 
AS
    SELECT 'welcome to iti';
```

- **Explanation**: Displays a welcome message after inserting a student.

#### AFTER UPDATE Trigger

```sql
CREATE TRIGGER t2
ON Student
FOR UPDATE 
AS 
    SELECT GETDATE(); -- Returns '2025-05-19 23:08:00'
```

- **Explanation**: Displays the current date/time after updating `Student`.

#### INSTEAD OF DELETE Trigger

```sql
CREATE TRIGGER t3
ON Student 
INSTEAD OF DELETE
AS
    SELECT 'Not allowed for user = ' + SUSER_NAME();
```

- **Explanation**: Prevents deletion and displays a message with the current user.

#### INSTEAD OF Multi-Event Trigger

```sql
CREATE TRIGGER t4 
ON Department
INSTEAD OF INSERT, UPDATE, DELETE
AS
    SELECT 'not allowed';
```

- **Explanation**: Blocks all DML operations on `Department`.

#### Conditional Trigger

```sql
CREATE TRIGGER t7
ON sales.student
AFTER UPDATE
AS
    IF UPDATE(name)
        SELECT 'hi';
```

- **Explanation**: Executes only if the `name` column is updated.

#### Trigger Management

```sql
ALTER TABLE Department DISABLE TRIGGER t4;
ALTER TABLE Department ENABLE TRIGGER t4;
```

- **Explanation**: Disables or enables the `t4` trigger.

#### Auditing Trigger

```sql
CREATE TABLE history
(
    _User VARCHAR(20),
    _date DATE,
    _oldid INT,
    _Newid INT
);

CREATE TRIGGER t10
ON topic 
INSTEAD OF UPDATE 
AS
    IF UPDATE(top_id)
        BEGIN
            DECLARE @new INT, @old INT;
            SELECT @old = top_id FROM deleted;
            SELECT @new = top_id FROM inserted;
            INSERT INTO history
            VALUES (SUSER_NAME(), GETDATE(), @old, @new);
        END;
```

- **Explanation**: Logs changes to `top_id` in the `history` table.

#### Trigger with Logic

```sql
CREATE TRIGGER t9
ON course
INSTEAD OF DELETE 
AS
    IF FORMAT(GETDATE(), 'dddd') != 'Friday'
        BEGIN
            DELETE FROM course WHERE crs_id = (SELECT crs_id FROM deleted);
        END;
```

- **Explanation**: Allows deletion only on non-Fridays.

### Special Tables

- **inserted**: Contains new rows for `INSERT` or `UPDATE`.
- **deleted**: Contains old rows for `DELETE` or `UPDATE`.

> [!note] Trigger Notes
> 
> - Use `inserted` and `deleted` for auditing or validation.
> - `INSTEAD OF` triggers override default DML actions.
> - Triggers inherit the schema of the table (e.g., `dbo.t1`).

## Output Clause

The `OUTPUT` clause captures data from DML operations, acting like a runtime trigger.

### Examples

#### DELETE with OUTPUT

```sql
DELETE FROM Student 
OUTPUT GETDATE(), deleted.St_Fname
WHERE St_Id = 44;
```

- **Explanation**: Deletes a student and outputs the current date (`2025-05-19`) and deleted `St_Fname`.

#### UPDATE with OUTPUT

```sql
UPDATE Student
SET St_Fname = 'ali'
OUTPUT SUSER_NAME(), inserted.St_Age
WHERE st_id = 1;
```

- **Explanation**: Updates `St_Fname` and outputs the current user and new `St_Age`.

#### OUTPUT to Table

```sql
UPDATE Student 
SET st_fname = 'ali'
OUTPUT SUSER_NAME(), inserted.St_Age INTO history
WHERE st_id = 1;
```

- **Explanation**: Stores output in the `history` table.

#### INSERT with OUTPUT

```sql
INSERT INTO Student(st_id, st_fname)
OUTPUT 'welcome to iti'
VALUES (444, 'ali');
```

- **Explanation**: Inserts a row and outputs a welcome message.

> [!success] OUTPUT Benefits
> 
> - Captures DML results without triggers.
> - Can redirect data to tables for auditing.
> - Uses `inserted` and `deleted` like triggers.

## XML Output

The `FOR XML` clause formats query results as XML.

### Examples

#### Basic XML

```sql
SELECT * 
FROM Student 
FOR XML RAW('student');
```

- **Explanation**: Outputs `Student` rows as XML, with each row as a `<student>` element and columns as attributes.

#### XML with Elements

```sql
SELECT * 
FROM Student 
FOR XML RAW('student'), ELEMENTS;
```

- **Explanation**: Columns are represented as child elements instead of attributes.

#### XML with Root

```sql
SELECT * 
FROM Student 
FOR XML RAW('student'), ELEMENTS, ROOT('iti');
```

- **Explanation**: Wraps the XML in a root element `<iti>`.

### Sample Output (Simplified)

```xml
<iti>
    <student>
        <st_id>1</st_id>
        <st_fname>Ahmed</st_fname>
    </student>
    <student>
        <st_id>2</st_id>
        <st_fname>Ali</st_fname>
    </student>
</iti>
```

> [!tip] XML Tips
> 
> - Use `ELEMENTS` for structured XML with columns as tags.
> - Add `ROOT` for valid XML with a single root element.
> - Useful for data exchange or API integration.

## Key Takeaways

> [!summary] Study Tips
> 
> - **Stored Procedures**: Use for reusable logic; leverage output parameters for data return.
> - **Triggers**: Automate actions on DML; use `inserted`/`deleted` for auditing.
> - **OUTPUT Clause**: Capture DML results efficiently, with or without triggers.
> - **XML Output**: Format data for interoperability; use `ELEMENTS` and `ROOT` for clarity.
> - Test triggers and SPs with edge cases (e.g., invalid IDs, NULLs).
> - Use `TRY-CATCH` in SPs for robust error handling.

> [!question] Practice Questions
> 
> 1. Write a stored procedure to update `Student` age and return the new age via an output parameter.
> 2. Create an `AFTER INSERT` trigger to log new `Student` insertions in a history table.
> 3. How would you use the `OUTPUT` clause to capture both old and new `st_fname` after an update?
> 4. Modify the XML query to output only `st_id` and `st_fname` with a root element `students`.