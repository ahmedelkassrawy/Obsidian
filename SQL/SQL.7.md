# SQL Date Formatting, Self-Joins, and CTEs Study Notes
## Date Formatting with CONVERT

The `CONVERT` function formats dates into various styles by specifying a style code.

### Example: Multiple Date Formats

```sql
SELECT 
    'Style 1 (Default)' AS StyleName,
    CONVERT(VARCHAR, GETDATE(), 100) AS FormattedDate
UNION ALL
SELECT 
    'Style 2 (MM/DD/YY)' AS StyleName,
    CONVERT(VARCHAR, GETDATE(), 1) AS FormattedDate
UNION ALL
SELECT 
    'Style 3 (YYYY-MM-DD)' AS StyleName,
    CONVERT(VARCHAR, GETDATE(), 23) AS FormattedDate
UNION ALL
SELECT 
    'Style 4 (DD/MM/YYYY)' AS StyleName,
    CONVERT(VARCHAR, GETDATE(), 103) AS FormattedDate
UNION ALL
SELECT 
    'Style 5 (Month DD, YYYY)' AS StyleName,
    CONVERT(VARCHAR, GETDATE(), 107) AS FormattedDate
UNION ALL
SELECT 
    'Style 6 (HH:MM:SS)' AS StyleName,
    CONVERT(VARCHAR, GETDATE(), 108) AS FormattedDate
UNION ALL
SELECT 
    'Style 7 (Mon DD, YYYY HH:MM:SS AM/PM)' AS StyleName,
    CONVERT(VARCHAR, GETDATE(), 109) AS FormattedDate;
```

- **Explanation**: Uses `UNION ALL` to combine different date formats of the current date/time (`2025-05-19 23:02:00`).
- **Sample Output**:
    
    |StyleName|FormattedDate|
    |---|---|
    |Style 1 (Default)|May 19 2025 11:02PM|
    |Style 2 (MM/DD/YY)|05/19/25|
    |Style 3 (YYYY-MM-DD)|2025-05-19|
    |Style 4 (DD/MM/YYYY)|19/05/2025|
    |Style 5 (Month DD, YYYY)|May 19, 2025|
    |Style 6 (HH:MM:SS)|23:02:00|
    |Style 7 (Mon DD, YYYY HH:MM:SS AM/PM)|May 19, 2025 11:02:00PM|
    

> [!tip] Date Formatting Tips
> 
> - Use style code `23` for ISO-compliant `YYYY-MM-DD`.
> - `FORMAT` is an alternative but slower than `CONVERT`.
> - Specify `VARCHAR` length to avoid truncation (e.g., `VARCHAR(20)`).

## Self-Joins

A self-join is a join where a table is joined with itself, often to model hierarchical relationships.

### Example: Student Supervisor

```sql
SELECT x.st_fname, y.St_Id, y.st_fname AS Supervisor_name
FROM Student x 
JOIN Student y
ON y.St_id = x.St_super;
```

- **Explanation**:
    - `Student x` represents students; `Student y` represents supervisors.
    - `x.St_super` is a `y.St_id`, linking students to their supervisors.
    - Returns each student’s name, supervisor’s ID, and supervisor’s name.
- **Use Case**: Model hierarchical relationships (e.g., student-supervisor).

> [!note] Self-Join Notes
> 
> - Use table aliases (`x`, `y`) for clarity.
> - Ensure the joining column (`St_super`) exists and contains valid `St_id` values.
> - Use `LEFT JOIN` if some students have no supervisor (`St_super` is `NULL`).

## Common Table Expressions (CTEs)

CTEs provide a temporary result set for cleaner, more readable queries, often used with ranking or randomization.

### Example: Random Student per Department

```sql
;WITH RandomStudents AS (
    SELECT 
        S.St_Id,
        S.St_Fname,
        S.St_Lname,
        D.Dept_Name AS DepartmentName,
        ROW_NUMBER() OVER (PARTITION BY S.Dept_Id ORDER BY NEWID()) AS RandomRank
    FROM Student S
    JOIN Department D ON S.Dept_Id = D.Dept_Id
)
SELECT 
    St_ID,
    St_Fname,
    St_Lname,
    DepartmentName
FROM RandomStudents
WHERE RandomRank = 1;
```

- **Explanation**:
    - CTE `RandomStudents` assigns a `ROW_NUMBER` to each student within their department (`PARTITION BY S.Dept_Id`), ordered randomly (`NEWID()`).
    - Filters to `RandomRank = 1`, selecting one random student per department.
- **Use Case**: Random sampling within groups.

### Example: Top 2 Salaries per Department

```sql
WITH RankedSalaries AS (
    SELECT 
        D.Dept_Name AS DepartmentName,
        I.Ins_Name,
        I.Salary,
        ROW_NUMBER() OVER (PARTITION BY I.Dept_Id ORDER BY I.Salary DESC) AS SalaryRank
    FROM Instructor I
    JOIN Department D ON I.Dept_Id = D.Dept_Id
    WHERE I.Salary IS NOT NULL
)
SELECT 
    DepartmentName,
    Ins_Name,
    Salary
FROM RankedSalaries
WHERE SalaryRank <= 2;
```

- **Explanation**:
    - CTE `RankedSalaries` ranks instructors by salary within each department.
    - Filters to `SalaryRank <= 2`, returning the top 2 highest-paid instructors per department.
- **Use Case**: Identify top performers per group.

> [!success] CTE Advantages
> 
> - Improves readability over subqueries.
> - Reusable within the same query.
> - Ideal for ranking, grouping, or recursive queries.

## Key Takeaways

> [!summary] Study Tips
> 
> - **Date Formatting**: Use `CONVERT` with style codes for specific formats; prefer `23` for standards.
> - **Self-Joins**: Model hierarchies; use clear aliases and verify foreign key data.
> - **CTEs**: Simplify complex queries, especially for ranking (`ROW_NUMBER`) or randomization (`NEWID()`).
> - Test queries with small datasets to ensure correct output.
> - Combine CTEs with `JOIN` for enriched data (e.g., department names).

> [!question] Practice Questions
> 
> 1. How would you modify the date formatting query to include a custom format like `YYYY/MM/DD HH:MM`?
> 2. Write a self-join query to list students and their supervisors, including students without supervisors.
> 3. Create a CTE to select the youngest student per department.
> 4. How would you find the 3rd highest salary per department using a CTE?