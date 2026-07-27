# Two Pointers

Related: [[Sliding window Tips]] (the same-direction family) · [[Binary Search.2]] · [[Prefix Sum]]
## The three families

| Family | Movement | Prerequisite | Typical use |
|---|---|---|---|
| **Opposite direction** | `l→ ... ←r`, meet in the middle | array is **sorted** (or the problem is symmetric) | pair with sum X, palindrome, reverse, container-with-most-water |
| **Same direction** (sliding window) | `l` and `r` both →, `l` never passes `r` | window validity is **monotonic** | longest/shortest subarray, ≤ k distinct — see [[Sliding window Tips]] |
| **Two arrays** | one pointer per array | both **sorted** | merge, intersection, union |

All three are O(n) because **each pointer only ever moves forward** — total moves ≤ 2n. That's the entire reason the technique exists: it replaces a nested O(n²) loop.

## Family 1 — opposite direction

```
 arr sorted:   [ 2   3   5   8   11   15 ]
                 ^                     ^
                 l                     r

   sum = arr[l] + arr[r]
   sum too SMALL -> only way to grow it is l++   (r-- would shrink it further)
   sum too BIG   -> only way to shrink it is r--
   sum == target -> found
```

That is the whole insight, and it is worth saying out loud: **because the array is sorted, each comparison lets you throw away an entire row/column of the O(n²) search space** — you never need to reconsider the discarded pairs.

### Pair with a given sum

```C++
sort(a.begin(), a.end());

int l = 0, r = (int)a.size() - 1;
while (l < r)                          // '<' not '<=' : an element can't pair with itself
{
    long long sum = a[l] + a[r];       // long long: two 1e9 values overflow int
    if (sum == target) { /* found a[l], a[r] */ break; }
    else if (sum < target) l++;
    else                   r--;
}
```

Trace on `target = 13`:

```
[ 2  3  5  8  11  15 ]   l=0 r=5  sum=17 > 13  -> r--
  l               r
[ 2  3  5  8  11  15 ]   l=0 r=4  sum=13 == 13 -> FOUND (2, 11)
  l           r
```

> **If the problem wants the original indices, sort pairs `(value, index)`, not raw values.** Sorting destroys positions — this is the #1 two-pointer WA.
> ```C++
> vector<pair<int,int>> v;            // {value, original index}
> for (int i = 0; i < n; i++) v.push_back({a[i], i});
> sort(v.begin(), v.end());
> ```
> (If the problem does *not* need indices and the array isn't sorted, a hash map is often simpler — see the Two Sum template in [[Array & Hashing Mastery]]. Two pointers wins when the array is already sorted or you need *counting*, not one answer.)

### Counting pairs with sum ≤ X

This is the shape that shows up more often in contests than "find one pair":

```C++
int n,target;
cin>>n>>target;

vector<int> v(n);
for(int i = 0; i < n; i++)
{
	cin>>v[i];
}

sort(v.begin(), v.end());

int l = 0;
int r = n - 1;
long long cnt = 0;

while(l < r)
{
	if(v[l] + v[r] <= target)
	{
		cnt += (r - l);
		l++;
	}
	else
	{
		r--;
	}
}

cout<<cnt<<"\n";
return 0;
```

When v[l] + v[r] <= target, it means v[l] plus any element at positions l+1 through r (all ≤ v[r]) also sums to ≤ target. So we count all (r - l) pairs with the current v[l] at once, then move l inward — we're done with that smallest element.

### Palindrome check

```C++
int l = 0, r = s.size() - 1;
bool ok = true;
while (l < r)
{
    if (s[l] != s[r]) { ok = false; break; }
    l++; r--;
}
```

```
   a  b  c  b  a
   ^           ^     equal -> move both inward
      ^     ^        equal -> move both inward
         ^           l >= r -> done, it's a palindrome
```

### 3Sum = sort + fix one + two pointers

The standard escalation: an O(n³) problem becomes O(n²).

```C++
sort(a.begin(), a.end());
for (int i = 0; i < n - 2; i++)
{
    if (i > 0 && a[i] == a[i-1]) continue;      // skip duplicate first element
    int l = i + 1, r = n - 1;
    while (l < r)
    {
        long long sum = (long long)a[i] + a[l] + a[r];
        if (sum == 0)
        {
            // record triple (a[i], a[l], a[r])
            while (l < r && a[l] == a[l+1]) l++;   // skip duplicates
            while (l < r && a[r] == a[r-1]) r--;
            l++; r--;
        }
        else if (sum < 0) l++;
        else              r--;
    }
}
```

**Fix one element, two-point the rest** is a pattern you should recognise instantly.

## Family 3 — two arrays (merge)

One pointer per array, both only move forward:

```C++
int i = 0, j = 0;
vector<int> res;
while (i < n && j < m)
{
    if (a[i] <= b[j]) res.push_back(a[i++]);
    else              res.push_back(b[j++]);
}
while (i < n) res.push_back(a[i++]);      // drain the leftovers -- don't forget these
while (j < m) res.push_back(b[j++]);
```

```
   a: [1  4  7]        b: [2  3  9]
       i                   j
   1 <= 2 -> take 1, i++
   4 >  2 -> take 2, j++
   4 >  3 -> take 3, j++
   4 <= 9 -> take 4, i++   ...
   res: 1 2 3 4 7 9
```

Intersection is the same skeleton with `if (a[i] == b[j]) { record; i++; j++; }`.

## When it does NOT work

Two pointers is only valid when moving a pointer **can never make you miss a better answer**. Concretely:
- Opposite direction needs **sorted / monotonic** data. Unsorted → sort first (O(n log n)) or use a hash map instead.
- Same direction needs the window property to be **monotonic** (adding an element can only make the window "more invalid"). Sums with **negative numbers break this** — a longer window isn't necessarily a bigger sum, so sliding window fails and you need prefix sum + hash map instead (that's exactly the "subarray sum = x" solution in [[Sliding window Tips]]).

If you can't state *why* moving the pointer is safe, you don't have a two-pointer solution — you have a guess.

## Contest checklist

- [ ] `while (l < r)` or `while (l <= r)`? Decide from the problem: can one element be used twice?
- [ ] Sorted? If the problem needs original indices, sort `(value, index)` pairs.
- [ ] `long long` on any sum/product of two elements.
- [ ] Both pointers strictly move every iteration → no infinite loop. (Every `if` branch must contain an `l++` or an `r--`.)
- [ ] Duplicates: skip them, or count them deliberately.
- [ ] Empty / n = 1 input.

## Practice

- CSES **Sum of Two Values** (indices matter → the pair trick), **Sum of Three Values**, **Apartments**, **Ferris Wheel** — this is the best two-pointer set that exists at your level, do these four.
- Your bookmarks already touch this: [[Shift Zeros]], [[Renting bikes]], [[Counting Arthimetic Sequence]] (from the "Adhocs & Two Pointers" sheet) — re-solve them consciously naming which family you're using.
- LeetCode: Container With Most Water (the "why is it safe to move the shorter side?" proof is worth 10 minutes of thinking on paper).

## Can I defend it?

1. Why is the whole technique O(n) and not O(n²)?
2. Why does opposite-direction require a sorted array — what breaks without it?
3. In the "count pairs ≤ X" code, why `cnt += (r - l)` and not `cnt++`?
4. Why does sliding window break when the array contains negative numbers?
5. When would you use a hash map instead of two pointers for a pair-sum problem?
