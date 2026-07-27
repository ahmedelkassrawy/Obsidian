# 2D Prefix Sum

Related: [[2D Partial Sum]] (the inverse operation)

## 1D prefix sum (refresher)

Given an array `a[1..n]`, `p[i] = a[1] + a[2] + ... + a[i]` (sum of first i elements).

```C++
for (int i = 1; i <= n; i++)
    p[i] = p[i - 1] + a[i];
```

Subarray sum `a[l..r]` = `p[r] - p[l - 1]` in O(1).

2D prefix sum is the same idea extended to two dimensions — build once, query any rectangle in O(1).

## The problem it solves

You have a grid `a[n][m]` and **q queries**, each asking: *what is the sum of the rectangle from (r1,c1) to (r2,c2)?*

Brute force = O(n·m) per query → dies at q = 10^5.
2D prefix sum = **O(n·m) once to build, O(1) per query.**

Same trade as 1D: pay once up front, answer instantly forever after.

## The core idea

`P[i][j]` = **sum of every cell in the rectangle from (1,1) to (i,j)** — the whole top-left block, not just row i.

```
     j=1   2   3   4
i=1 [ * ][ * ][ * ][   ]
i=2 [ * ][ * ][ * ][   ]      P[3][3] = sum of all cells marked *
i=3 [ * ][ * ][ * ][   ]
i=4 [   ][   ][   ][   ]
```

## Building it — inclusion / exclusion

```C++
P[i][j] = a[i][j]
        + P[i-1][j]      // block above
        + P[i][j-1]      // block to the left
        - P[i-1][j-1];   // this corner got added TWICE -> remove one copy
```

Why the subtraction:

```
   P[i-1][j]  = A + B          A = the overlap block (top-left)
   P[i][j-1]  = A + C          B = rest of the block above
   ------------------          C = rest of the block to the left
   added:  2A + B + C          <-- A counted twice!
   fix:    - P[i-1][j-1] = -A

        j-1   j
       +---+---+
       | A | B |   <- i-1
       +---+---+
       | C | x |   <- i    (x = a[i][j], the new cell)
       +---+---+
```

**Always use a 1-indexed prefix array with row 0 and column 0 left as zeros.** That zero border is what makes `P[i-1][...]` safe when `i = 1` — no `if (i > 0)` guards anywhere. This is the single biggest source of clean 2D-prefix code.

```C++
const int N = 1005;
long long P[N][N];              // GLOBAL -> zero-initialised, and no stack overflow

int n, m;
cin >> n >> m;

for (int i = 1; i <= n; i++)
    for (int j = 1; j <= m; j++)
    {
        long long x;
        cin >> x;
        P[i][j] = x + P[i-1][j] + P[i][j-1] - P[i-1][j-1];
    }
```

Note there is no separate `a[][]` array — you can read straight into the prefix if you don't need the original grid.

### Alternative: row‑wise prefix first

You can also build row‑wise 1D prefixes first, then (optionally) collapse columns — useful when a problem only needs horizontal ranges per row:

```C++
int v[n + 1][m + 1], p[n + 1][m + 1] = {};

for (int i = 1; i <= n; i++)
    for (int j = 1; j <= m; j++)
        p[i][j] = v[i][j] + p[i][j - 1];       // prefix of row i only
```

Now `p[i][j]` = sum of `v[i][1..j]`. To get the full 2D prefix, add a second pass that goes column‑wise:

```C++
for (int j = 1; j <= m; j++)
    for (int i = 1; i <= n; i++)
        p[i][j] += p[i - 1][j];                 // now p is the full 2D prefix
```

The inclusion‑exclusion formula on line 31 does both passes in one, but the two‑pass approach is easier to reason about when debugging.

## Querying a rectangle — inclusion / exclusion again

Sum of rectangle with top-left `(r1,c1)` and bottom-right `(r2,c2)`, **inclusive, 1-indexed**:

```C++
long long rect(int r1, int c1, int r2, int c2)
{
    return P[r2][c2]
         - P[r1-1][c2]        // strip above
         - P[r2][c1-1]        // strip to the left
         + P[r1-1][c1-1];     // that strip corner was removed twice -> add back
}
```

Read the picture — `D` is the rectangle you want:

```
          c1        c2
        +----+-------+
        | A  |   B   |        P[r2][c2]      = A + B + C + D
   r1-1 +----+-------+        P[r1-1][c2]    = A + B
        | C  |   D   |        P[r2][c1-1]    = A + C
   r2   +----+-------+        P[r1-1][c1-1]  = A

   D = (A+B+C+D) - (A+B) - (A+C) + A
```

The `+ P[r1-1][c1-1]` is not a trick to memorise — you removed region `A` **twice** (once inside the strip above, once inside the strip to the left), so you owe it back once.

## The two conventions that cause WA

1. **Rows vs (x, y).** Problems often say "point (x, y)" where x is the *column*. Your array is `P[row][col]`. Decide once, write it in a comment, never mix. Most wrong answers on 2D prefix are this, not the formula.
2. **Inclusive bounds.** The formula above assumes `(r2,c2)` is *inside* the rectangle. If the statement gives a half-open range, convert at the input line, not inside the formula.

Sanity check every time: `rect(1,1,n,m)` must equal `P[n][m]`, and `rect(i,j,i,j)` must equal the original `a[i][j]`.

## Overflow

`n·m` cells of up to 10^9 each overflows `int` immediately. **Prefix arrays are `long long` by default.** This is a reflex, not a decision.

## Recognising it in a problem

- "sum of a subrectangle", "q queries on a grid"
- Counting on a grid: make a 0/1 grid (`1` if the cell is a wall / is black / satisfies P) → prefix sum now counts *how many* in any rectangle, in O(1). This is the most common contest use, more than plain sums.
- Fixed k×k square scanning: build the prefix, then slide a k×k window in O(n·m) — the 2D version of [[Sliding window Tips|fixed-size sliding window]].

Example — max sum k×k square:

```C++
long long best = LLONG_MIN;
for (int i = k; i <= n; i++)
    for (int j = k; j <= m; j++)
        best = max(best, rect(i-k+1, j-k+1, i, j));
```

## Full template

```C++
#include <bits/stdc++.h>
using namespace std;

const int N = 1005;
long long P[N][N];
int n, m;

long long rect(int r1, int c1, int r2, int c2)   // 1-indexed, inclusive
{
    return P[r2][c2] - P[r1-1][c2] - P[r2][c1-1] + P[r1-1][c1-1];
}

int main()
{
    ios::sync_with_stdio(0); cin.tie(0);

    cin >> n >> m;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++)
        {
            long long x; cin >> x;
            P[i][j] = x + P[i-1][j] + P[i][j-1] - P[i-1][j-1];
        }

    int q; cin >> q;
    while (q--)
    {
        int r1, c1, r2, c2;
        cin >> r1 >> c1 >> r2 >> c2;
        cout << rect(r1, c1, r2, c2) << "\n";
    }
}
```

## Practice

- CSES **Forest Queries** — the canonical one. Solve this first.
- CF Div3 problems tagged `dp` + `implementation` on grids — many are a 0/1 grid + prefix count.
- Then CSES **Forest Queries II** only if you later learn 2D BIT (point *update* + range query) — out of scope for now.

## Can I defend it?

Before you call this note "done", answer without looking:
1. Why is the `- P[i-1][j-1]` in the **build** there?
2. Why is the `+ P[r1-1][c1-1]` in the **query** a `+` and not a `-`?
3. What breaks if the prefix array is 0-indexed?
4. Why `long long`?
