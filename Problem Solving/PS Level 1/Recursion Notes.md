---
title: Recursion Notes
tags:
  - problem-solving
  - recursion
  - backtracking
  - competitive-programming
aliases:
  - Recursion
---

# Recursion Notes

> [!abstract] What's in here
> Recursion from the ground up: how the call stack drives execution order, the classic patterns (linear recursion, accumulate-on-return, two-pointer, memoization), and the pick/don't-pick backtracking template that powers subset generation.

> [!tip] The mental model
> Every recursive function answers three questions:
> 1. **Base case** — when do I stop?
> 2. **Work** — what do I do at this level?
> 3. **Recurrence** — how do I shrink the problem toward the base case?
>
> The subtle part is *when* the work happens: **before** the recursive call (top-down, on the way *in*) or **after** it (bottom-up, on the way *out* — "backtracking").

---

## 1. Basic Recursion: Printing Numbers

### Concept

- **Pre-call vs. post-call execution** decides the order of operations.
- Print **before** the recursive call → runs on the way in (top-down).
- Print **after** the recursive call → runs on the way out (during backtracking).

### Example 1 — Print *before* the recursive call

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

### Example 2 — Print *after* the recursive call

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

> [!note] The one-line difference
> Both functions count down the same way. Only the **position of the `cout`** relative to `f(i - 1, n)` changes — and that flips the output from descending to ascending. This is the single most important intuition in recursion.

---

## 2. Sum from 1 to n (accumulate on return)

### Concept

- Recursively compute `n + (n-1) + ... + 1`.
- Each frame adds its own `n`, then trusts the recursive call to return the sum of everything smaller.
- The additions actually happen as the stack **unwinds**.

### Example

- For `n = 3`: `fact(3) = 3 + fact(2) = 3 + (2 + fact(1)) = 3 + 2 + 1 + fact(0)`
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

> [!warning] It's a *sum*, not a factorial
> Despite the name `fact`, this computes $\sum_{k=1}^{n} k = \tfrac{n(n+1)}{2}$, **not** $n!$. For a true factorial the base case returns `1` and the operator is `*`:
> ```cpp
> if (n == 0) return 1;
> return n * fact(n - 1);
> ```

---

## 3. Array Reversal (two pointers)

### Concept

- Swap the outermost pair, then recurse inward on the rest.
- **Base case:** left index `l >= r` — the pointers met (or crossed), nothing left to swap.

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

> [!note] Feeding the example
> `main` reads `l` and `r` from input, so to reverse the whole 5-element array you'd type `0 4`. In general pass `f(0, size - 1)`.

---

## 4. Palindrome Check

### Concept

- Compare characters from both ends inward: `s[i]` vs `s[n - i - 1]`.
- **Base case:** once `i` reaches the middle (`i >= n / 2`), all pairs matched → it's a palindrome.
- Any mismatch short-circuits to `false` immediately.

### Example

- Input: `n = 5, s = "radar"`
- Checks: `s[0] == s[4]`, `s[1] == s[3]` (middle char `s[2]` is skipped)
- Output: `YES`

```cpp
#include <iostream>
#include <string>
using namespace std;

string s;
int n;

bool f(int i) 
{
    if (i >= (n / 2)) return true;
    if (s[i] != s[n - i - 1]) return false;

    return f(i + 1);
}

int main() 
{
    cin >> n >> s;

    if (f(0)) cout << "YES";
    else cout << "NO";

    return 0;
}
```

> [!tip] Why only `n / 2` checks
> Each comparison validates **two** characters at once, so you only need to reach the halfway point. The middle character of an odd-length string never needs checking — it's its own mirror.

---

## 5. Fibonacci with Memoization

### Concept

- Plain recursive Fibonacci recomputes the same subproblems exponentially often.
- **Memoization** caches each result in a `dp` array; a value is computed once, then reused in $O(1)$.

### Example

- For `n = 5`: `fib(5) = fib(4) + fib(3)`, reusing memoized `fib(3)`, `fib(2)`…
- Output: `5` (sequence: 0, 1, 1, 2, 3, 5)

```cpp
#include <iostream>
#include <vector>
using namespace std;

int n;
vector<int> dp(1000, -1);

int fib(int n) 
{
    if (n == 0) return 0;
    if (n == 1) return 1;
    
    if (dp[n] != -1) return dp[n];
    
    return dp[n] = fib(n - 1) + fib(n - 2);
}

int main() 
{
    cin >> n;
    
    cout << fib(n);
    
    return 0;
}
```

> [!info] Complexity: exponential → linear
> | Version | Time | Why |
> |---|---|---|
> | Naive `fib(n-1) + fib(n-2)` | $O(\varphi^{\,n}) \approx O(2^n)$ | each call spawns two, subtrees overlap |
> | Memoized (above) | $O(n)$ | each `dp[n]` filled exactly once |
>
> `-1` is the "not computed yet" sentinel — safe here because no Fibonacci value is negative.

> [!warning] Overflow
> `int` Fibonacci overflows around `fib(47)`. Use `long long` (and a matching `dp`) for larger `n`.

---

## 6. Backtracking: Print All Subsets

### Concept

- Walk the array index by index; at each element make a binary choice: **exclude it** or **include it**.
- That's the universal **pick / don't-pick** pattern — `push_back` → recurse → `pop_back` (undo).
- Reaching `idx == n` means one complete subset has been decided → print it.

### Example

- Array: `{1, 2, 3}`
- Output: all $2^3 = 8$ subsets — `{}`, `{1}`, `{2}`, `{3}`, `{1,2}`, … `{1,2,3}`

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

> [!note] The two recursive calls
> - First `printt(idx + 1, …)` — the **don't-pick** branch (element left out).
> - Then `push_back`, recurse (the **pick** branch), then `pop_back` to restore `ds` before returning to the caller.
>
> The `pop_back` is the heart of backtracking: it rewinds the shared `ds` so the next branch starts from a clean state.

> [!info] Complexity
> $O(2^n)$ leaves × $O(n)$ to print each ⇒ $O(n \cdot 2^n)$. Passing `ds` by reference (`&`) avoids copying the vector on every call.

---

## 7. Backtracking: Subsets with a Given Sum

### Concept

- Same pick/don't-pick skeleton, but carry a running `s` (current sum).
- At a full subset (`idx == n`), print it **only if** `s == sum`.

### Example

- Array: `{1, 2, 3}`, target `sum = 5`
- Output: `2 3`

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

> [!tip] `s` is passed by value — no manual undo needed
> Because `s` is a copy per frame, the `s -= arr[idx]` isn't strictly required for correctness (the child's changes don't leak back). But `ds` **is** shared by reference, so its `pop_back` undo *is* mandatory. Keeping both undos side by side makes the pattern uniform and easy to extend.

---

## 8. Print Numbers with Backtracking

### Concept

- **Backtracking** here means: recurse first, act (print) on the way back up.
- Whether you count *up* or *down* in the recursion decides which direction the printing runs.

### Example 1 — count up, print on the way back → `5 4 3 2 1`

- **Logic:** recurse `i + 1` until `i > n` (base case), then print `i` while unwinding.
- Stack: `main -> f(1,n) -> f(2,n) -> ... -> f(n+1,n)` (base), then prints `n, n-1, ..., 1`.
- Input: `n = 5` → Output: `5 4 3 2 1`

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

### Example 2 — count down, print on the way back → `1 2 3 4 5`

- **Logic:** recurse `i - 1` until `i < 1` (base case), then print `i` while unwinding.
- Stack: `main -> f(n,n) -> f(n-1,n) -> ... -> f(0,n)` (base), then prints `1, 2, ..., n`.
- Input: `n = 5` → Output: `1 2 3 4 5`

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

> [!note] Deepest frame prints first
> Because the print is *after* the recursive call, the **last** frame pushed is the **first** to print. So counting *up* to `n` and printing on return yields `n … 1`, while counting *down* yields `1 … n` — the reverse of what the recursion direction alone suggests. (Both headings read "N to 1", but Example 2 actually prints `1 → 5`.)

---

## Pattern cheat-sheet

| Pattern | Where the work goes | Effect | Section |
|---|---|---|---|
| Print pre-call | before recursion | top-down (in-order) | [[#1 Basic Recursion Printing Numbers\|§1]] |
| Print post-call | after recursion | bottom-up (reversed) | [[#1 Basic Recursion Printing Numbers\|§1]], [[#8 Print Numbers with Backtracking\|§8]] |
| Accumulate on return | `return x + f(...)` | fold/aggregate | [[#2 Sum from 1 to n accumulate on return\|§2]] |
| Two pointers | shrink `l++`, `r--` | in-place reversal / palindrome | [[#3 Array Reversal two pointers\|§3]], [[#4 Palindrome Check\|§4]] |
| Memoization | cache in `dp[]` | kill repeated subproblems | [[#5 Fibonacci with Memoization\|§5]] |
| Pick / don't-pick | `push` → recurse → `pop` | enumerate all subsets | [[#6 Backtracking Print All Subsets\|§6]], [[#7 Backtracking Subsets with a Given Sum\|§7]] |

## See also

- [[Number Theory]] — modular arithmetic, binary exponentiation (itself a divide-and-conquer recursion)
- [[Backtracking]]
- [[Dynamic Programming]]
