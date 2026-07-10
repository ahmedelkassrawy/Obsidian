#### Ternary Operator

```C++
if (condition)
    statement1;
else
    statement2;
```
```
condition ? True : False;
```

Example:
```C++
if(a%2 == 0)
{
	return a*8;
}
else
{

	return a*9;
}
```
```C++
//with ternary operator
return a%2 == 0 ? a*8 : a*9;

```
switch statment doesnt work on logical operators.

```C++
//how to find the length of an array
#include <iostream>
using namespace std;

// Driver code
int main()
{
    // Initializing an arraay with some elements
    int arr[] = { 1, 2, 3, 5, 6, 7, 8, 9 };
    // Finding the length of the array
    int length = sizeof(arr) / sizeof(arr[0]);
    // Printing the length of the array
    cout << "Length of the array is " << length << endl;

    return 0;
}

```

```C++
#include <cmath>
//power of a num
double x
{ 
std::pow(3.0, 4.0) // 3 to the 4th power
}; 
```

- use while loop if you don't know how many times you want to do sth.
## Palindrome
palindrome is looking if a reverse is = to the original before reverse
```C++
#include <iostream>
using namespace std;
int main()
{
  int digit,num,rev = 0,m;
  cin>>num;
  m = num;
  //number ==> digits
  while(num > 0)
  {
    digit = num % 10;
    num /= 10;
    rev = rev* 10 + digit;
  }
  if(m == rev) cout<<rev<<endl<<"YES";
  else cout<<rev<<endl<<"NO";
}
```

*num % 10 gives you the last digit in num.
*num /= 10 ==> removes the last digit*
![[Pasted image 20240423190247.png]]
after adding the digit
![[Pasted image 20240423190325.png]]
- `while (cin >> num1 >> num2)`: This is the `while` loop condition. The loop will continue to execute as long as reading integers from the input stream `cin` is successful. If reading fails (e.g., due to reaching the end of the input or encountering non-integer input), the loop will terminate.
- @







- floor is rounding the number to a int like (3.32) becomes 3
- prime function start with for loop intiallize i to 2, i less than or equal sqrt of number and if num % that i equal zero then return false else return true
```C++
bool isPrime(long long num)
{
    if (num < 2)
    {
        return false;
    }

    for (int i = 2; i <= sqrt(num); i++)
    {
        if (num % i == 0)
            return false;
    }

    return true;
```

- max distinct numbers
```C++
long long num = (sqrt(8 * N + 1) - 1) / 2;
```

```C++
bool is_prime(int n) {
    if (n <= 1) return false;
    for (int i = 2; i * i <= n; ++i) {

        if (n % i == 0) return false;

    }
    return true;
}//O(n^1/2)
```

btdwr 3la rkm msln zhr kam mra momken nstd5m frequency array aw fy tre2a tnya
```C++
int index1 = 0, index2 = 0, index3 = 0;
    int num;

    for (int i = 1; i <= size; i++)
    {
        cin >> num;
        if (num == 1)
        {
            ones[index1] = i;
            index1++;
        }
        else if (num == 2)
        {
            twos[index2] = i;
            index2++;
        }
        else
        {
            threes[index3] = i;
            index3++;
        }
    }
```

ht3ml array lkol rakm(hena nf3t 34ana arkam so8yra akbr mn dy m4 hynf3 )
yhb2a index bta3tk lkol rkm bytsyve wbtzwd literrator b3dha.



str.find(char) --> returns index 