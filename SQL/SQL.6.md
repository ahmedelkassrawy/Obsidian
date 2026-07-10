# SQL Constraints and Rules Study Notes

This document covers SQL constraints, rules, defaults, and custom data types, focusing on their syntax, usage, and key concepts. It includes examples from a provided `emp` table schema and related operations, formatted for easy study in Obsidian.

## Overview of Key Concepts

> [!info] Key Definitions
> 
> - **Constraints**: Enforce rules on table data to ensure integrity (e.g., primary keys, foreign keys, checks).
> - **Rules**: Database objects that enforce conditions on columns, less common than constraints.
> - **Defaults**: Specify default values for columns when no value is provided.
> - **Datatypes**: Define the type of data a column can store (e.g., `INT`, `VARCHAR`).
> - **Schemas**: Logical containers within a database that hold tables and other objects.

> [!note] Database Structure
> 
> - **Databases** contain **schemas**.
> - **Schemas** contain **tables** and other objects like rules and defaults.
> - Constraints apply to new data and can be shared across tables.
> - Rules and defaults are bound to columns or data types for reusable logic.

## Creating the `emp` Table

The `emp` table demonstrates various constraints and computed columns. Below is the creation script with annotations.

```sql
CREATE TABLE emp
(
    eid INT, -- Primary key component
    ename VARCHAR(20), -- Primary key component
    eadd VARCHAR(20) DEFAULT 'alex', -- Default value for address
    hiredate DATE DEFAULT GETDATE(), -- Default to current date
    sal INT UNIQUE, -- Unique constraint on salary
    overtime INT,
    netsal AS (ISNULL(sal, 0) + ISNULL(overtime, 0)) PERSISTED, -- Computed column (persisted for storage)
    BD DATE, -- Birth date
    age AS (YEAR(GETDATE()) - YEAR(BD)), -- Computed column (not persisted)
    gender VARCHAR(1),
    hour_rate INT NOT NULL, -- Cannot be null
    did INT, -- Foreign key to Department

    -- Composite primary key
    CONSTRAINT c1 PRIMARY KEY (eid, ename),

    -- Unique constraint on sal (redundant with inline UNIQUE)
    CONSTRAINT c2 UNIQUE (sal),

    -- Unique constraint on overtime
    CONSTRAINT c3 UNIQUE (overtime),

    -- Composite unique constraint
    CONSTRAINT c4 UNIQUE (overtime, sal),

    -- Check salary > 1000
    CONSTRAINT c5 CHECK (sal > 1000),

    -- Check valid addresses
    CONSTRAINT c6 CHECK (eadd IN ('cairo', 'mansoura', 'alex')),

    -- Check gender is 'F' or 'M'
    CONSTRAINT c7 CHECK (gender = 'F' OR gender = 'M'),

    -- Check overtime between 100 and 500
    CONSTRAINT c8 CHECK (overtime BETWEEN 100 AND 500),

    -- Foreign key to Department(dept_id)
    CONSTRAINT c9 FOREIGN KEY (did) REFERENCES Department(dept_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);
```

> [!tip] Notes on `emp` Table
> 
> - The composite primary key (`eid`, `ename`) ensures unique combinations of employee ID and name.
> - `netsal` is a **persisted** computed column, stored physically to improve query performance.
> - `age` is a non-persisted computed column, calculated on-the-fly.
> - The `UNIQUE` constraint on `sal` is defined both inline and as a named constraint (`c2`), which is redundant but valid.

### Constraints Summary

|Constraint Name|Type|Description|Columns Affected|
|---|---|---|---|
|`c1`|Primary Key|Composite key on `eid` and `ename`|`eid`, `ename`|
|`c2`|Unique|Ensures unique `sal` values|`sal`|
|`c3`|Unique|Ensures unique `overtime` values|`overtime`|
|`c4`|Unique|Ensures unique combinations of `overtime`, `sal`|`overtime`, `sal`|
|`c5`|Check|Ensures `sal` > 1000|`sal`|
|`c6`|Check|Ensures `eadd` is 'cairo', 'mansoura', or 'alex'|`eadd`|
|`c7`|Check|Ensures `gender` is 'F' or 'M'|`gender`|
|`c8`|Check|Ensures `overtime` between 100 and 500|`overtime`|
|`c9`|Foreign Key|References `Department(dept_id)`|`did`|

## Modifying Constraints

Constraints can be added or dropped using `ALTER TABLE`. Example:

```sql
-- Add a check constraint on hour_rate
ALTER TABLE emp ADD CONSTRAINT c100 CHECK (hour_rate > 100);

-- Drop the check constraint
ALTER TABLE emp DROP CONSTRAINT c100;
```

> [!warning] Dropping Constraints
> 
> - Dropping a constraint removes its enforcement, potentially allowing invalid data.
> - Ensure no dependencies (e.g., foreign keys) are affected before dropping.

## Rules

Rules are database objects that enforce conditions on column values, similar to check constraints but reusable across tables. They are stored under **Programmability > Rules** in SQL Server.

### Creating and Binding Rules

```sql
-- Create a rule to ensure values > 1000
CREATE RULE r1 AS @x > 1000;

-- Bind rule to columns
sp_bindrule r1, 'instructor.salary';
sp_bindrule r1, 'emp.overtime';

-- Unbind rule from columns
sp_unbindrule r1, 'emp.overtime';
sp_unbindrule r1, 'instructor.salary';

-- Drop the rule
DROP RULE r1;
```

> [!important] Rule Limitations
> 
> - Only **one rule** can be bound to a column.
> - Rules are less flexible than check constraints and are considered legacy in modern SQL Server versions.
> - The `@x` in the rule acts as a placeholder for the column value.

## Defaults

Defaults provide fallback values for columns when no value is specified during insertion. They are stored under **Programmability > Defaults**.

### Creating and Binding Defaults

```sql
-- Create a default value of 1000
CREATE DEFAULT def1 AS 1000;

-- Bind default to columns
sp_bindefault def1, 'instructor.salary';
sp_bindefault def1, 'emp.overtime';

-- Unbind default from columns
sp_unbindefault def1, 'emp.overtime';
sp_unbindefault def1, 'in obraz instructor.salary';

-- Drop the default
DROP DEFAULT def1;
```

> [!note] Default Behavior
> 
> - Defaults apply only when no value is provided (e.g., `INSERT` omits the column or specifies `NULL`).
> - Like rules, defaults are reusable but considered legacy compared to inline `DEFAULT` constraints.

## Custom Data Types with Rules and Defaults

Custom data types can combine a base type with rules and defaults for reusable column definitions.

### Creating a Custom Data Type

```sql
-- Create rule and default
CREATE RULE r1 AS @x > 1000;
CREATE DEFAULT def1 AS 5000;

-- Create custom data type
sp_addtype ComplexDT, 'int';
sp_bindrule r1, ComplexDT;
sp_bindefault def1, ComplexDT;

-- Use custom data type in a table
CREATE TABLE table1
(
    id INT,
    name VARCHAR(20),
    salary ComplexDT
);
```

> [!success] Why Use Custom Data Types?
> 
> - **Reusability**: Apply consistent rules and defaults across multiple tables.
> - **Consistency**: Ensure columns like `salary` always have the same constraints (e.g., `> 1000`, default `5000`).
> - **Limitation**: Only one rule per data type, as rules are tied to the data type definition.

### Example Behavior of `ComplexDT`

- Type: `INT`
- Rule: Values must be `> 1000`
- Default: `5000` if no value is provided
- Usage in `table1.salary` enforces these rules automatically.

## Key Takeaways

> [!summary] Study Tips
> 
> - **Constraints** are the primary way to enforce data integrity in modern SQL Server.
> - **Rules** and **Defaults** are legacy features; prefer inline constraints (`CHECK`, `DEFAULT`) for new designs.
> - **Custom Data Types** are useful for standardizing column definitions across tables.
> - Use `ALTER TABLE` to modify constraints dynamically.
> - Always test constraints and rules to ensure they don’t conflict (e.g., redundant unique constraints).

> [!question] Practice Questions
> 
> 1. What happens if you try to bind two rules to the same column?
> 2. How does a persisted computed column (`netsal`) differ from a non-persisted one (`age`)?
> 3. Why might you choose a composite primary key (`eid`, `ename`) over a single-column key?
> 4. How does `ON DELETE SET NULL` in the foreign key constraint (`c9`) affect data integrity?