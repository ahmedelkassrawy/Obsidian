## 1. Understanding Recursion Basics

### Example 1: Countdown (No Base Case)

Without a base case, recursion can lead to infinite calls, causing a stack overflow.

```python
def countdown(i):
    print(i)
    countdown(i - 1)  # No base case
```

- **Issue**: No condition stops the recursion, leading to infinite calls.
- **Output**: Prints `i`, then calls `countdown(i-1)` indefinitely until a crash.

### Example 2: Countdown (With Base Case)

A base case ensures recursion terminates.

```python
def countdown(i):
    print(i)
    if i <= 1:  # Base case
        return
    else:  # Recursive case
        countdown(i - 1)
```

- **Base Case**: `i <= 1` stops recursion.
- **Recursive Case**: Calls `countdown(i-1)` for `i > 1`.
- **Output** (e.g., `countdown(5)`): Prints `5, 4, 3, 2, 1`.

### Stack Mechanism

- Each recursive call is pushed onto the call stack (enqueue).
- When the base case is reached, the stack unwinds (dequeue), executing the remaining code in each call.
- The stack saves the state of each call (e.g., local variables, return address) until the base case is executed, then processes calls in reverse order.

## 2. Recursive Function with Conditional Logic

### Example 3: Collatz-like Function

This C++ function applies different operations based on whether the input is even or odd.

```cpp
#include <iostream>
using namespace std;

int fun(int x) {
    cout << x << " ";  // Executed at each call
    if (x == 1)        // Base case
        return 0;
    if (x % 2 == 0)    // Recursive case (even)
        return fun(x / 2);
    else               // Recursive case (odd)
        return fun(x * 3 + 1);
}

int main() {
    int num;
    cin >> num;
    fun(num);
}
```

- **Base Case**: `x == 1`, returns 0 and stops recursion.
- **Recursive Cases**:
    - If `x` is even: Call `fun(x / 2)`.
    - If `x` is odd: Call `fun(x * 3 + 1)`.
- **Execution Example** (input `5`):
    - `5` (odd) → `fun(5*3+1 = 16)` → prints `5`.
    - `16` (even) → `fun(16/2 = 8)` → prints `16`.
    - `8` (even) → `fun(8/2 = 4)` → prints `8`.
    - `4` (even) → `fun(4/2 = 2)` → prints `4`.
    - `2` (even) → `fun(2/2 = 1)` → prints `2`.
    - `1` (base case) → prints `1`, returns.
    - Output: `5 16 8 4 2 1`.
- **Stack Behavior**: Each call is pushed to the stack. When `x == 1`, the stack unwinds, and no further code executes after the base case.

## 3. Order of Execution in Recursion

### Example 4: Print Binary Representation

The order of the recursive call and the print statement affects the output.

#### Version 1: Print Before Recursive Call

```cpp
void printBinary(int n) {
    if (n <= 1) {
        cout << n;  // Base case
    } else {
        cout << n % 2;         // Print before recursion
        printBinary(n / 2);    // Recursive call
    }
}
```

- **Input**: `10`.
- **Execution**:
    - `n = 10`: Prints `10 % 2 = 0`, calls `printBinary(10/2 = 5)`.
    - `n = 5`: Prints `5 % 2 = 1`, calls `printBinary(5/2 = 2)`.
    - `n = 2`: Prints `2 % 2 = 0`, calls `printBinary(2/2 = 1)`.
    - `n = 1`: Prints `1`.
- **Output**: `0101` (least significant bit first).

#### Version 2: Print After Recursive Call

```cpp
void printBinary(int n) {
    if (n <= 1) {
        cout << n;  // Base case
    } else {
        printBinary(n / 2);    // Recursive call
        cout << n % 2;         // Print after recursion
    }
}
```

- **Input**: `10`.
    
- **Execution**:
    
    - `n = 10`: Calls `printBinary(10/2 = 5)`, defers printing.
    - `n = 5`: Calls `printBinary(5/2 = 2)`, defers printing.
    - `n = 2`: Calls `printBinary(2/2 = 1)`, defers printing.
    - `n = 1`: Prints `1`.
    - Unwind: Prints `2 % 2 = 0`, `5 % 2 = 1`, `10 % 2 = 0`.
- **Output**: `1010` (most significant bit first, correct binary).
    
- **Key Insight**: The placement of the print statement relative to the recursive call determines whether the output is processed during the call (down the stack) or during the unwind (up the stack).
    

## 4. Counting Recursion Iterations

To count occurrences (e.g., vowels in a string), initialize a counter in `main` and pass it by reference to the recursive function.

### General Approach

- Initialize an integer in `main`.
- Pass it by reference (`&`) to the recursive function.
- Increment the counter in the recursive function for each valid case.

### Example: Counting Vowels (Pseudo-Code)

```cpp
#include <iostream>
#include <string>
using namespace std;

void countVowels(string s, int index, int& count) {
    if (index >= s.length())  // Base case
        return;
    if (s[index] == 'a' || s[index] == 'e' || s[index] == 'i' || 
        s[index] == 'o' || s[index] == 'u')
        count++;  // Increment for vowel
    countVowels(s, index + 1, count);  // Recursive call
}

int main() {
    string s;
    cin >> s;
    int count = 0;
    countVowels(s, 0, count);
    cout << count;
}
```

- **Initialization**: `count = 0` in `main`.
- **By Reference**: `int& count` allows the function to modify `count`.
- **Increment**: `count++` for each vowel.
- **Recursion**: Processes each character until the end of the string.

## 5. Recursive Array Processing

### Example 5: Calculate Average of Array

This C++ program calculates the average of a vector using recursion.

```cpp
#include <iostream>
#include <vector>
#include <iomanip> // for setprecision
using namespace std;

double calculateAverage(vector<int>& arr, int index) {
    if (index == arr.size()) {
        return 0;  // Base case: return 0 when index exceeds array size
    } else {
        return arr[index] + calculateAverage(arr, index + 1);  // Sum of current element and recursive call
    }
}

int main() {
    int N;
    cin >> N;

    vector<int> A(N);  // Initialize vector with size N
    for (int i = 0; i < N; ++i) {
        cin >> A[i];
    }

    double sum = calculateAverage(A, 0);  // Calculate sum using recursion
    double average = sum / N;  // Calculate average

    cout << fixed << setprecision(6) << average;  // Print average with 6 digits after decimal

    return 0;
}
```

- **Vector Initialization**:
    - `vector<int> A(N)` creates a vector of size `N`.
    - Input is read using a loop: `cin >> A[i]`.
    - Unlike arrays, vectors dynamically allocate memory and are safer.
- **Recursive Function**:
    - **Base Case**: `index == arr.size()`, returns `0`.
    - **Recursive Case**: Returns `arr[index] + calculateAverage(arr, index + 1)`.
    - The recursion computes the sum: `arr[0] + arr[1] + ... + arr[N-1]`.
- **Stack Unwinding**:
    - For `N=3`, `A=[1,2,3]`:
        - `calculateAverage(A, 0)` → `A[0] + calculateAverage(A, 1)`.
        - `calculateAverage(A, 1)` → `A[1] + calculateAverage(A, 2)`.
        - `calculateAverage(A, 2)` → `A[2] + calculateAverage(A, 3)`.
        - `calculateAverage(A, 3)` → `0` (base case).
        - Unwinds: `3 + 0 = 3`, `2 + 3 = 5`, `1 + 5 = 6`.
    - `sum = 6`, `average = 6/3 = 2.0`.
- **Output**: Uses `fixed << setprecision(6)` to format the average (e.g., `2.000000`).

## Study Tips

- Trace recursive calls on paper for small inputs to understand stack behavior.
- Experiment with code by changing the order of print statements or recursive calls.
- Practice writing recursive functions for simple problems (e.g., factorial, Fibonacci) before tackling complex ones like knapsack.
- Use debugging tools to step through recursive calls and inspect the stack.