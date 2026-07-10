common problems in ssms

- to avoid alter table columns problem
    
    tools → options → designers → table and database designers
    
    ![[Untitled.png]]
    
- when restoring any database to see the database diagram
    
    right click on the database → files → ont the onwer field write → sa
    
    sa = “sql admin”
    

  

# **Categories of T-SQL Statements**

## DDL – Data Definition Language

- create
    
    ```SQL
    create table table_name 
    ("column 1" "data_type",
    "column 2" "data_type", ... ) 
    ```
    
    example
    
    ```SQL
    create table employee
    (id int primary key,
    fname char(50),
    lname char(50),
    birthdated date)
    ```
    
- alter
    
    ```POSTGRESQL
     /* add */
     ALTER TABLE table_name ADD column_name datatype
     --ex.
     alter table employee add address varchar(50)
    /* drop */
    ALTER TABLE table_name DROP column_name 
    --ex.
    alter table employee drop adress
    
    ```
    
      
    
      
    
- drop
    
    ```SQL
    drop table employee
    ```
    
- select into
    
    ```SQL
    --create table from existsing one
    select * into tab2 --> the new table
    from Student
    --
    select st_id,st_fname into tab5
    from Student
    where St_Address='alex'
    -- insert the new table into another database
    select * into company_sd.dbo.student 
    from student
    --
    select * into tab7
    from Student
    where 1=2  --> flase condition ,so it will insert empty table
    
    ```
    

## DML – Data Manipulation Language

- insert
    
    ```SQL
    INSERT [INTO] table_or_view [(column_list)] data_values
    --ex
    insert into employee 
    values(1,'hassan', 'elsayed', GETDATE())
    
    --Inserting Multiple Rows 
    insert into employee 
    values(2,'ahmed', 'ali', GETDATE()),
    (3,'ali', 'ahmed', 1/1/2000)
    
    -- insert based on select
    insert into table
    select ....
    
    -- insert based on excute
    insert into table
    execute SP_NAME
    
    ```
    
- bulk insert
    
    - insert data from file [delimited file]
    
    ```SQL
    bulk insert tab5 --> the new table's name
    from 'g:\employee.txt' -->path
    with (fieldterminator=',')
    ```
    
- delete
    
    ```SQL
    --delete row
    
    delete from employee where id=3
    
    truncate table employee
    DELETE FROM employee; -- delet rows not table
    ------------------------------------
    DROP TABLE employee; -- delet table completly
    ```
    
- update
    
    ```SQL
    UPDATE table_name
    SET column1 = value1, column2 = value2, ...
    WHERE condition; -- without condition it will update all rows
    
    --ex.
    update employee
    set salary = 20000 , birthdated= '2000/5/5'
    where id =3
    ```
    

- ==merge==
    
    ```SQL
    create table Lastt
    (Xid int,Xname varchar(10),Xval int)
    
    create table dailyt
    (Yid int,Yname varchar(10),Yval int)
    
    Merge into Lastt as T   --target table
    using dailyt as S       --Source table
    On T.Xid= S.Yid
    
    When Matched Then
    	Update
    		Set T.Xval = S.yval
    When not Matched Then  ---not matched by target
    	Insert
    	values(S.Yid,S.yname,S.yval);
    ```
    
    ![[Untitled 1.png]]
    
    ![[Untitled 2.png]]
    

## DQL - Data Query Language (Select)

### select

```SQL
-- between
SELECT * FROM Products
WHERE Price BETWEEN 50 AND 60;  
------------------------------

-- like
SELECT * FROM Customers
WHERE City LIKE 's%';
-------------------------------

-- in
SELECT * FROM Customers
WHERE City IN ('Paris','London');
-------------------------------------

-- and or
SELECT * FROM Customers
WHERE Country = 'Spain' 
AND CustomerName LIKE 'G%' 
OR CustomerName LIKE 'R%';
-----------------------------

-- not
SELECT * FROM Customers
WHERE NOT Country = 'Spain';

-- not like
SELECT * FROM Customers
WHERE CustomerName NOT LIKE 'A%';

-- not between
SELECT * FROM Customers
WHERE CustomerID NOT BETWEEN 10 AND 60;

-- not in
SELECT * FROM Customers
WHERE City NOT IN ('Paris', 'London');
------------------------------------------

-- null
SELECT CustomerName, ContactName, Address
FROM Customers
WHERE Address IS NULL;

-- not null
SELECT CustomerName, ContactName, Address
FROM Customers
WHERE Address IS NOT NULL;
```

## Wildcard Characters

[SQL Wildcard Characters (w3schools.com)](https://www.w3schools.com/sql/sql_wildcards.asp)

|   |   |
|---|---|
|%|Represents zero or more characters|
|_|Represents a single character|
|-|Represents any single character within the specified range *|
|[]|Represents any single character within the brackets *|
|{}|Represents any escaped character **|

### Using the `%` Wildcard

```SQL
SELECT * FROM Customers
WHERE CustomerName LIKE '%es';
--Return all customers that ends with the pattern 'es':

SELECT * FROM Customers
WHERE CustomerName LIKE '%mer%';
--Return all customers that contains the pattern 'mer':
```

## Using the `_` Wildcard

```SQL
SELECT City FROM Customers
WHERE City LIKE '_ondon';
--Return all Cities starting with one character, followed by "ondon"
-- london

SELECT * FROM Customers
WHERE City LIKE 'L___on';
--City starting with "L", followed by any 3 characters, ending with "on"
```

### Using the `[ ]` Wildcard

```SQL
SELECT * FROM Customers
WHERE CustomerName LIKE '[bsp]%';
--Return all customers starting with either "b", "s", or "p"
```

### Using the `-` Wildcard

```SQL
SELECT * FROM Customers
WHERE CustomerName LIKE '[a-f]%';
```

  

### order by

```SQL
SELECT column1, column2, ...
FROM table_name
ORDER BY column1, column2, ... ASC|DESC;

/*
ORDER BY Several Columns
The following SQL statement selects all customers from the
 "Customers" table, sorted by the "Country" and the "CustomerName"
  column. This means that it orders by Country, but if some rows 
  have the same Country, it orders them by CustomerName:
*/

SELECT * FROM Customers
ORDER BY Country ASC, CustomerName DESC;

SELECT column1, column2, ...
FROM table_name
ORDER BY 1; // first column in select columns
```

### subquery

> can’t use aggregate functions with where because of the excution order  
> so we overcome that by using subqueries  

```SQL
select st_age
from Student
where st_age > (select avg(st_age) from Student)

-----------

select *, (select count(st_id) from Student)
from Student
```

**return the name of the departments that contain students**

```SQL
select * from Department
where Dept_Id in (select Dept_Id
from Student
where Dept_Id is not null
)
```

another way to do it with join

```SQL
select distinct d.Dept_Name from Department d
join Student s on d.Dept_Id = s.Dept_Id
```

![[Untitled 3.png]]

### joins

- ==Type of join==
    
    - cross join
        - cartesian product
    - inner join
        - equijoin
    - outer join
        - left
        - right
        - full
    - self join (unary relationship)
    
    in case you can not open a diagram
    
    - right click, properties ,files, write sa
    
      
    
- join
    
    ```SQL
    select * from employee e 
    join Dependent d on e.ssn = d.ESSN
    
    
    -- join with more than one table
    select p.Pnumber, d.Dname,
    e.Lname , e.Address, e.Bdate, p.city
    from Project p
    join Departments d on p.Dnum = d.Dnum
    join employee e on d.Dnum = e.Dno
    where city = 'cairo'
    ```
    
    - self join
        
        ```SQL
        
        select FirstN as employee, FirstN as super from 
        Employee X, Employee Y; 
        // Employee X, Employee Y -> create a copy of my table
        // any join from parent child one has PK and another has FK 
        // table in database is child
        // new table has PK, old table has  FK
        
        select FirstN as employee, FirstN as super from 
        Employee X, Employee Y
        where x.superssn = y.SSN; 
        ```
        
    - Isnull
        
        ```SQL
        select isnull(fname, '') from student;
        // replace any null value bt  ''
        ```
        

### aggregate functions

count & sum

```SQL
select count(id) from employee
select sum(salary) from employee
```

max & min

```SQL
select min(salary), max(salary)
 from employee
```

avg

```SQL
select avg(salary) from employee

select avg( isnull(salary, 0) ) from employee --take in count null values
```

- top
    
    - select
    
    ```SQL
    SELECT TOP 2 Salary 
        FROM Employee 
        ORDER BY Salary DESC
    ```
    
    - update
    
    ```SQL
    UPDATE TOP (5) Students
    SET Name = 'Updated Name'
    WHERE Name = 'John Doe';
    -- top percent
    UPDATE TOP (10) PERCENT Students
    SET Name = 'Updated Name'
    WHERE Name = 'John Doe';
    ```
    
    Delete
    
    ```SQL
    DELETE TOP (3) FROM Students
    WHERE Name = 'Jane Smith';
    
    -- top percent
    DELETE TOP (5) PERCENT FROM Students
    WHERE Name = 'Jane Smith';
    ```
    
- group by
    
    > aggregate functions + normal clum → we should use groub by
    
    ```SQL
    select sum(salary) , did
    from employee
    group by did
    ```
    
    group by with 2 columns
    
    ```SQL
    select count (st_id,st_adress,dep_id)
    from student
    group by st_adress,dep_id
    ```
    
    ![[f40dadc2-c865-4213-9305-7314b2459526.png]]
    
- group by with where & having
    
    ![[Untitled 4.png]]
    
    - having
        
        ```SQL
        select sum(salary),did
         from employee
         group by did
         having sum(salary) > 25000 --filters the group
        ```
        
        where with having
        
        ![[Untitled 5.png]]
        

### set operators → union ,intersect , except

- **union all**

```SQL
select st_fname
from Student
union all
select ins_name
from Instructon
--return all students name and instructors name in one column 
```

- **union** → same as union but returns unique values and ordered
- **intersect** → returns the common rows present in both tables

```SQL
select st_fname, st_id
from Student
intersect
select ins_name, ins_id
from Instructor
```

- **except → returns the rows that are in column one but not in column two**

```SQL
select st_fname
from Student
except
select ins_name
from Instructor
```

## Ranking function Row_Number , Dense_rank, NTiles(group)

```SQL
select *,Row_number() 
over(order by id desc) as RN
from employee

-- partition by
select *,Row_number() 
over(partition by dep order by id desc) as RN
from employee

---------- to use where you need to use subquery
select *
from (select *,Row_number() over(order by st_age desc) as RN
       from student) as newtable
where RN=1

select *
from (select *,dense_Rank() over(order by st_age desc) as DR
	  from student) as newtable
where DR=1

select *
from (select *,ntile(3) over(order by st_age desc) as G
      from student) as newtable
where G=1


select *
from (select *,Row_number() over(partition by dept_id order by st_age desc) as RN
       from student) as newtable
where RN=1

select *
from (select *,dense_Rank() over(partition by dept_id order by st_age desc) as DR
	  from student) as newtable
where DR=1

select *
from (select *,ntile(2) over(partition by dept_id order by st_id desc) as G
      from student) as newtable
where g=1 and dept_id=10 
```

  

### windowing functions

- **1. lead & lag**
    
    ```SQL
    select id,fname,
    lag(fname) over(order by id) as prev,
    lead(fname) over(order by id) as next
    from employee
    ```
    
    ![[Untitled 6.png]]
    
    - where and partition by
    
    ```SQL
    --to use where you should use subquery
    select * from(
    select id,fname,
    lag(fname) over(order by id) as prev,
    lead(fname) over(order by id) as next
    from employee) as neww
    where id = 3
    
    --partition by
    select id,fname,dep,
    lag(fname) over(partition by dep order by id) as prev,
    lead(fname) over(partition by dep order by id) as next
    from employee
    ```
    
    ![[Untitled 7.png]]
    
- **First Value & Last Value**
    
    ```SQL
    select *,
    FIRST_VALUE(fname) over(order by id) as first,
    last_value(fname) over(order by id) as last
    from employee
    ```
    
    ![[Untitled 8.png]]
    
    partition by
    
    ```SQL
    select *,
    FIRST_VALUE(fname) over(partition by dep order by id) as first,
    last_value(fname) over(partition by dep order by id) as last
    from employee
    ```
    
    - if last_vlaue doesn’t work
        
        ```SQL
        SELECT *,
            FIRST_VALUE(fname) OVER (ORDER BY id) AS first,
            LAST_VALUE(fname) OVER (ORDER BY id ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last
        FROM employee;
        ```
        
        > error cause
        > 
        > The issue arises because the `LAST_VALUE` function, by default, looks at the current row and all preceding rows within the window frame. To get the desired result with `LAST_VALUE`, you need to specify the correct window frame that includes all rows up to the end of the partition.
        > 
        > To achieve this, you should use `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` to ensure that the window frame includes all rows from the beginning to the end of the result set.
        

## DCL – Data Control Language

## TCL - Transactional Control Language

soon :)

## built-in functions → DQL

```SQL
date functions
--date   getdate eomonth month   day   year  datediff isdate eomonth

select isdate('dsfsdfsdf')
select isdate('1/1/2000')

SELECT DATEDIFF(end_date, start_date) AS day_difference;


-- String Functions
SELECT CONCAT('W3Schools', '.com'); --> adds two or more strings together

SELECT FORMAT(123456789, '#\#-##-#####') --> 12-34-56789

select upper(st_fname),lower(st_lname) from Student

select len(st_fname),st_fname
from Student

select substring(st_fname,1,3)
from Student   --> returns the first 3 chars

select substring(st_fname,3,3)
from Student   --> returns the chars form 3 to 6

select substring(st_fname,1,len(st_fname)-1)
from Student   --> returns the whole word except the last char

-- NULL Functions
SELECT ISNULL(NULL, 'spare');  --> if the value is null returns 'spare'
SELECT COALESCE(NULL, 1, 2) --> returns first non-null value -> 1

-- conversion Function
SELECT CONVERT(int, 25.65); --> convert's the valur to int type
select CAST(50.5 as int) --> same

-- Math function
select POWER(2,3)
select sin(0)
select log(5,2)

--System Functions
select db_name()  --> returns database name
select suser_name()
select Newid() --> creates random id
```

### `newid`

```SQL
select * , newid() as Xid
from Student
order by Xid
--
select top(1)*
from Student
order by newid() --> selects a random raw
```

`**identity**`

```SQL
alter table employee 
add identintyy int identity(10,10) --> 10,20,30,....
-- adds a column starts by 10 increases by 10
```

- identity insert
    
    ```SQL
    -- Create a sample table with an identity column
    CREATE TABLE Students (
        StudentID INT IDENTITY(1,1) PRIMARY KEY,
        Name NVARCHAR(50)
    );
    
    -- Insert a row without specifying the identity column (default behavior)
    INSERT INTO Students (Name) VALUES ('John Doe');
    
    -- Turn on IDENTITY_INSERT for the Students table
    SET IDENTITY_INSERT Students ON;
    
    -- Insert a row with an explicit value for the identity column
    INSERT INTO Students (StudentID, Name) VALUES (100, 'Jane Smith');
    
    -- Turn off IDENTITY_INSERT for the Students table
    SET IDENTITY_INSERT Students OFF; --now we can't insert identity manually
    
    -- Verify the inserted rows
    SELECT * FROM Students;
    ```
    

---

## database integrity (constraints & rules)

![[Untitled 9.png]]

- `[not null](https://www.w3schools.com/sql/sql_notnull.asp)`
- `[unique](https://www.w3schools.com/sql/sql_unique.asp)`
- `[PRIMARY KEY](https://www.w3schools.com/sql/sql_primarykey.asp)` - A combination of a `NOT NULL` and `UNIQUE`. Uniquely identifies each row in a table
- `[FOREIGN KEY](https://www.w3schools.com/sql/sql_foreignkey.asp)` - Prevents actions that would destroy links between tables
- `[default](https://www.w3schools.com/sql/sql_default.asp)` `= ‘ ’`
- `persisted`
- `[check](https://www.w3schools.com/sql/sql_check.asp)`

![[Untitled 10.png]]

### constraint

```SQL
create table emps
(
 eid int ,
 ename varchar(10),
 eadd varchar(10) default 'cairo',
 hiredate date default getdate(),
 salary int,
 overtime int,
 netsal as(isnull(salary,0)+isnull(overtime,0)) persisted,  --computed+saved
 bd date,
 age as year(getdate())-year(bd), -->computed
 hour_rate int not null,
 gender varchar(1),
 dnum int,
 constraint c1 primary key(eid,ename),-->composite PK
 constraint c2 unique(overtime),
 constraint c3 unique(Salary),
 constraint c4 check(salary>1000),
 constraint c5 check(overtime between 100 and 500),
 constraint c6 check(gender='f' or gender='m'),
 constraint c7 check(eadd in('alex','mansoura','cairo')),
 --make a relation with constraint
 constraint c8 foreign key(dnum) references depts(did)
	on delete set null  on update cascade
 )
```

remove or add constraint to an exsisting tablr

```SQL
 alter table emps drop constraint c3

 alter table emps add constraint c100 check(hour_rate>1000)

 alter table instructor add constraint c20  check(salary>1000)
```

### rule

> note : the Column should have on rule but may have many constrints

```SQL
  --Rule   --->global check constraint
  
  create rule r1 as @x>1000
  -- apply the rule to the table
  sp_bindrule r1,'instructor.salary' 
  
  -- remove the rule from the column
  sp_unbindrule 'instructor.salary'
  
  --delete the rule itself
  drop rule r1
```

  

> Constraints in SQL enforce data integrity for both old and new data, while rules are an older, less common method specific to certain database systems.

### Default

```SQL
create default def1 as 5000;
sp_bindefault def1,'emp.sal';

sp_unbindefault 'emp.sal';
drop default def1;
```

## security (logins , users)

authentication → login name + password

- windows authentication —> windows admin == sql server admin
- sql server authentication
    - create new logins → new password → new users
    - -------->SA built in admin

  
authorization (permission)  

- SQL server Schema
- logical group of objects
    
    - dbo → database owner ( default schema )
    - to select object the right syntax is
    
    ```SQL
    (schemaName).objectName
    -- ex.
    select * from dbo.Student --dbo is the default schema
    ```
    

### 10 steps of security

- 1. change authentication mode (to allow multible users)
    
    1. select server→ right click → properties → SQL Server and Windows Authentication mode
    
    ![[Untitled 11.png]]
    

1. restart server : services → sql server(MSSQLSERVER) → righ click - restart

- 3. create login
    
    database → security → logins (right click) → new login
    
    → general —→ choose : sql server authentication
    
    insert (login name , password ), remove check ( Enforce password policy)
    
- 4. create user
    
    select database → security → users → r.c new user → username, login name
    
- 5. create schema
    
    ```SQL
    create schema HR
    create schema Sales
    ```
    
- 6. assign objects to schema
    
    ```SQL
    alter schema hr transfer student
    alter schema sales transfer department
    ```
    
- 7. join [schema+user]
    
    database → security → users → chooese the user → owned schemas
    
- 8. set permissions
    
    select database → properties → permissions →
    
- 9. disconnect ==>connect user
    
    chooese sql server authentication → username , password
    
    → check ( trust server certificate )
    
- 10. test the permission with new query
    
    ```SQL
    --permissions
    --(student+instructor)
    -----grant   select insert
    -----deny    update delete
    ```
    

  

## schema and fullpath object

create

```SQL
create schema HR
create schema Sales
```

assign tables to schema

```SQL
alter schema hr transfer student
alter schema sales transfer department
```

return to the default schema

```SQL
alter schema dbo transfer sales.department
alter schema dbo transfer hr.instructor
```

### fullpath object

```SQL
-- [Servename].[dbName].[schemaName].[objectName]

select * from "Rami".[ITI].dbo.student

-- so we can get data from two databases
select dept_name from Department
union all
select dname from Company_SD.dbo.Departments



```

## type of tables

1. physical table → stored in database

```SQL
create table currencies (id int, currency varchar(10), value int)
```

1. variable table
    - only accessible within the batch, stored procedure, or function in which it is declared.

```SQL
declare @t table (x int)
```

1. local table [session based tables]
    - Local temporary tables are tables that are only visible within the session (query) that created them. They are automatically dropped when the session ends

```SQL
-- this table appera only on the opend query
create table \#exam (id int, edate date)
```

1. global tables [shared tables]
    - accessible to all sessions and users , The table is automatically dropped when the session that created it ends

```SQL
-- you can access this table in any query in the current session
create table #\#exam (id int, edate date)
```

> local table & global tables are stored in databases → tempdb → temporary table

![[Untitled 12.png]]

### Backup

![[Capture.jpg]]

- **Full Backup**:
    
    A full backup contains all the data in a specific database at the time the backup is completed. It also includes parts of the transaction log so that the full backup can be recovered.
    
- **Differential Backup**:
    
    A differential backup contains only the data that has changed since the last full backup. This means it captures the differences from the last full backup, making it smaller and quicker to create than a full backup.
    
- **Transaction Log Backup**:
    
    A transaction log backup captures all the transaction log records that have been generated since the last log backup. This allows for point-in-time recovery of the database. Transaction log backups are essential for databases in the full or bulk-logged recovery model.
    

- data types
    - numeric
        - bit → 0:1 false:true boolean
        - tinyint → 1byte -128:127
        - smallint → 2 byte -32768:32767
        - int → 4 byte
        - bigint → 8 b
    - decimal
        - smallmoney → 4B .0000 $
        - money → 4B .0000
        - real → 0.0000000 7
        - float
        - dec - decimal → dec(5,2) 5 digits 2 of them are decimal → ex 123.33
    - string & char
        - char(10) → fixed length string → ex. ahmed :10 , ali: 10
        - varchar(10) → variable length string → ex. ahmed:5 ali:3
        - nchar(10) → Unicode language
        - nvarchar(10) → unicode — up ro 2 GB
    - date time
        
        - date → MM/dd/yyyy
        - time → hh:mm
        - smalldatetime
        - datetime
        
        ![[Untitled 13.png]]
        
    - binary
        - binary
        - image
    - other
        - xml
        - sql_variant
        - geography
- excution order
    1. from
    2. join
    3. on
    4. where
    5. groub by
    6. having
    7. select
    8. order by
    9. top
- server hierarchy
    - **server**
        - **DB**, logins
            - Users, **Schema**
                - **objects** (table, rule, function, stored view)
                    - columns, Keys, constraints, index, trigger

---

## variables

- types of variables
    1. local variable
        1. scope : batch, function, stored procedures
    2. global variable

### local variable @

### normal vaiable

- `**declare**`

```SQL
declare @x int
set @x = 100
select @x 
---

-- assigning the value in the decalre step
declare @x int = 12
select @x

-- assign the result of select statment to var
declare @x int = (select avg(salary) from employee)
select @x
	
```

- `assign`

```SQL
--asign value to var
set @x = 100
select @x 100 -- select here is working like set

--asign query to var
declare @x int = (select st_age from student where st_id = 15)

--asign using update
update students set name = 'ali' , @x = age --both update name  and assign to the var 
where id = 2

--show the var
select @x
```

> note:
> 
> - if the select didn’t return any value the variable keep it’s value → ex1
> - if i select a column or multiple values the var holds last value int that column →ex2
> 
> ```SQL
> -- ex1.
> declare @y int=100
> select @y = age from Student where id=900 -- there's no id 900
> select @y --> returns 100 because the select returns null
> 
> -- ex2.
> declare @y
> select @y = age from Student -- the last age in the column is 25
> select @y --> returns 25
> ```

### one and multidimensional array→ table var

```SQL
declare @t table(id int, salary int)

-- insert
declare @t table(id int, sa int)
insert into @t 
values (1,5000),
	   (2,10000)

--insert from existing table
insert into @t
select id,salary from employee

--show the table
select * from @t
```

  

### global variable @@

```SQL
select @@SERVERNAME
select @@SERVICENAME
select @@VERSION
select @@IDENTITY --> returns the last identity generated number
select @@ROWCOUNT -->returns the number of rows affected due to your last operation
select @@ERROR

select USER

---
select * from employe
go
select @@ERROR --> returns the number of the error
```

### control of flow statements if else & try catch & while& choose

- if else
    
    ```SQL
    declare @f int = 10
    
    if @f < 6
    	select 'hi'
    else
    	select 'bye'
    
    --using begin & end --> when writing multiple statment 
    if @f < 6
    begin
    	select 'hi'
    	select * from employee
    end
    else
    	select 'bye'
    
    ```
    
- if exists () - not exists
    
    - exists
    
    ```SQL
    -- avoid table duplication error
    if exists(select name from sys.tables where name = 'currencies')
    	select 'table is existed choose new name'
    else 
    	create table currencies (id int, currency varchar(10), value int)
    ```
    
    - not exists
    
    ```SQL
    -- delete the department of there is no employee assigned to it
    if not exists (select dep from employee where dep = 2)
    	delete from departemnts where depid = 2
    ```
    
- try & catch
    
    ```SQL
    begin try
    	delete from employee where id = 5
    end try
    begin catch
    	select 'erorr'
    end catch
    ```
    
- while
    
    ```SQL
    declare @n int = 1
    while @n <= 10
    begin
    	select @n 
    	set @n += 1
    end
    ```
    
    - break - continue
    
    ```SQL
    declare @n int = 0
    while @n <= 10
    begin
    	set @n += 1
    	if @n = 5
    		CONTINUE --> skips number 5
    	if @n = 9
    		break --> stops at number 9
    	select @n 
    end
    ```
    
- choose
    
    ```SQL
    CHOOSE ( index, val_1, val_2,... )  
    
    -- returns the third item from the list
    select choose(3,'a','b','c','d') --> c
    ```
    

  

## execute & dynamic query

```SQL
execute('select * from student') --> converting the string to query and runs it


declare @col varchar(20) = '*',  @tab varchar(20) = 'employee'
execute('select ' + @col + ' from ' + @tab)
select * from employee
```

### synonyms

```SQL
-- synonyms are just an abbreviation
create synonym emp
for employee

select * from emp
```

- to show all synonyms

```SQL
select name,base_object_name from sys.synonyms
-- returns synonym name and the table name
```

![[Untitled 14.png]]

### user defined Functions

- scalar Functions → returns one value
    - create & call & alter & drop
        
        ```SQL
        create Function GetName(@id int)
        returns varchar(30)
        begin
        	declare @name varchar(30)
        	set @name = (select st_fname from student where st_id = @id)
        	return @name
        end
        ```
        
        - Alter
        
        ```SQL
        Alter Function GetName(@id int)
        returns varchar(30)
        begin
        	declare @name varchar(30)
        	set @name = (select st_fname from student where st_id = @id + 1)
        	return @name
        end
        ```
        
        - drop
        
        ```SQL
        drop Function GetName
        ```
        
        - call function
        
        ```SQL
        -- i have to select the schema "dbo"
        select dbo.GetName(1)
        ```
        
    - stored at
        
        ![[Untitled 15.png]]
        
- Inline Function → the body contains only select statement
    
    - create
    
    ```SQL
    Create Function getStudents_DID(@did int)
    returns table
    as
    return
    	(
    	-- the body of the function 
    	select st_fname,dept_id
    	from student
    	where Dept_Id = @did
    	)
    ```
    
    - call
    
    ```SQL
    	-- i'm using select from because i returns table
    	select * from getStudents_DID(20)
    ```
    
    - alter & drop like scalar Functions
    - we can use the function as a normal table so i can even create new table with it
    
    ```SQL
    	select * into new_table from getStudents_DID(20)
    ```
    
      
    
    > note: if you add any driven column you should add a name to the new column  
    > ex. → select st_fname + st_Lname as full_name  
    > without “as full_name” it will give an error  
    
- Multiapartment Table Valued Function → contains: select + ( IF, while,….)
    
    - create
    
    ```SQL
    	create function getS(@f varchar(50))
    	returns @t table(id int, sname varchar(50))
    	as
    		begin
    		--function body
    			if @f = 'first'
    				insert into @t
    				select st_id,st_fname from student
    			else if @f = 'last'
    				insert into @t
    				select st_id,st_lname from student
    			else if @f = 'full'
    				insert into @t
    				select st_id,st_fname +' '+ st_lname as fullname 
    				from student
    
    			return
    		end
    		
    ```
    
    - call
    
    ```SQL
    select * from getS('full')
    ```
    
    > note: you can only inert and update and delete into variable but not into physical table
    

---

### stored procedure

- built-in stored procedures
    
    ```SQL
    EXEC sp_help 'student'
    --Provides information about a database object, such as tables, views, or indexes.
    
    EXEC sp_who;
    --Displays information about current SQL Server processes.
    
    EXEC sp_rename 'OldTableName', 'NewTableName';
    --Renames any database object.
    
    EXEC sp_adduser 'NewUser', 'NewUserLogin';
    --Adds a new user to the current database.
    
    EXEC sp_addrole 'NewRole';
    --Creates a new database role.
    
    EXEC sp_password @oldpassword = 'OldPass', @newpassword = 'NewPass', @loginame = 'UserName';
    --Changes a user’s password.
    
    EXEC sp_helptext 'd1'
    --Displays the text of a user-defined object, such as a stored procedure or function.
    ```
    

> [!important] to see all procedures [ select * from sys.procedures ]
> 
> - stored in
>     
>     ![[Untitled 16.png]]
>     
>       
>     

- create & call & alter & drop
    
    ```SQL
    create procedure GetStById @id int
    as
    	select * from student
    	where st_id = @id
    	
    -- another ex -> we can use proc instead of procedure 
    create proc insert_in @name varchar(30), @id int
    as
    	insert into new_table values(@name,@id)
    
    
    insert_in 'ahmed', 50
    ```
    
    - call
    
    ```SQL
    GetStById 2
    
    -- call bt postion
    insert_in 'ahmed', 50 
    --call by name
    insert_in @name='mona', @id=120
    
    --execute 
    execute insert_in 'mfm' , null
    ```
    
    - alter
    
    ```SQL
    alter procedure GetStById @id int
    as
    	select * from student
    	where st_id = @id
    ```
    
    - drop
    
    ```SQL
    drop procedure GetStById
    ```
    
    - default value
    
    ```SQL
    alter proc insert_in @name varchar(30)='def', @id int = 50
    as
    	insert into new_table values(@name,@id)
    
    insert_in       --> adds a row ('def', 50)
    insert_in 'ali' --> adds a row ('ali', 50)
    ```
    
      
    

- return
    
    > **return**  
    > The  
    > `RETURN` statement in a stored procedure always returns an integer and can only be used once. Its main use is to indicate the execution status, serving as a communication code between the programmer and the database administrator.
    
    ```SQL
    create proc plus  @x1 int, @x2 int
    as 
    	return @x1 + @x2
    
    declare @s int 
    execute @s = plus 5 ,6
    select @s --> returns 11
    ```
    

- output parameter
    
    ```SQL
    create proc p1 @id int,@age int output
    as
    begin
    	select @age= St_Age
    	from student
    	where St_Id = @id
    end
    
    declare @a int
    execute p1 5,@a output 
    --↑ give me the age of the student with id = 5 then but the output in var @a ↑--
    select @a 
    --note: you can make multiple output vars
    ```
    
    - input output parameter
    
    ![[Untitled.jpeg]]
    
- dynamic sp
    
    ```SQL
    create proc d1 @col varchar(50),@t varchar(50)
    as
    	execute('select '+ @col+ ' from '+ @t)
    
    d1 'st_id', 'student'
    ```
    

### Trigger

> [!important] Trigger: A database object that automatically runs when a specified database event occurs, such as an INSERT, UPDATE, or DELETE operation on a table
> 
> > [!important] to see all procedures [ select * from sys.triggers ]
> > 
> > - stored in
> >     
> >     ![[Untitled 17.png]]
> >     

- create & drop
    
    - instead of → prevent event and execute action instead of it
    
    ```SQL
    create trigger t1
    on new_table 
    instead of update
    as
    	select 'not allowed for user' + SUSER_NAME() + N'اندهلي حد كبير يا حبيبي'
    -- this trigger will work every time you try to update the table and show this message
    ```
    
    ![[Untitled 18.png]]
    
    - drop
    
    ```SQL
    drop trigger t1
    ```
    
- after → execute event then execute the action 
    
    ```SQL
    create trigger t5
    on new_table
    after insert
    as
    	select 'welcome to the club'
    	
    insert into new_table values('mmm',50)
    ```
    
    - In SQL Server, FOR and AFTER are identical in behavior.
    
    ```SQL
    create trigger t5
    on new_table
    for insert
    as
    	select 'welcome to the club'
    	
    insert into new_table values('mmm',50)
    ```
    
- inserted
    
    > The _inserted_ table stores copies of the new or changed rows after an INSERT or UPDATE statement
    
    ```SQL
    create trigger t6
    on new_table
    instead of insert
    as
    	select 'INSERT',* from inserted
    -
    insert into new_table values ('a',1)
    ```
    
    ![[6542f880-052c-4ab0-96dc-28a5091426df.png]]
    
- deleted
    
    > The _deleted_ table stores copies of the affected rows in the trigger table before they were changed by a DELETE or UPDATE statement
    
    ```SQL
    create trigger t7
    on new_table
    after update
    as
    	select 'inserted', i.*,'deleted',i.*
    	from inserted i, deleted d
    -
    update new_table set st_fname = 'ahmed'
    where dept_id = 20
    ```
    
    ![[Untitled 19.png]]
    
      
    
- enable and disable
    
    ```SQL
    alter table new_table disable trigger t5
    alter table new_table enable trigger t5
    ```
    
- runtime trigger `output` 
    
    ```SQL
    update new_table 
    set st_fname = 'ali' 
    output inserted.*,deleted.* 
    where st_fname = 'mfm'
    
    --
    --this wil show the data that were inserted, date and username
    insert into new_table
    output SUSER_NAME() as 'user',GETDATE() as 'date',inserted.*  
    values('noha',555)
    ```
    
- example
    
    ```SQL
    --trigger to prevent the user from updating the department to be 1000
    create trigger tdep
    on new_table
    instead of update
    as
    	if UPDATE(dept_id)
    		if (select dept_id from inserted) = 1000
    		select 'you cant insert any one in department num 1000'
    
    update new_table set dept_id = 1000 where st_fname = 'hassan'
    ```
    
- display the operation executed (insertupdate,delete)
    
    ```SQL
    create trigger tablechanges
    on new_table
    after insert,update,delete
    as
    begin
    	if exists(select * from inserted) AND NOT exists(select * from deleted)
    		select 'inserted'
    	else if exists(select * from deleted) AND NOT exists(select * from inserted)
    		select 'deleted'
    	else if exists(select * from deleted) AND exists(select * from inserted)
    		select 'updated'
    end
    ```