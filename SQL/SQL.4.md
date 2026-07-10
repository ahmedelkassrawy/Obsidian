# SQL Ranking and Adhoc Queries Study Notes

This document covers SQL ranking functions (`ROW_NUMBER`, `DENSE_RANK`, `NTILE`) and adhoc queries, including conditional logic (`CASE`, `IIF`), date formatting, and data updates. It includes examples and explanations formatted for easy study in Obsidian, based on provided SQL scripts. All examples assume execution on May 19, 2025, at 11:00 PM EEST.

## Ranking Functions

Ranking functions assign a rank or group number to rows based on an `OVER` clause, which defines the ordering or partitioning of the data. Common functions include `ROW_NUMBER`, `DENSE_RANK`, and `NTILE`.

### Key Concepts

- **OVER Clause**: Specifies the window for ranking, including `ORDER BY` (required) and optional `PARTITION BY`.
- **PARTITION BY**: Divides the data into groups (partitions) before applying the ranking.
- **Filtering**: Ranking functions cannot be directly used in `WHERE` clauses; use a subquery or CTE.

### Examples of Ranking Functions

#### ROW_NUMBER

```sql
SELECT *, ROW_NUMBER() OVER(ORDER BY st_age DESC) AS RN
FROM Student;
```

- **Explanation**: Assigns a unique sequential number to each row, ordered by `st_age` (descending). The oldest student gets `RN = 1`.
- **Use Case**: Identify the nth row in a sorted list.

#### DENSE_RANK

```sql
SELECT *, DENSE_RANK() OVER(ORDER BY st_age DESC) AS DR
FROM Student;
```

- **Explanation**: Assigns a rank to each unique `st_age`, with ties sharing the same rank. Unlike `ROW_NUMBER`, gaps are not created (e.g., 1, 1, 2 instead of 1, 2, 3 for ties).
- **Use Case**: Rank students by age without skipping numbers for ties.

#### Filtering with Subquery

```sql
SELECT *
FROM (
    SELECT *, ROW_NUMBER() OVER(ORDER BY st_age DESC) AS RN
    FROM Student
) AS Newtable
WHERE RN = 1;
```

- **Explanation**: Returns the oldest student (where `RN = 1`). The subquery is needed because `ROW_NUMBER` cannot be directly filtered in `WHERE`.
- **Result**: One row with the highest `st_age`.

#### ROW_NUMBER with PARTITION BY

```sql
SELECT *
FROM (
    SELECT *, ROW_NUMBER() OVER(PARTITION BY dept_id ORDER BY st_age DESC) AS RN
    FROM Student
) AS Newtable
WHERE RN = 1;
```

- **Explanation**: Assigns `ROW_NUMBER` within each `dept_id` partition, ordered by `st_age` (descending). Filters to return the oldest student in each department.
- **Use Case**: Find the top record per group (e.g., oldest student per department).

#### NTILE

```sql
SELECT *
FROM (
    SELECT *, NTILE(4) OVER(ORDER BY st_age DESC) AS G
    FROM Student
) AS NEWTABLE
WHERE G = 1;
```

- **Explanation**: Divides rows into 4 equal groups (quartiles) based on `st_age` (descending). Group 1 contains the oldest 25% of students.
- **Use Case**: Segment data into buckets (e.g., performance tiers).

### Ranking Functions Summary

|Function|Description|Ties Handling|
|---|---|---|
|`ROW_NUMBER()`|Assigns a unique sequential number to each row.|No ties; each row gets a unique number.|
|`DENSE_RANK()`|Assigns a rank, with ties sharing the same rank.|Ties get the same rank; no gaps.|
|`NTILE(n)`|Divides rows into `n` equal groups.|Distributes ties across groups.|

> [!tip] Ranking Tips
> 
> - Use `PARTITION BY` to rank within groups.
> - Wrap ranking queries in subqueries or CTEs for filtering.
> - Choose `DENSE_RANK` over `ROW_NUMBER` when ties should share ranks.

## Adhoc Queries

Adhoc queries use conditional logic, type conversions, and date functions to manipulate or format data dynamically.

### Conditional Logic

#### CASE Statement

```sql
SELECT ins_name, 
       CASE 
           WHEN salary >= 3000 THEN 'high sal'
           WHEN salary < 3000 THEN 'low'
           ELSE 'NO Value'
       END AS Newsal
FROM Instructor;
```

- **Explanation**: Categorizes instructors based on salary: `high sal` (≥ 3000), `low` (< 3000), or `NO Value` (NULL).
- **Use Case**: Create readable labels for reporting.

#### IIF (Ternary Operator)

```sql
SELECT ins_name, IIF(salary >= 3000, 'high', 'low')
FROM Instructor;
```

- **Explanation**: Simplified `CASE` for binary conditions. Returns `high` if `salary >= 3000`, else `low`.
- **Use Case**: Quick conditional logic for two outcomes.

### Date and Type Conversion

#### CONVERT and CAST

```sql
SELECT CONVERT(VARCHAR(20), GETDATE());
SELECT CAST(GETDATE() AS VARCHAR(20));
```

- **Explanation**: Converts the current date/time (e.g., `2025-05-19 23:00:00`) to a string. Both produce similar output (e.g., `May 19 2025 11:00PM`).
- **Use Case**: Format dates for display.

#### FORMAT and Date Functions

```sql
SELECT FORMAT(GETDATE(), 'dd'); -- Returns '19'
SELECT DAY(GETDATE()); -- Returns 19
SELECT EOMONTH(GETDATE()); -- Returns '2025-05-31'
SELECT FORMAT(EOMONTH(GETDATE()), 'dd'); -- Returns '31'
SELECT EOMONTH('1/1/2000'); -- Returns '2000-01-31'
```

- **Explanation**:
    - `FORMAT(GETDATE(), 'dd')`: Extracts the day of the month as a string.
    - `DAY(GETDATE())`: Extracts the day as an integer.
    - `EOMONTH()`: Returns the last day of the month for the given date.
- **Use Case**: Extract or format date components for reports or calculations.

### Updating Data with CASE

```sql
UPDATE Instructor
SET salary = 
    CASE
        WHEN salary >= 3000 THEN salary * 1.10
        ELSE salary * 1.20
    END;
```

- **Explanation**: Increases `salary` by 10% if ≥ 3000, or 20% otherwise.
- **Use Case**: Apply conditional updates to data.

> [!warning] Adhoc Query Notes
> 
> - Test `UPDATE` statements in a transaction (`BEGIN TRAN`, `ROLLBACK`) to avoid unintended changes.
> - `IIF` is SQL Server-specific; use `CASE` for portability.
> - `FORMAT` is flexible but slower than `CONVERT` for simple conversions.

## Key Takeaways

> [!summary] Study Tips
> 
> - **Ranking Functions**: Use `ROW_NUMBER` for unique ranks, `DENSE_RANK` for ties, and `NTILE` for grouping.
> - **Adhoc Queries**: Leverage `CASE` and `IIF` for conditional logic, and `CONVERT`/`FORMAT` for data presentation.
> - **Subqueries/CTEs**: Essential for filtering ranking results.
> - **Date Functions**: Use `EOMONTH` and `FORMAT` for precise date handling.
> - Always verify `UPDATE` logic to prevent data errors.

> [!question] Practice Questions
> 
> 1. How would you find the second-oldest student using `ROW_NUMBER()`?
> 2. Write a query to divide instructors into 3 salary tiers using `NTILE`.
> 3. How would you format `GETDATE()` to show only the year (e.g., '2025')?
> 4. Modify the `UPDATE` query to cap salary increases at 5000.