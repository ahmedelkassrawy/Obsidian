# 1D Partial Sum (Difference Array)

Related: [[Prefix Sum]] · [[2D Partial Sum]]

> ⚠️ **Naming warning.** In a lot of Arabic CP material (Assiut / ICPC sheets), *"partial sum"* is used as a **synonym for prefix sum**. If your sheet uses it that way, the note you want is [[Prefix Sum]].
> This note covers the *other* meaning — the **difference array** (also called *imos technique* / *range update trick*), which is the **inverse** of prefix sum. Check which one your sheet means before drilling.

## Prefix sum vs difference array — the mirror

|                    | Prefix sum            | Difference array          |
|--------------------|-----------------------|---------------------------|
| Fast operation     | **range query** O(1)  | **range update** O(1)     |
| Slow operation     | update = rebuild O(n) | query = rebuild O(n)      |
| Use when           | array is fixed, many queries | many updates, then read the array **once** at the end |

They are inverses: **prefix sum of a difference array gives back the original array.**

## The problem it solves

*"You have an array of n zeros. Apply q operations, each adding `v` to every element in `[l, r]`. Print the final array."*

Naive = O(n) per operation → 10^5 × 10^5 = 10^10 operations. Dead.
Difference array = **O(1) per update, O(n) once at the end.**

## The core idea

Store not the values, but the **change between neighbours**:

```
d[i] = a[i] - a[i-1]
```

Then `a` is recovered by a running sum of `d`:

```
a[i] = d[1] + d[2] + ... + d[i]     // i.e. prefix sum of d
```

Now the key insight — to add `v` to the whole range `[l, r]`, you only need to touch **two** positions:

```C++
d[l]   += v;     // from index l onwards, everything is v higher
d[r+1] -= v;     // from index r+1 onwards, cancel it back out
```

Everything strictly between `l` and `r` has an *unchanged* difference with its neighbour, so it needs no work at all. That's why it's O(1).

## Watch it happen

`n = 8`, apply `+5` on `[3, 6]`:

```
index:   1   2   3   4   5   6   7   8   (9)
d:       0   0  +5   0   0   0  -5   0    0
                 ^                  ^
                 |                  |
              d[l]+=5           d[r+1]-=5

running sum (this IS the final array):
a:       0   0   5   5   5   5   0   0
                 |---- the range ----|
```

The running sum "switches on" at `l` and "switches off" at `r+1`. Think of `d[l] += v` as *turn the tap on* and `d[r+1] -= v` as *turn it off*.

Two overlapping updates just stack:

```
apply +5 on [3,6], then +3 on [5,8]:

index:   1   2   3   4   5   6   7   8  (9)
d:       0   0  +5   0  +3   0  -5   0   -3
a:       0   0   5   5   8   8   3   3
                 |--+5--|
                         |----+3-----|
```

## Template

```C++
int n, q;
cin >> n >> q;

vector<long long> d(n + 2, 0);      // size n+2 !! so d[r+1] is safe when r == n

while (q--)
{
    int l, r; long long v;
    cin >> l >> r >> v;
    d[l]   += v;
    d[r+1] -= v;                    // needs index n+1 to exist
}

// rebuild the array with a running (prefix) sum
for (int i = 1; i <= n; i++)
{
    d[i] += d[i-1];
    cout << d[i] << " \n"[i == n];
}
```

Three things that are not optional:
1. **`n + 2`, not `n + 1`.** If an update ends at `r = n`, you write to `d[n+1]`. Sizing it `n+1` is an out-of-bounds write that often *doesn't* crash — it silently corrupts. Classic invisible WA/RE.
2. **1-indexed.** With `l = 1` you'd need `d[0]`, so start at 1 and keep index 0 free.
3. **`long long`.** q updates of up to 10^9 stack up fast.

## Starting from a non-zero array

If the array isn't all zeros, build `d` from it first, then do the updates:

```C++
for (int i = 1; i <= n; i++) d[i] = a[i] - a[i-1];   // a[0] = 0
```

## Recognising it in a problem

- "add v to all elements in range [l,r]", repeated many times, **output at the end**
- **Event / interval counting:** "n intervals, how many cover each point?" → `+1` at start, `-1` at end+1, prefix sum. Very common in Div3.
- "how many people are in the room at time t" / booking-overlap problems → same thing on a timeline.
- Max overlap of intervals = the max value of the rebuilt array.

Interval counting looks like this:

```C++
for each interval [s, e]:
    d[s]++, d[e+1]--;

prefix sum -> d[i] = how many intervals cover point i
answer     = *max_element(d.begin()+1, d.begin()+n+1);
```

If coordinates are huge (up to 10^9) you can't index an array that big — you'd need coordinate compression or a sorted `(point, ±1)` event sweep. Same idea, different container.

## The mental one-liner

> **Prefix sum answers ranges. Difference array updates ranges. Each is the other run backwards.**

## Practice

- CSES **Room Allocation** / **Restaurant Customers** — pure event counting, exactly this technique.
- CF Div3: any "add to range, print final array" problem.
- Then compare: solve one of them the O(n·q) way first and watch it TLE — feeling the limit is worth more than reading it.

## Can I defend it?

1. Why does touching only two cells update a whole range?
2. Why must the array have size `n+2`?
3. What operation converts `d` back into `a` — and what does that tell you about the relationship to [[Prefix Sum]]?
4. Why is a difference array *useless* if the problem interleaves updates and queries?
