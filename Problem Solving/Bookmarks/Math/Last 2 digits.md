https://codeforces.com/group/MWSDmqGsZm/contest/219158/problem/Y
```C++
1. #include <iostream>
2. using namespace std;

1. void solution1()
2. {
3. long long a, b;
4. long long c, d;
5. cin >> a >> b >> c >> d;
6. //- The code calculates the last two digits of each number by taking modulo 100.
7. long long a1 = a % 100;
8. long long b1 = b % 100;
9. long long c1 = c % 100;
10. long long d1 = d % 100;
11. //takes them all multiple multiplications
12. long long x = a1 * b1 * c1 * d1;
13. //- Finally, it checks if the last two digits of the product `x` are less than or equal to 9.
14. //If true, it prints a leading zero followed by the last two digits.
- //Otherwise, it prints only the last two digits.
15. if (x % 100 <= 9)
16. {
17. cout << "0" << x % 100;
18. }
19. else
20. {
21. cout << x % 100;
22. }
23. 
24. }
25. int main()
 {
 solution1();
 }
```