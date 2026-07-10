SQL stands for Structured Query Language. It is a programming language used for managing and manipulating databases divided into three categories.

  

- **Database schema**
    - A schema is a group of related objects in a database
    - There’s one owner of a schema who has access to manipulate the structure of any object in the schema
    - schema doesn’t represent a person

- **Data types** A data type determines the type of data that can be stored in a database column e.g. (String, numeric, date & time)

- **Database constraints:** Restrictions on database table or object to help **maintain integrity of data**
    - **Primary key Constraint**
        - Not Null
        - Unique
    - **Not Null constraint**
        
        this enforces a field to always contain a value, means that you can’t insert or update a record without adding value to this column e.g. ID.
        
    - **Unique Key constraint**
        
        the UNIQUE constraint ensures that all values in a column are different and need to be identified e.g. insurance number.
        
    - **Referential integrity constraints (FK)** !!
        
        - when we take a primary key to another table as foreign it called (Child record).
        - this primary key in his original table it called (Parent Record).
        
        - **Insert**
            
            Insert in the Parent record first then the child record.
            
        - **Delete**
            
            Delete from child record first then the parent record.
            
        
        - E.g. my column is dep Number what if i want to add new department I will go first for parent record and If I want to eliminate a department I will go for the child record then parent
    - **Check Constraints**
        - Customize a column e.g. (Salary) for employee is between 1000 - 20000.
        - Only accept the values with this range.
        - avoiding the typo error

  

- **DDL:** Data definition language
    
    - Group of commands responsible for the structure of the database objects like
        - Create structure
        - Edit the structure
        - Delete the structure
    
    - **Create** 
        
        ```SQL
        Create table table_name (column_name1 column data type (if there’s constraints), column_name2 column data type Not null, …)
        ```
        
    - **Alter**
        
        ```SQL
        Alter table table_name add new_column_name column data type
        ```
        
        ```SQL
        Alter table table_name drop column_name
        ```
        
    - **Drop**
        
        ```SQL
        drop table table_name
        ```
        
    - **Truncate**
        
        - Truncate doesn’t have where clause
        - no roll back for DDL due to the auto commit
        
        ```SQL
        -- regarding the previous two sentance if you the oppsite use delete command in DML
        TRUNCATE FROM mytable
        ```
        
          
        
    
    Hint: you can’t manipulate the data using DDL
    
- **DML:** Data manipulation language
    - **INSERT**
        
        ```SQL
        INSERT INTO table_name (id, fname, lname, age, sex) VALUES (50, ‘Ahmed’, ‘Ziada’, 23, ‘m’)
        ```
        
        ```SQL
        --If I know my table columns names and the column arranges we can procced with values
        INSERT INTO table_name VALUES (50, ‘Ahmed’, ‘Ziada’, 23, ‘m’)
        ```
        
        ```SQL
        --If I Want to add new record and fill specific columns in the table 
        INSERT INTO table_name (id, fname,age) VALUES (50, ‘Ahmed’, 23)
        ```
        
    - **UPDATE**
        
        ```SQL
        -- without the where clause the whole salary column will be one value and it's 1200 
        UPDATE mytable
        SET salary = 1200
        WHERE SSN = 102674;
        ```
        
        ```SQL
        -- update more than col 
        UPDATE mytable
        SET salary = 1200, dno = 10
        WHERE SSN = 102674;
        ```
        
    - **DELETE**
        
        - Delete command is working on record level (ROW level)
        
        ```SQL
        --  
        DELETE FROM mytable
        WHERE ssn = 10267
        ```
        
    - **SELECT**
        
        ```SQL
        SELECT dname, Dnum, [resign date], mgssn
        FROM mytable
        WHERE mgssn = 50856
        ```
        
- **DCL:** Data control language **(Object not system)**
    
    using to give access privilege to any user for specific objects or remove it.
    
    - **Grant command** 
        
        ```SQL
        GRANT SELECT ON TABLE table_name to user_name;
        ```
        
        ```SQL
        GRANT ALL ON TABLE table_name to user_name1,user_name2;
        ```
        
        ```SQL
        GRANT SELECT ON TABLE table_name to user_name WITH GRANT OPTION;
        ```
        
        **HINT: Grant all mean all the DMLs functions (SELECT, INSERT, UPDATE, DELETE)**
        
        **GRANT OPTION:** he can give the same privilege he has with other users.
        
    - **Revoke command**
        
        ```SQL
        	REVOKE UPDATE ON TABLE table_name from user_name;
        ```
        
        ```SQL
        	REVOKE All ON TABLE table_name from user_name1, user_name2;
        ```
        
- **Comparison & Logical operators**
    
    - Multi & Single rows operators
        - Multi Row Operator
            
            - `**IN**`
                
                `**IN**` operator is used to compare a single value with a list of values or a subquery result. It returns true if the value matches any value in the list or subquery result.
                
                ```SQL
                SELECT employee_name
                FROM employees
                WHERE department_id IN (1, 2, 3);
                ```
                
            - `**ALL**`
                
                `**ALL**` operator is used to compare a single value with a set of values returned by a subquery. It returns true if the comparison is true for all the values in the set.
                
                ```SQL
                SELECT product_name
                FROM products
                WHERE price > ALL (SELECT price FROM products WHERE category_id = 1);
                ```
                
            - `**ANY**`
                
                `**ANY**` operator is used to compare a single value with a set of values returned by a subquery. It returns true if the comparison is true for at least one of the values in the set.
                
                ```SQL
                SELECT product_name
                FROM products
                WHERE price > ANY (SELECT price FROM products WHERE category_id = 1);
                ```
                
            
            - **Aggregate functions**: SUM, AVG, COUNT, MAX, MIN
            - **Window functions:** ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD
            - **Common Table Expressions (CTE)** with recursive queries
        - Single Row Operator
            
            - **Arithmetic operators:** +, -, *, /
            - **Comparison operators:** =, <, >, <=, >=, !=
            - **String functions:** CONCAT, LENGTH, SUBSTR
            - **Date functions:** DATEADD, DATEDIFF, DATEPART
            - **Conditional functions:** CASE WHEN, IFNULL (or COALESCE in some databases)
            
              
            
    - AND & Between operators
        
        ```SQL
        -- AND / BETWEEN logical operators
        SELECT fname
        FROM mytable
        WHERE salary >= 1500
        AND salary <= 2500
        
        -- WHERE salary between 1500 and 2500
        ```
        
    - OR & IN operators
        
        ```SQL
        -- OR(Single-row operator) / IN(multi-row operator) logical operators
        SELECT fname, ssn
        from employee 
        WHERE MGSSN = 15618
        OR MGSSN = 48615
        
        -- WHERE MGSSS IN (15618, 48615)
        ```
        
    - LIKE operator
        
        ```SQL
        SELECT * 
        FROM employee
        WHERE fname like 'Ahm?d'
        
        -- to get all who names ahmed whether this spell or Ahmad spell.
        ```
        
        ```SQL
        SELECT * 
        FROM employee
        WHERE fname like '?o*'
        
        -- WHERE fname like '?o%'
        -- * and % are doing the same functionallity.
        ```
        
    - Alias 
        
        ```SQL
        SELECT fname, salary *0.1 as Bouns
        FROM employee
        ```
        
        ```SQL
        SELECT fname+''+lname as [full Name)
        FROM Employee 
        WHERE salary*12 > 10000
        ```
        
          
        
    - Order By
        
        ```SQL
        SELECT *
        from employee
        order by dno asc, salary desc
        ```
        
    - DISTINCT
        
        ```SQL
        SELECT DISTINCT Dno
        FROM Employee
        ```
        
    - Inner Join
        
        **TIP:** When you join two tables, and both have Partitioning Schemes, be sure to include conditions in your WHERE clause to ensure you're making use of the partitions in both tables.
        
        ```SQL
        SELECT fname, dname
        from emplyee, departments 
        WHERE MGRSSN = SSN
        ```
        
        ```SQL
        SELECT fname, dname
        FROM employee as e, department as d
        WHERE e.dno = d.dno
        ```
        
        ```SQL
        SELECT fname, dname
        FROM employee as e Inner join 
        department as d
        ON e.dno = d.dno
        ```
        
        ```SQL
        SELECT FNAME, pname, hours
        FROM Employee,Project,worksfor
        WHERE SSN = essn
        and pno = pnumber
        ```
        
    - Outer, Full Join
        
        ```SQL
        Select fname,dname
        From Employee as e left outer join department as d
        ON e.dno = d.dno
        ```
        
        ```SQL
        Select fname,dname
        From Employee as e Right outer join department as d
        ON e.dno = d.dno
        ```
        
        ```SQL
        Select fname,dname
        From Employee as e Full outer join department as d
        ON e.dno = d.dno
        ```
        
    - SELF Join
        
        to make self join you must have recursive relationship
        
        ```SQL
        SELECT e.fname, s.fname as Manger
        FROM Employee as e , Emplyee as s
        WHERE e.superSSN = ssn
        ```
        
    - Sub-Queries
        
        Subqueries represent another way to pull data from two or more tables and can be an effective tool to avoid errors in JOINs. What you'll see is that subqueries are really great when you need to return rows from one table based on the existence of one or more conditions in another table. That's because subqueries produce a list of values used as inputs to the main query.
        
          
        Subqueries can be included either into a JOIN statement, or in the WHERE clause to limit the results of the main query. On the following lesson, you will learn more about these two ways. of creating subqueries.  
        
        ```SQL
        SELECT *
        FROM employee
        WHERE salary > (Select salary from employee
        WHERE fname = 'Ahmed' and lname = 'Ali')
        ```
        
        ```SQL
        -- Return employee that has salaries higher than any employee in dno 10. (All the employees))
        SELECT *
        FROM employee
        WHERE salary > ALL (Select salary from employee
        WHERE dno = 10)
        ```
        
        ```SQL
        -- Return employee that has salaries higher than anyone in dno 10 not. (just one person)
        SELECT *
        FROM employee
        WHERE salary > ANY (Select salary from employee
        WHERE dno = 10)
        ```
        
    - Aggregate functions
        
        - Aggregate functions Ignore Nulls.
        - Aggregate functions: SUM, AVG, COUNT, MAX, MIN.
        
        ```SQL
        Select max(salary) as Max, Min(salary) as Min
        from employee
        ```
        
        ```SQL
        SELECT COUNT(ssn) as emp, count(salary)
        from employee
        ```
        
          
        
    - Group By / Having
        
        Having: take conditions based on aggregate
        
        ```SQL
        SELECT AVG(salary)
        FROM employee
        GROUP BY dno
        HAVING max(salary) > 1800
        ```
        
    - Null & NotNULL
        
        ```SQL
        -- NULL / NOT NULL
        SELECT fname
        FROM mytable
        WHERE salary BETWEEN 1500 and 2500
        AND salary is NOT NULL
        -- to exlcude all the empty salary values
        -- entries you can use just NULL to extract the null without NOT.
        ```
        
        ```SQL
        -- NVL
        SELECT fname 
        , NVL(salary, 0)
        FROM mytable
        WHERE salary BETWEEN 1500 and 2500
        
        -- Replace all the NULL value in salary column with 0 Value.
        -- You can use it on string columns also.
        ```
        
    
    ```SQL
    SELECT dname, max(salary) as max
    FROM employee as e Inner join departments as d
    ON e.dno = d.dno
    
    -- OR we can write the join in this way 
    -- From employee as e , departments as d
    --WHERE e.dno = d.dno 
    GROUP BY ddname
    HAVING avg(salary) > 1200
    ORDER BY dname
    ```
    
- **Other DB Objects**
    - **Views**
        
        **Logical table:** visual table doesn’t have it’s own data, it’s a window leads to the date from it’s source
        
        View is Logical table based on a table (Based tables) or another view.
        
        ```SQL
        CREATE VIEW VW_Work_hrs -- you can alies your column hear unless the original name will appear
        AS
        SELECT fname, lname, pname, hours
        FROM employee, project, works_on
        WHERE ssn = ssn and pno = pnumber
        ```
        
          
        
        **With check Option:** is option that he will check the constraints that the condition is valid to add new record.
        
        ```SQL
        CREATE VIEW VW_Work_hrs 
        AS
        SELECT *
        FROM suppliers
        WHERE statues > 15
        with check option;
        
        -- I can't add new supllier to the original table using this view with statues less than 15
        ```
        
        ```SQL
        -- Quering form the view i've create it
        SELECT fname, lname, hours
        FROM VW_Work_hrs
        
        --SELECT * FROM VW_Work_hrs
        ```
        
        ```SQL
        --Edit the view whether drop or add new
        CREATE OR REPLACE VIEW VW_Work_hrs 
        AS
        SELECT fname, lname, pname, hours
        FROM employee, project, works_on
        WHERE ssn = ssn and pno = pnumber and dno = 5
        ```
        
        ```SQL
        -- Delete View 
        
        Drop View View_name
        ```
        
          
        
    - **Indexes**
        
        - Indexes needed when I have two problems
            1. Data not sorted
            2. Data is scattered (not in row in the physical memory)
        - They are used to speed the retrieval of record in response in certain conditions.
        - May be defined on one or multiple columns in the same table
        
        - Create an index when
            - Retrieving data heavily from table
            - Columns are used in search conditions, join conditions, and filter conditions
            - column contain large number of nulls (Avoiding full table scan)
        - Do not create index when
            
            Table is updated frequently (Using DML a lot)
            
        
        ```SQL
        -- How to create an index
        
        Create index index_name ON table_name(column_name);
        
        -- Create index emp_inx ON employee (Salary);
        ```
        
        ```SQL
        -- How to remove an index
        
        Drop index index_name
        ```
        
    - **DCODE()**
        
        The DECODE function translates values in a column to different values depending on a specified condition. Essentially, this function works as an IF-THEN-ELSE expression.
        
          
        
        Consequently, the DECODE is very similar to the IF function in Excel, which works by performing a logical test and returning
        
          
        
        To use the ==**DECODE function()**==, you should include the column name followed by the logical test within parentheses, like this:
        
          
        DECODE (column,  
        ==A==,==X==, ==B==,==Y==,==C==,==Z==, default) - which functions as:  
        IF the column value is  
        ==A==, THEN return ==X== IF the column value is ==B==, THEN return ==Y== IF the column value is ==C==, THEN return ==Z== ELSE, return the default.  
        The first argument in the function is a column in one of the tables you're querying. Then, the value "  
        ==A==" is a defined value that could be found in the specified column. The value "==X==" is what you want the "==A==" value translated to in your results. If"==A==" was not found, then "==B==" is another value that could be found, and "==y==" is what you want returned if "==B==" is found. Successively, the same goes for "==C==" and "==Z==" and any other values you might include.
        
          
        This type of expression is useful for replacing abbreviations or codes that are stored in tables with meaningful business values that are needed for reports.  
        
          
        
        ```SQL
        -- convert from Numric to String
        SELECT
        	vendors.VENDOR_ID
        	, DECODE (vendors.PREFERRED_ORDER_ METHOD, 0, 'Unknown', 1, 'Phone', 2, 'Fax', 3, 'Ema11',4, 'EDI', 5, 'EDI and Email') as ORDERING _METHOD
        
        FROM 
        	BOOKER.VENDORS vendors
        
        WHERE 
        	vendors.VENDOR_ID IN(46745, 46972, 48033)
        ```
        
          
        
    - **CASE()**
        
        The ==CASE== function is similar to the ==DECODE()==, but with more advanced options. With ==CASE==, you can evaluate not just if a column record is equal to a value, but also if an expression is true, and return your results depending on the conditions set for the expression.
        
          
        To use the  
        ==CASE== function, you need to define an expression and compared it with a value. When a match is found, the value specified in the ==THEN== clause is returned. If no match is found, the value in the ==ELSE== clause is returned. Also, you can include several different expressions before ending the function.
        
        ```SQL
        SELECT
        		dma.ASIN
        		, CASE WHEN (coi.ORDER_DAY < dma. STREET_DAY) THEN
        		'Pre_Order'
        		ELSE 'Regular'
        		END as Lifecycle
        
        FROM
        		BOOKER.D_MP_ASINS as dma
        
        		JOIN BOOKER.D_CUSTOMER_ORDER_ITEMS coi
        				ON dma.ASIN = coi.ASIN
        				AND dma.MARKETPLACE_ ID = coi. MARKETPLACE_ ID
        		
        		JOIN BOOKER-D_MP_ASIN_MANUEACTURER manuf
        				ON dma.ASIN = manuf.ASIN
        				AND dma MARKETPLACE_ID = manuf.MARKETPLACE_ID
        
        WHERE
        		dma.MARKETPLACE_ ID = 1
        		AND dma.GL_PRODUCT_GROUP_DESC = 'gl_home'
        		AND dma.CATEGORY_CODE = '20103500'
        		AND coi.ORDER_DAY = TO_DATE ('2017.01.25', 'УУУУ.ММ.DD')
        		AND manuf.BRAND_CODE = 'POOPV'
        		
        GROUP BY
        		1,2
        ```
        
    - **TO_Char()**
        
        **Convert Date column to the format you need**
        
        **Changes the column data type the char or varchar (String).**
        
        ![[Untitled.png]]
        
    - **TO_Date()**
        
        Convert char or varchar (String) columns data type to date format
        
        Uses in Where clause
        
        ![[Untitled 1.png]]
        
        ![[Untitled 2.png]]
        
    - **DATE_TRUNC()**
        
        In a world of ever-expanding data streams, we rely on time stamps to organize data down to the second. But this level of detail can be distracting. Suppose you want to explore trends in glance views for a particular ASIN and need a time-series analysis, such as a week over week or year over year report.
        
          
        You'll need to aggregate data for each time a detail page hit occurred over a specified time range and then specify a date within your time range to report your aggregation. That's when the  
        **DATE_TRUNC()** function is needed. You can use it to truncate a time stamp to a particular day within the interval you need, while reporting on the aggregated data.
        
          
        For example, the DATE_TRUNCO function can return values for the first day of a specified year, the first day of a specified month, or the Monday of a specified week. To learn more, view the detailed example below.  
        
        ![[Untitled 3.png]]
        
          
        
        **there’s also:**
        
        - minute, minutes:
            
            ```SQL
            		SELECT DATE_TRUNC('minute', TIMESTAMP '20200430 04:05:06.789');
            ```
            
        - hour, hours:
            
            ```SQL
            SELECT DATE_TRUNC('hour', TIMESTAMP '20200430 04:05:06.789');
            ```
            
        - day, days:
            
            ```SQL
            SELECT DATE_TRUNC('day', TIMESTAMP '20200430 04:05:06.789');
            ```
            
        
          
        
          
        
        ![[Untitled 4.png]]
        
        ![[Untitled 5.png]]
        
          
        
        - Also there’s differnace between Orcale and Redshift:
            
            ![[Untitled 6.png]]


==In summary:==

- ==`LEFT JOIN` includes all records from the left table and matched records from the right table.==
- ==`RIGHT JOIN` includes all records from the right table and matched records from the left table.==