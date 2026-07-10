```SQL
SELECT St_Fname,Dept_Name
From Student , Department

SELECT St_Fname , Dept_Name
FROM Student CROSS JOIN Department

SELECT St_Fname , Dept_Name
FROM Student S , Department D
WHERE D.Dept_Id = S.Dept_Id

SELECT St_Fname , Dept_Name,D.Dept_Id
FROM Student S , Department D
WHERE D.Dept_Id = S.Dept_Id

SELECT St_Fname , D.*
FROM Student S , Department D
WHERE D.Dept_Id = S.Dept_Id

SELECT St_Fname , Dept_Name
FROM Student S , Department D
WHERE D.Dept_Id = S.Dept_Id and St_Address = 'alex'
ORDER BY Dept_Name
```

#### Joins
```SQL
SELECT St_Fname , Dept_Name
FROM Student S INNER JOIN Department D
ON D.Dept_Id = S.Dept_Id

SELECT St_Fname , Dept_Name
FROM Student S INNER JOIN Department D
ON D.Dept_Id = S.Dept_Id and St_Address='alex'

SELECT St_Fname , Dept_Name
FROM Student S LEFT OUTER JOIN Department D
ON D.Dept_Id = S.Dept_Id

SELECT St_Fname , Dept_Name
FROM Student S RIGHT OUTER JOIN Department D
ON D.Dept_Id = S.Dept_Id

SELECT St_Fname , Dept_Name
FROM Student S FULL OUTER JOIN Department D
ON D.Dept_Id = S.Dept_Id
```

### Self join
```SQL
SELECT X.St_Fname as SName , Y.St_Fname as SuperID
FROM Student X , Student Y
WHERE Y.St_id = X.St_super
```

```SQL
--Update + JOIN 
UPDATE Stud_Course 
SET Grade += 10

SELECT grade 
FROM Student S , Stud_Course SC
WHERE s.St_Id = SC.St_Id and St_Address = 'cairo'
```

### NULL
```SQL
SELECT st_fname 
FROM Student
Where st_fname IS NOT NULL

SELECT isnull(St_Fname,' ')
From Student

SELECT isnull(St_Fname,'has no name')
From Student

SELECT isnull(St_Fname,St_Lname)
From Student
```

### Multiple Replacement
```SQL
SELECT COALESCE(St_fname , st_lname,st_address,'NO DATA')
FROM Student

SELECT st_fname + ' ' + convert(varchar(2),st_age)
From Student

SELECT isnull(st_fname,'') + ' ' + convert(varchar(2),isnull(st_age,0))
FROM Student
```

----   _ one char 
----   % more than one char 


