## 1. Basic Recursion: Printing Numbers

### Concept

- **Pre-call vs. Post-call execution** affects the order of operations.
- When the print statement is before the recursive call, it executes bottom-up.
- When the print statement is after the recursive call, it executes top-down (backtracking).

### Example 1: Print Before Recursive Call

- Stack fills: `main -> f(3,3) + print(3) -> f(2,3) + print(2) -> f(1,3) + print(1)`
- Output: `3 2 1`

```cpp
#include <iostream>
using namespace std;

void f(int i, int n) {
    if (i < 1) return;
    cout << i << "\n";
    f(i - 1, n);
}

int main() {
    int i, n;
    cin >> i >> n;
    f(i, n);
}
```

### Example 2: Print After Recursive Call

- Stack fills: `main -> f(3,3) -> f(2,3) -> f(1,3) -> top`
- Prints during backtracking: `print(1) -> print(2) -> print(3)`
- Output: `1 2 3`

```cpp
#include <iostream>
using namespace std;

void f(int i, int n) {
    if (i < 1) return;
    f(i - 1, n);
    cout << i << "\n";
}

int main() {
    int i, n;
    cin >> i >> n;
    f(i, n);
}
```

## 2. Factorial (Sum Up to n)

### Concept

- Recursive function to compute `n + (n-1) + ... + 1`.
- Call stack evaluates from innermost call outward.

### Example

- For `n = 3`: `main -> fact(3) = 3 + fact(2) -> 3 + 2 + fact(1) -> 3 + 2 + 1`
- Output: `6`

```cpp
#include <iostream>
using namespace std;

int fact(int n) {
    if (n == 0) return 0;
    return n + fact(n - 1);
}

int main() {
    int n;
    cin >> n;
    cout << fact(n);
    return 0;
}
```

## 3. Array Reversal

### Concept

- Swap elements from both ends of the array recursively.
- Base case: when left index `l` is greater than or equal to right index `r`.

### Example

- Array: `{1, 2, 3, 4, 2}`
- Recursive swaps: `f(0,4) -> swap(1,2) -> f(1,3) -> swap(2,4) -> f(2,2)`
- Output: `2 4 3 2 1`

```cpp
#include <iostream>
using namespace std;

int a[] = {1, 2, 3, 4, 2};

void f(int l, int r) {
    if (l >= r) return;
    swap(a[l], a[r]);
    f(l + 1, r - 1);
}

int main() {
    int i, n;
    cin >> i >> n;
    f(i, n);
    for (int i = 0; i < 5; i++)
        cout << a[i] << " ";
    return 0;
}
```

## 4. Palindrome Check

### Concept

- Check if a string is a palindrome by comparing characters from both ends.
- Base case: when index `i` reaches or exceeds half the string length.

### Example

- Input: `n = 5, s = "radar"`
- Checks: `s[0] == s[4]`, `s[1] == s[3]`, etc.
- Output: `YES`

```cpp
#include <iostream>
#include <string>
using namespace std;

string s;
int n;

bool f(int i) {
    if (i >= (n / 2)) return true;
    if (s[i] != s[n - i - 1]) return false;
    return f(i + 1);
}

int main() {
    cin >> n >> s;
    if (f(0)) cout << "YES";
    else cout << "NO";
    return 0;
}
```

## 5. Fibonacci with Memoization

### Concept

- Compute Fibonacci numbers using recursion with memoization to avoid redundant calculations.
- Store results in a `dp` array to optimize performance.

### Example

- For `n = 5`: Computes `fib(5) = fib(4) + fib(3)` with memoized values.
- Output: `5` (Fibonacci sequence: 0, 1, 1, 2, 3, 5)

```cpp
#include <iostream>
#include <vector>
using namespace std;

int n;
vector<int> dp(1000, -1);

int fib(int n) {
    if (n == 0) return 0;
    if (n == 1) return 1;
    if (dp[n] != -1) return dp[n];
    return dp[n] = fib(n - 1) + fib(n - 2);
}

int main() {
    cin >> n;
    cout << fib(n);
    return 0;
}
```

## 6. Backtracking: Print All Subsets

### Concept

- Generate all possible subsets of an array using backtracking.
- At each index, decide to include or exclude the element.

### Example

- Array: `{1, 2, 3}`
- Output: All subsets including `{}`, `{1}`, `{2}`, `{3}`, `{1, 2}`, etc.

```cpp
#include <iostream>
#include <vector>
using namespace std;

void printt(int idx, vector<int> &ds, int arr[], int n) 
{
    if (idx == n) 
    {
        for (int i = 0; i < ds.size(); i++)
            cout << ds[i] << " ";
            
        if (ds.size() == 0)
            cout << "{}";
        cout << endl;
        return;
    }
    printt(idx + 1, ds, arr, n);
    ds.push_back(arr[idx]);
    
    printt(idx + 1, ds, arr, n);
    ds.pop_back();
}

int main() 
{
    int arr[] = {1, 2, 3};
    vector<int> ds;
    
    printt(0, ds, arr, 3);
    return 0;
}
```

## 7. Backtracking: Subsets with Given Sum

### Concept

- Find all subsets of an array that sum to a given value.
- Track the current sum and include/exclude elements recursively.

### Example

- Array: `{1, 2, 3}`, Target sum: `5`
- Output: `{2, 3}`

```cpp
#include <iostream>
#include <vector>
using namespace std;

void printt(int idx, vector<int> &ds, int arr[], int n, int s, int sum) {
    if (idx == n) {
        if (s == sum) {
            for (int i = 0; i < ds.size(); i++)
                cout << ds[i] << " ";
            cout << endl;
        }
        return;
    }
    ds.push_back(arr[idx]);
    s += arr[idx];
    
    printt(idx + 1, ds, arr, n, s, sum);
    
    ds.pop_back();
    s -= arr[idx];
    
    printt(idx + 1, ds, arr, n, s, sum);
}

int main() {
    int arr[] = {1, 2, 3};
    vector<int> ds;
    int sum = 5;
    printt(0, ds, arr, 3, 0, sum);
    return 0;
}
```

## 8. Print Numbers with Backtracking

### Concept

- **Backtracking** involves making recursive calls first and performing actions (e.g., printing) during the unwinding of the call stack.
- For printing from **1 to N**, recursive calls reach the base case, then print in ascending order.
- For printing from **N to 1**, recursive calls reach the base case, then print in descending order.

### Example 1: Print from N to 1 (Backtracking)

- **Logic**: Make recursive calls until `i > n`, then print `i` during backtracking.
- Stack: `main -> f(1,n) -> f(2,n) -> ... -> f(n+1,n)` (base case), then print `1, 2, ..., n`.
- Input: `n = 5`
- Output: `5 4 3 2 1`

```cpp
#include <iostream>
using namespace std;

void printOneToN(int i, int n) {
    if (i > n) return;
    printOneToN(i + 1, n);
    cout << i << " ";
}

int main() {
    int n;
    cin >> n;
    printOneToN(1, n);
    return 0;
}
```

### Example 2: Print from N to 1 (Backtracking)

- **Logic**: Make recursive calls until `i < 1`, then print `i` during backtracking.
- Stack: `main -> f(n,n) -> f(n-1,n) -> ... -> f(0,n)` (base case), then print `n, n-1, ..., 1`.
- Input: `n = 5`
- Output: `1 2 3 4 5`

```cpp
#include <iostream>
using namespace std;

void printNToOne(int i, int n) {
    if (i < 1) return;
    printNToOne(i - 1, n);
    cout << i << " ";
}

int main() {
    int n;
    cin >> n;
    printNToOne(n, n);
    return 0;
}
```