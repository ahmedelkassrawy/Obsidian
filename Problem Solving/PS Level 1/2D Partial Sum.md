# 2D Partial Sum (2D Difference Array)

Related: [[1D Partial Sum]] (read that first) · [[2D Prefix Sum]] (needed for the rebuild)

> Same naming warning as [[1D Partial Sum]]: if your sheet says "2D partial sum" meaning *2D prefix sum*, go to [[2D Prefix Sum]]. This note is the **range-update** version.

## The problem it solves

*"You have an n×m grid of zeros. Apply q operations, each adding `v` to every cell of a subrectangle. Print the final grid."*

Naive = O(n·m) per operation. Dead at q = 10^5.
2D difference array = **O(1) per update, one O(n·m) rebuild at the end.**

## The core idea — 4 corners instead of 2

In 1D you turned a tap on at `l` and off at `r+1` — 2 cells.
In 2D, "turn on at a corner" leaks into the whole quadrant below-right of it, so you need **4 cells** to carve out exactly one rectangle:

```C++
d[r1][c1] += v;  // turn ON  the whole quadrant from (r1,c1) down-right
d[r1][c2+1] -= v;  // cancel everything to the RIGHT of the rectangle
d[r2+1][c1] -= v;   // cancel everything BELOW the rectangle
d[r2+1][c2+1] += v; // that bottom-right corner got cancelled TWICE -> add it back
```

It is the **same inclusion–exclusion as [[2D Prefix Sum]]**, just applied to the update instead of the query. Same four terms, same signs (`+ - - +`).

## Watch it happen

5×5 grid, apply `+1` to the rectangle `(2,2)` → `(4,3)`:

```
d after the 4 writes:                the 4 marks:
      c=1  2  3  4  5  (6)
r=1  [ 0  0  0  0  0 ] 0
r=2  [ 0 +1  0 -1  0 ] 0             (r1,c1)=+1   (r1,c2+1)=-1
r=3  [ 0  0  0  0  0 ] 0
r=4  [ 0  0  0  0  0 ] 0
r=5  [ 0 -1  0 +1  0 ] 0             (r2+1,c1)=-1 (r2+1,c2+1)=+1
(6)    0  0  0  0  0   0
```

Now take a **2D prefix sum over d** — that rebuilds the grid:

```
      c=1  2  3  4  5
r=1  [ 0  0  0  0  0 ]
r=2  [ 0  1  1  0  0 ]      <- exactly the rectangle (2,2)-(4,3)
r=3  [ 0  1  1  0  0 ]
r=4  [ 0  1  1  0  0 ]
r=5  [ 0  0  0  0  0 ]
```

Why each mark is needed — trace what `+v` at `(r1,c1)` alone would do:

```
   +v at (r1,c1) alone fills the whole quadrant:

        c1      c2
      +----+-------+--------
   r1 |####|#######|########
      |####|#######|########   <- everything right of c2 is wrong
   r2 |####|#######|########
      +----+-------+--------
      |####|#######|########   <- everything below r2 is wrong
      |####|#######|########

   -v at (r1,c2+1)  kills the right strip
   -v at (r2+1,c1)  kills the bottom strip
   the bottom-RIGHT block got killed by BOTH -> +v at (r2+1,c2+1) restores it once
```

That last `+v` is the exact same "you subtracted the overlap twice, pay it back once" move as the query formula in [[2D Prefix Sum]]. If you understand one, you understand both.

## Template

```C++
#include <bits/stdc++.h>
using namespace std;

const int N = 1005;
long long d[N][N];              // global -> zeroed; size must be >= n+2 and m+2
int n, m, q;

int main()
{
    ios::sync_with_stdio(0); cin.tie(0);
    cin >> n >> m >> q;

    while (q--)
    {
        int r1, c1, r2, c2; long long v;
        cin >> r1 >> c1 >> r2 >> c2 >> v;

        d[r1  ][c1  ] += v;
        d[r1  ][c2+1] -= v;
        d[r2+1][c1  ] -= v;
        d[r2+1][c2+1] += v;
    }

    // rebuild: 2D prefix sum in place
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++)
        {
            d[i][j] += d[i-1][j] + d[i][j-1] - d[i-1][j-1];
            cout << d[i][j] << " \n"[j == m];
        }
}
```

Non-negotiables (all inherited from the 1D version):
1. **Dimensions `n+2` × `m+2`** — updates touch `r2+1` and `c2+1`, which can be `n+1` / `m+1`.
2. **1-indexed** — the rebuild reads `d[i-1][j-1]`, so row 0 and column 0 must exist and stay zero.
3. **`long long`.**

The rebuild is *literally* the 2D prefix-sum build, done in place. Write it once, reuse the same three lines.

## Recognising it in a problem

- "paint / stamp a rectangle, many times, then print the grid"
- Counting how many rectangles cover each cell (`v = 1`) → then max coverage, or count of cells covered ≥ k
- Grid problems where q is large but you only need the **final** state — never when updates and queries interleave

## The whole family in one table

|                       | Range **query**, fixed array | Range **update**, read once |
|-----------------------|------------------------------|------------------------------|
| 1D                    | [[Prefix Sum]]               | [[1D Partial Sum]] — 2 cells |
| 2D                    | [[2D Prefix Sum]] — 4 terms  | **this note** — 4 cells      |

Four notes, one idea: *inclusion–exclusion on corners.* The 2D versions cost 4 terms because a rectangle has 4 corners.

## Practice

- CF Div3 "stamp the rectangle" problems (tags: `implementation`, `dp`).
- Build one yourself: random 200×200 grid + 1000 random rectangle updates, compare against the naive O(n·m·q) loop. **Write this brute-force checker** — it takes 5 minutes and catches every off-by-one you'll ever make in this technique.

## Can I defend it?

1. Why 4 cells in 2D when 1D needed only 2?
2. Why is the 4th write a `+` and not a `-`?
3. Why is the rebuild the same code as the 2D prefix-sum build — what does that say about the two techniques?
4. What must the array dimensions be, and what goes wrong at exactly `r2 = n`?
