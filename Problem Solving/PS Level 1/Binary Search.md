---
tags: [problem-solving, binary-search, level-1]
difficulty: beginner
topic: Binary Search
---
# 🔍 Binary Search — From Zero

> [!abstract] What you'll learn
> 1. The **idea** behind binary search (guess-the-number game).
> 2. How to **walk through it by hand**, step by step.
> 3. Writing the **basic search** yourself.
> 4. The two famous variants: **lower bound** and **upper bound**.
> 5. Letting C++ **STL** do it for you.
>
> We go slow first, then ramp up the difficulty. 🚀

---

## 1. The Big Idea 🧠

Imagine I think of a number between **1 and 100**, and you must guess it.
After each guess I only say **"higher"** or **"lower"**.

The smart move is to **always guess the middle**. Every guess throws away
**half** of the remaining numbers.

```
Guess 50  → "higher"   → throw away 1..50
Guess 75  → "lower"    → throw away 76..100
Guess 62  → "higher"   → throw away 51..62
...
```

That halving is *binary search*. On a sorted list of 1,000,000 items you
find anything in about **20 steps** instead of 1,000,000.

> [!warning] The one rule you cannot break
> The array **must be sorted**. Binary search on unsorted data gives garbage.

---

## 2. How It Works — 3 Pointers

We track a search window with three markers:

```
  l  = left edge   (start of the window)
  r  = right edge  (end of the window)
  mid = the middle  = (l + r) / 2   ← integer division
```

Picture the window as a box. Everything **outside** the box is already
ruled out; we only ever look **inside** it:

```
 index:   0    1    2    3    4    5    6
 value: [ 2 ][ 5 ][ 8 ][12 ][16 ][23 ][38 ]
          ^                             ^
          l            mid              r
```

Each step we:
1. Look at `arr[mid]`.
2. Decide: is our target to the **left** or the **right** of mid?
3. Shrink the box by moving `l` or `r`.
4. Repeat until the box is empty (`l > r`).

---

## 3. Worked Example — Find `23` 🐢 (slow & careful)

Array (sorted): `[2, 5, 8, 12, 16, 23, 38]`, target = **23**.

We start with `l = 0`, `r = 6`.

**Step 1** — `mid = (0 + 6) / 2 = 3`, so `arr[3] = 12`.

```
 [ 2 ][ 5 ][ 8 ][12 ][16 ][23 ][38 ]
   l              m               r
```
`12 < 23` → target is on the **right**. Move `l = mid + 1 = 4`.

**Step 2** — window is now `[16, 23, 38]`. `mid = (4 + 6) / 2 = 5`, `arr[5] = 23`.

```
 [ 2 ][ 5 ][ 8 ][12 ][16 ][23 ][38 ]
                       l    m    r
```
`23 == 23` → **found it at index 5!** ✅

Notice we only looked at **2 elements** (12 and 23) out of 7.

---

## 4. Your First Binary Search (does the target exist?) ✍️

Before the fancy variants, here is the plain "is it there?" version.
Read the comments — they map exactly to the steps above.

```C++
#include <iostream>
#include <vector>
#include <map>
#include <math.h>
#include <algorithm>
#include <numeric>
#include <unordered_map>
using namespace std;

int main() 
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n,x;
    cin>>n>>x;

    vector<int> arr(n);
    for(int i =0; i < n; i++)
    {
        cin>>arr[i];
    }

    sort(arr.begin(), arr.end());

    int l = 0;
    int r = n - 1;

    while(l <= r)
    {
        int mid = l + (r - l) / 2;

        if(arr[mid] == x)
        {
            cout<<mid<<"\n";
            return 0;
        }
        else if(arr[mid] < x)
        {
            l = mid + 1;
        }
        else
        {
            r = mid - 1;
        }
    }

    cout<<"-1\n";

    return 0;
}
```

> [!tip] Why `l <= r` and not `l < r`?
> When `l == r` the window still holds **one** element — we must check it.
> Stopping early would miss single-element windows.

> [!note] A subtle safety trick
> `mid = (l + r) / 2` can overflow if `l` and `r` are huge.
> The overflow-safe form is `mid = l + (r - l) / 2`. Same value, no overflow.

---

## 5. Level Up — Lower Bound 📈

Sometimes the exact target isn't there, or appears many times, and we want
**the first element that is `>= x`** (the "insertion point").

That is the **lower bound**.

```
 target x = 16
 array:  [ 2 ][ 5 ][ 8 ][12 ][16 ][16 ][23 ]
                             ^
                     first value >= 16  → index 4
```

Instead of stopping when we find `x`, we **keep shrinking to the left**
every time `arr[mid] >= x`, remembering the best candidate so far.

```C++
#include <iostream>
#include <vector>
#include <map>
#include <math.h>
#include <algorithm>
#include <numeric>
#include <unordered_map>
using namespace std;

int main() 
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n,x;
    cin>>n>>x;

    vector<int> arr(n);
    for(int i =0; i < n; i++)
    {
        cin>>arr[i];
    }

    sort(arr.begin(), arr.end());

    int l = 0;
    int r = n - 1;
    int ans = 0;

    while(l <= r)
    {
        int mid = l + (r - l) / 2;

        if(arr[mid] >= x)
        {
            ans = mid;
            r = mid - 1;
        }
        else
        {
            l = mid + 1;
        }
    }

    cout<<ans<<"\n";

    return 0;
}
```

> [!info] Read the key line
> `arr[mid] >= x` → we found a valid answer, but maybe there's an even
> earlier one, so we move `r` left. That "keep searching left" is what
> makes it *lower* bound.

---

## 6. Level Up More — Upper Bound 📊

**Upper bound** is almost identical, but we want the **first element that
is strictly `> x`** (the first one *past* all copies of `x`).

The **only change** is the comparison: `>` instead of `>=`.

```
                 lower_bound(16)      upper_bound(16)
                      │                    │
                      v                    v
 array:  [ 8 ][12 ][16 ][16 ][16 ][23 ][38 ]
   index:  0    1    2    3    4    5    6

 lower_bound → first value >= 16  → index 2
 upper_bound → first value  > 16  → index 5
```

```C++
#include <iostream>
#include <vector>
#include <map>
#include <math.h>
#include <algorithm>
#include <numeric>
#include <unordered_map>
using namespace std;

int main() 
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n,x;
    cin>>n>>x;

    vector<int> arr(n);
    for(int i =0; i < n; i++)
    {
        cin>>arr[i];
    }

    sort(arr.begin(), arr.end());

    int l = 0;
    int r = n - 1;
    int ans = 0;

    while(l <= r)
    {
        int mid = l + (r - l) / 2;

        if(arr[mid] > x)
        {
            ans = mid;
            r = mid - 1;
        }
        else
        {
            l = mid + 1;
        }
    }

    cout<<ans<<"\n";

    return 0;
}
```

> [!tip] Remember the difference in one line
> **lower_bound** = first `>= x`  •  **upper_bound** = first `> x`.
> Together they give you *how many copies of `x` exist*:
> `count = upper_bound - lower_bound`.

---

## 7. The Shortcut — C++ STL 🏎️

You almost never write the loop by hand in real contests. The standard
library already ships both, and they run in the same `O(log n)`:

```C++
#include <bits/stdc++.h>
using namespace std;

int main()
{
    int n, q;
    cin >> n >> q;

    vector<int> arr(n);
    for (int i = 0; i < n; i++) cin >> arr[i];

    while (q--)
    {
        int x;
        cin >> x;

        // returns an ITERATOR to the first element > x
        auto it = upper_bound(arr.begin(), arr.end(), x);

        if (it == arr.end())            // nothing greater → not found
        {
            cout << -1 << endl;
        }
        else
        {
            int ans = it - arr.begin(); // iterator → index (0-based)
            cout << ans + 1 << endl;    // +1 for 1-based output
        }
    }
}
```

> [!note] The two functions you'll use forever
> - `lower_bound(begin, end, x)` → iterator to first `>= x`
> - `upper_bound(begin, end, x)` → iterator to first `> x`
> - Subtract `arr.begin()` from the iterator to turn it into an **index**.
> - If the iterator equals `arr.end()`, no such element exists.

---

## 8. Cheat Sheet 📋

| Question | Tool | Comparison |
|---|---|---|
| Does `x` exist? | plain binary search | `arr[mid] == x` |
| First index `>= x`? | lower bound | `arr[mid] >= x`, move `r` left |
| First index `> x`? | upper bound | `arr[mid] > x`, move `r` left |
| How many `x`? | both | `upper_bound - lower_bound` |

> [!success] Golden rules
> 1. Array **must be sorted**.
> 2. Loop while `l <= r`.
> 3. Use `mid = l + (r - l) / 2` to be overflow-safe.
> 4. Each step **halves** the window → `O(log n)`.

---

## 9. Practice Next 🎯

- [ ] Find the **first** and **last** position of a target (use both bounds).
- [ ] Count how many numbers fall in a range `[a, b]` (two upper bounds).
- [ ] "Binary search on the answer" — search over a *value range*, not an
      array (e.g. minimum capacity, square root). ← this is Level 2.

Related: [[Two Pointers]] • [[Prefix Sum]] • [[Sorting]]
