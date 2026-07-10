### Self Join 2
```SQL
SELECT x.Fname, y.Superssn
FROM Employee x 
JOIN Employee y 
ON x.Superssn = y.SSN
WHERE y.Fname = 'Kamel' AND y.Lname = 'Mohamed';
```

### ADHOCS
```SQL
SELECT dname,Departments.Dnum,count(dnum) AS Emp_count
from Departments JOIN employee
ON Employee.dno = Departments.Dnum
group by Dname,Dnum
HAVING avg(salary) < (select avg(salary) from Employee)

SELECT Employee.SSN , fname + ' ' + lname AS Employee_Name 
FROM Employee
where EXISTS(
	SELECT 1 FROM Dependent
	WHERE Dependent.ESSN = Employee.SSN
)

UPDATE Employee 
SET Dno = 100
WHERE SSN = 968574;

INSERT INTO Employee (Fname, Lname, SSN, Dno)
VALUES ('Kassra', 'Mohammed', 102672, 20);

DELETE FROM Employee
where ssn = 223344;
```