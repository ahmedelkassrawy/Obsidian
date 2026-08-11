---
tags: [problem-solving, reference, ecpc, contest]
topic: ECPC Reference Sheet
description: Printable one-file reference for the contest — concept, when-to-use, and code for every Level-1 technique
---

# ECPC Reference Sheet

Print settings: A4, portrait, margins 10mm, **scale 80%**. Code blocks are kept compact on purpose so nothing wraps in print.
Built from `PS Level 1` + `C++ Notes` + `Bookmarks`.

**How to read this sheet:** every block has three parts — *Concept* (what it actually does), *When to use* (the signal in the problem statement that should make you reach for it), and the code.

**Don't read it front to back — jump.** Start at §13 (the statement → technique table), then go to the section it names.

| § | Section | § | Section |
|---|---|---|---|
| 0 | Template + complexity budget | 7 | Bit manipulation & bitmask |
| 1 | STL | 8 | Strings |
| 2 | Sorting | 9 | Math & number theory |
| 3 | Binary search | 10 | Dynamic programming |
| 4 | Two pointers & sliding window | 11 | Graphs |
| 5 | Prefix sums & difference arrays | 12 | Contest checklist (WA/TLE/RE) |
| 6 | Recursion & backtracking | **13** | **"Which technique?" — start here** |

---

## 0. Template + budget

```cpp
#include <bits/stdc++.h>
using namespace std;
#define ll long long
#define all(v) v.begin(), v.end()

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int t = 1;
    // cin >> t;
    while (t--) solve();
    return 0;
}
```

If `bits/stdc++.h` is missing on the judge:

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <set>
#include <queue>
#include <stack>
#include <algorithm>
#include <numeric>
#include <cmath>
#include <climits>
```

**Read the constraints before you think about the algorithm — they tell you which complexity is intended.** ~10^8 simple ops/second.

| n up to | What fits | So think… |
|---|---|---|
| 10 – 12 | `O(n!)` | permutations, brute force every order |
| 20 – 24 | `O(2^n)` / `O(2^n · n)` | bitmask subsets |
| 500 | `O(n^3)` | triple loop, Floyd–Warshall |
| 5·10^3 | `O(n^2)` | double loop, classic 2D DP |
| 10^5 – 10^6 | `O(n log n)` | sort, binary search, set/map, heap |
| 10^7 – 10^8 | `O(n)` | one pass — prefix sum, two pointers, greedy |

**Value limits**

| Type | Max |
|---|---|
| `int` | ~2.1·10^9 |
| `long long` | ~9.2·10^18 |
| `unsigned long long` | ~1.8·10^19 |

Constants: `const ll INF = 1e18;` `const int inf = 1e9;` `const ll MOD = 1e9 + 7;`

```cpp
cout << fixed << setprecision(2) << x;   // needs <iomanip>
cout << "\n";                            // never endl in loops (flushes)
```

---

## 1. STL

**Concept.** Ready-made data structures. The whole skill is picking the one whose *cost profile* matches what the problem does most often.

**When to use.** Always. Choosing right is usually the difference between AC and TLE.

### 1.1 Which container?

| Need | Container | Access | Ordered? |
|---|---|---|---|
| Dynamic array | `vector<T>` | O(1) index | insertion order |
| Sorted unique keys | `set<T>` | O(log n) | yes |
| Sorted with duplicates | `multiset<T>` | O(log n) | yes |
| Key → value, sorted | `map<K,V>` | O(log n) | yes |
| Key → value, fastest | `unordered_map<K,V>` | O(1) avg | no |
| FIFO (BFS) | `queue<T>` | O(1) | — |
| LIFO (DFS) | `stack<T>` | O(1) | — |
| Always-max / always-min | `priority_queue<T>` | O(log n) push/pop | — |
| Both ends | `deque<T>` | O(1) both ends | — |

Rule of thumb: **`vector` unless you need something a `vector` can't do.** If keys are small integers (`≤ 10^6`), a plain array beats any map.

### 1.2 vector

**Concept.** A resizable array — contiguous memory, so indexing is free and iteration is cache-friendly.

**When to use.** The default container. Insert/erase in the *middle* is O(n), so if you need that a lot, rethink.

```cpp
vector<int> v(n);              // n zeros
vector<int> v(n, -1);          // n copies of -1
vector<vector<int>> g(n);      // n empty lists (adjacency list)
vector<vector<ll>> dp(n + 1, vector<ll>(m + 1, 0));   // 2D

v.push_back(x); v.pop_back();
v.size(); v.empty(); v.clear();
v.back(); v.front();
v.resize(k); v.assign(n, 0);
reverse(all(v));
v.erase(v.begin() + i);                // O(n)
v.erase(unique(all(v)), v.end());      // dedupe AFTER sorting
```

### 1.3 map / set

**Concept.** Balanced BSTs — every operation O(log n) and the contents stay **sorted**. `unordered_*` are hash tables: O(1) average but no order.

**When to use.** `map` when you need counting/lookup by a key that isn't a small int (strings, big values, pairs). `set` when you need "is it there?" *plus* "what's the smallest/next bigger?". If you only need counting and keys are small, use a frequency `vector` instead — it's much faster.

```cpp
map<char,int> freq;
for (char c : s) freq[c]++;            // missing key auto-creates 0
for (auto &p : freq) cout << p.first << " " << p.second << "\n";

if (freq.count(c)) ...                 // exists?
if (mp.find(x) != mp.end()) ...        // same thing
mp.erase(key);

set<int> s;
s.insert(x); s.erase(x);
*s.begin();                            // smallest
*s.rbegin();                           // largest
auto it = s.lower_bound(x);            // MEMBER version — O(log n)
```

> On a `set` / `map` always use the **member** `s.lower_bound(x)`, never `lower_bound(s.begin(), s.end(), x)` — the free function is O(n) on a tree.

```cpp
ms.erase(x);                  // erases ALL copies of x
ms.erase(ms.find(x));         // erases exactly ONE copy   <-- usually what you want
```

### 1.4 priority_queue

**Concept.** A heap — you can always see and remove the current best element in O(log n), but you can't look at anything else.

**When to use.** "Repeatedly take the largest/smallest remaining" — greedy scheduling, merging k lists, Dijkstra, "join the two cheapest ropes".

```cpp
priority_queue<int> pq;                                     // MAX-heap
priority_queue<int, vector<int>, greater<int>> mn;           // MIN-heap
priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<>> d;  // Dijkstra

pq.push(x); pq.top(); pq.pop(); pq.empty(); pq.size();
```

Pairs sort by `.first`, then `.second`. Cheap min-heap trick: push `-x` into a max-heap.

### 1.5 pair / tuple

**Concept.** Glue 2–3 values into one comparable object; comparison is lexicographic (first, then second).

**When to use.** Sorting by one field while carrying another (value+index), edges `{weight, node}`, grid cells `{row, col}`.

```cpp
pair<int,int> p = {a, b};
p.first; p.second;
vector<pair<int,int>> v;
v.push_back({val, idx});

tuple<int,int,int> t = {a, b, c};
auto [x, y, z] = t;            // C++17 structured binding
```

### 1.6 Algorithms

**Concept.** One-line library versions of loops you'd otherwise write by hand (and get wrong).

**When to use.** Before writing any loop, ask whether `<algorithm>` already has it.

```cpp
sort(all(v));
sort(v.rbegin(), v.rend());               // descending
reverse(all(v));
*max_element(all(v));  *min_element(all(v));
max_element(all(v)) - v.begin();          // INDEX of the max
accumulate(all(v), 0LL);                  // 0LL !! or it overflows
count(all(v), x);
find(all(v), x) != v.end();
next_permutation(all(v));                 // sort first; loops all n! orders
__gcd(a, b);  swap(a, b);
min({a,b,c});  max({a,b,c});
fill(all(v), 0);
memset(arr, 0, sizeof arr);               // only for 0 and -1
```

### 1.7 String

**Concept.** A `vector<char>` with text helpers — everything vector can do, plus `substr`/`find`.

**When to use.** Anything character-based. `s[i] - 'a'` turns a letter into a 0..25 index for frequency arrays.

```cpp
string s; cin >> s;                 // stops at whitespace
getline(cin, s);                    // whole line — after cin>>n do cin.ignore()

s.size(); s.substr(i, len); s + t; s.push_back(c);
s.find("ab");                       // returns string::npos if absent
sort(all(s));                       // anagram signature
to_string(n); stoi(s); stoll(s);
isalpha(c); isdigit(c); tolower(c); toupper(c);
s[i] - 'a';                         // 0..25 index
```

---

## 2. Sorting

**Concept.** Rearranging data into an order that makes the answer obvious. Sorting itself is O(n log n) — the *point* is that a sorted array unlocks binary search, two pointers, and greedy.

**When to use.** When the answer depends on relative order, ranks, "k-th smallest", pairing extremes, or when you're about to binary-search / two-point. Also: **sorting is a legitimate first move even when the problem never mentions order.**

### 2.1 Comparators

**Concept.** You tell `sort` what "comes first" means.

**When to use.** Multi-field ordering — "by score descending, ties by name ascending".

```cpp
bool cmp(const pair<int,int> &a, const pair<int,int> &b) {
    if (a.first != b.first) return a.first < b.first;   // asc by first
    return a.second > b.second;                          // tie: desc by second
}
sort(all(v), cmp);

sort(all(v), [](auto &a, auto &b) { return a.second < b.second; });  // lambda
```

Returns **true when `a` must come before `b`**. Must be a strict weak order — never `<=`, that crashes.

### 2.2 Sorting structs

**Concept.** Bundle related fields, sort the bundle.

**When to use.** Each input line describes an object with several attributes (dragon: strength+bonus; person: x+y; interval: start+end).

```cpp
struct Dragon { int strength; int bonus; };

bool compare(const Dragon &a, const Dragon &b) { return a.strength < b.strength; }

vector<Dragon> d(n);
for (int i = 0; i < n; i++) cin >> d[i].strength >> d[i].bonus;
sort(all(d), compare);

struct P { int x, y;
    bool operator<(const P &o) const { return x < o.x; } };   // or inside
```

### 2.3 Keeping the original index

**Concept.** Sorting destroys positions, so carry the position along as part of the element.

**When to use.** The output asks for *indices* ("print the 1-based positions of the two numbers"). This is the #1 sorting WA.

```cpp
vector<pair<int,int>> v;
for (int i = 0; i < n; i++) v.push_back({a[i], i});
sort(all(v));                          // v[k].second is the original index
```

### 2.4 Counting sort / frequency array

**Concept.** Don't compare anything — just tally how many times each value appears, then read the tally in order. O(n + V).

**When to use.** Values are bounded and small (`≤ 10^6`), n is huge, or you need "how many of value x" repeatedly.

```cpp
vector<int> freq(MAXV + 1, 0);
for (int x : a) freq[x]++;
for (int x = 0; x <= MAXV; x++)
    while (freq[x]--) cout << x << " ";
```

---

## 3. Binary search

**Concept.** Every step throws away **half** the remaining possibilities, so 10^6 items take ~20 steps. It works only because the data is **monotonic**: once you know which side the answer is on, the other side can never contain it.

**When to use.** (1) Searching a **sorted array**. (2) The answer is a number in a known range and you can *check* a guess faster than you can *find* the answer — that's §3.4, and it is the single highest-value trick on this sheet.

### 3.1 Does `x` exist?

**When to use.** Plain membership on a sorted array. (In contest: `binary_search(all(v), x)`.)

```cpp
int l = 0, r = n - 1, ans = -1;
while (l <= r) {
    int mid = l + (r - l) / 2;        // overflow-safe
    if (a[mid] == x)      { ans = mid; break; }
    else if (a[mid] < x)  l = mid + 1;
    else                  r = mid - 1;
}
```

`l <= r` (not `<`) — when `l == r` the window still holds one element to check.

### 3.2 Lower / upper bound by hand

**Concept.** Don't stop at a match — record it and keep shrinking left, so you land on the *first* valid position.

**When to use.** Duplicates exist, or `x` may be absent and you want the insertion point.

```cpp
// first index with a[i] >= x
int l = 0, r = n - 1, ans = n;        // ans = n means "no such element"
while (l <= r) {
    int mid = l + (r - l) / 2;
    if (a[mid] >= x) { ans = mid; r = mid - 1; }   // valid — but look left for earlier
    else               l = mid + 1;
}
```

Upper bound = the same code with `a[mid] > x`. Initialise `ans = n`, **not 0** — with `0` you can't tell "not found" from "found at index 0".

### 3.3 STL version (use this in contest)

```cpp
auto it = lower_bound(all(v), x);          // first >= x
auto it = upper_bound(all(v), x);          // first  > x
int idx = it - v.begin();                  // iterator -> index
if (it == v.end()) /* nothing found */;

int cntX  = upper_bound(all(v),x) - lower_bound(all(v),x);        // copies of x
int inRange = upper_bound(all(v),R) - lower_bound(all(v),L);      // count in [L,R]
```

| Question | Tool |
|---|---|
| Does `x` exist? | `binary_search(all(v),x)` |
| First index `>= x` | `lower_bound` |
| First index `> x` | `upper_bound` |
| How many `x` | `upper_bound - lower_bound` |
| How many in `[L,R]` | `upper_bound(R) - lower_bound(L)` |

### 3.4 Binary search on the ANSWER ⭐

**Concept.** Stop searching *an array* and start searching *the range of possible answers*. If `check(X)` is monotonic — false, false, …, false, **true**, true, … — you can binary-search the boundary.

**When to use.** The statement says **"minimum X such that…"**, **"maximum X such that…"**, "minimum time/capacity/size that suffices", "maximise the minimum distance". Test for monotonicity out loud: *if X works, does X+1 automatically work?* If yes → binary search.

```cpp
bool check(ll mid) { /* is mid feasible? */ }

ll l = 1, r = 1e18, ans = -1;
while (l <= r) {
    ll mid = l + (r - l) / 2;
    if (check(mid)) { ans = mid; r = mid - 1; }   // MINIMISE: keep it, shrink right
    else              l = mid + 1;
}
```

To **maximise**, flip: on success `ans = mid; l = mid + 1;`.

Real form — *Machines*: can we make ≥ k items in t seconds?

```cpp
bool check(ll t) {
    ll made = 0;
    for (int i = 0; i < n; i++) {
        made += t / a[i];
        if (made >= k) return true;    // early exit also avoids overflow
    }
    return made >= k;
}
```

Floating-point version: fixed 100 iterations instead of `l <= r`.

```cpp
double l = 0, r = 1e9;
for (int i = 0; i < 100; i++) {
    double mid = (l + r) / 2;
    if (check(mid)) r = mid; else l = mid;
}
```

Total cost = O(log(range) · cost of `check`).

---

## 4. Two pointers & sliding window

**Concept.** Replace a nested O(n²) scan with two indices that each only ever move **forward** — total movement ≤ 2n, hence O(n). It's valid only when moving a pointer can never make you miss a better answer.

**When to use.** Subarrays/substrings (contiguous!), pairs in a sorted array, merging sorted data. **If you can't say *why* moving the pointer is safe, you don't have a two-pointer solution — you have a guess.**

### 4.1 The three families

| Family | Movement | Needs | Typical use |
|---|---|---|---|
| Opposite | `l→ ... ←r` | sorted / symmetric | pair with sum X, palindrome, most water |
| Same direction (window) | both → | validity monotonic | longest/shortest subarray, ≤k distinct |
| Two arrays | one pointer each | both sorted | merge, intersection, union |

### 4.2 Pair with a given sum

**Concept.** Sorted array: too small → the only way to grow the sum is `l++`; too big → the only way to shrink it is `r--`. Each comparison discards a whole row of the O(n²) grid.

**When to use.** "Do two numbers add up to X?" on sorted data (or when you may sort). If the array is unsorted *and* you need indices, a hash map is simpler.

```cpp
sort(all(a));
int l = 0, r = n - 1;
while (l < r) {                       // '<' : an element can't pair with itself
    ll sum = a[l] + a[r];             // ll — two 1e9 values overflow int
    if (sum == target) break;
    else if (sum < target) l++;
    else                   r--;
}
```

### 4.3 Count pairs with sum ≤ X

**Concept.** If the smallest + largest already fits, then that smallest fits with **everything** between them — count `r - l` pairs in one shot.

**When to use.** "How many pairs satisfy …" — counting, not finding. This shape appears in contests more than "find one pair".

```cpp
sort(all(v));
int l = 0, r = n - 1; ll cnt = 0;
while (l < r) {
    if (v[l] + v[r] <= target) { cnt += (r - l); l++; }
    else r--;
}
```

### 4.4 3Sum — fix one, two-point the rest

**Concept.** Freeze one element, and the remaining problem is a 2-sum on a sorted array. O(n³) → O(n²).

**When to use.** Any "find k numbers with property P" for small k. Recognise **fix-one-then-two-point** instantly.

```cpp
sort(all(a));
for (int i = 0; i < n - 2; i++) {
    if (i > 0 && a[i] == a[i-1]) continue;      // skip duplicate anchors
    int l = i + 1, r = n - 1;
    while (l < r) {
        ll sum = a[i] + a[l] + a[r];
        if (sum == 0) {
            // record a[i], a[l], a[r]
            while (l < r && a[l] == a[l+1]) l++;
            while (l < r && a[r] == a[r-1]) r--;
            l++; r--;
        }
        else if (sum < 0) l++;
        else              r--;
    }
}
```

### 4.5 Palindrome / reverse

**Concept.** Symmetric structure — compare the ends, walk inward.

**When to use.** Palindrome checks, reversing in place, "is the sequence symmetric".

```cpp
int l = 0, r = s.size() - 1;
bool ok = true;
while (l < r) {
    if (s[l] != s[r]) { ok = false; break; }
    l++; r--;
}
```

### 4.6 Merge two sorted arrays

**Concept.** Whichever front element is smaller must come next — no comparison is ever wasted.

**When to use.** Merging, intersection, union, "combine two sorted lists". Same skeleton with `a[i] == b[j]` gives intersection.

```cpp
int i = 0, j = 0; vector<int> res;
while (i < n && j < m) {
    if (a[i] <= b[j]) res.push_back(a[i++]);
    else              res.push_back(b[j++]);
}
while (i < n) res.push_back(a[i++]);    // drain leftovers — don't forget
while (j < m) res.push_back(b[j++]);
```

### 4.7 Fixed-size window (size k)

**Concept.** Move the window one step: add the entering element, subtract the leaving one. O(1) per step instead of O(k).

**When to use.** "Every contiguous block of exactly k elements" — max sum of k consecutive, average of k days.

```cpp
ll sum = 0, best = LLONG_MIN;
for (int i = 0; i < n; i++) {
    sum += a[i];
    if (i >= k) sum -= a[i - k];       // slide: drop the element leaving
    if (i >= k - 1) best = max(best, sum);
}
```

### 4.8 Variable window — the universal skeleton

**Concept.** `r` expands greedily; the moment the window breaks the rule, `l` shrinks until it's legal again. Every index enters and leaves once → O(n).

**When to use.** "Longest / shortest **contiguous** subarray such that …" — at most k distinct, no repeats, sum ≤ S. **Requires all-positive values** (see 4.9).

```cpp
int l = 0; ll cur = 0; int best = 0;
for (int r = 0; r < n; r++) {
    cur += a[r];                       // 1. add the new right element
    while (/* window is INVALID */) {  // 2. shrink from the left until valid
        cur -= a[l];
        l++;
    }
    best = max(best, r - l + 1);       // 3. record
}
```

Longest substring with no repeats:

```cpp
map<char,int> cnt; int l = 0, best = 0;
for (int r = 0; r < (int)s.size(); r++) {
    cnt[s[r]]++;
    while (cnt[s[r]] > 1) { cnt[s[l]]--; l++; }
    best = max(best, r - l + 1);
}
```

### 4.9 When sliding window FAILS

**Concept.** The window relies on "growing can only make things worse". **Negative numbers destroy that** — a longer window isn't necessarily a bigger sum. Then you need prefix sums keyed in a hash map: `sum(l..r) = pre[r] - pre[l-1]`, so for each `r` you ask how many earlier prefixes equal `pre[r] - x`.

**When to use this instead.** Array contains negatives, or the target is an exact value/divisibility rather than a bound.

```cpp
// count subarrays with sum == x  (works with negatives)
map<ll,ll> seen;  seen[0] = 1;
ll pre = 0, ans = 0;
for (int i = 0; i < n; i++) {
    pre += a[i];
    ans += seen[pre - x];
    seen[pre]++;
}
```

Divisible by k → same idea keyed on `((pre % k) + k) % k`.

---

## 5. Prefix sums & difference arrays

**Concept.** Two mirror-image tricks. **Prefix sum** = precompute once, answer any range *query* in O(1). **Difference array** = record only the *edges* of each range update, then one final sweep materialises the array.

**When to use.** Prefix sum: many range-sum questions on a fixed array. Difference array: many "add v to everything in [l,r]" updates, and you only print at the end. If updates and queries are **interleaved**, you need a Fenwick/segment tree (Level 2).

### 5.1 1D prefix sum

**When to use.** q queries × O(n) each is too slow → precompute in O(n), answer in O(1).

```cpp
vector<ll> pre(n + 1, 0);
for (int i = 1; i <= n; i++) pre[i] = pre[i-1] + a[i];   // a is 1-indexed
ll s = pre[r] - pre[l-1];                                 // sum of a[l..r]
```

### 5.2 1D difference array

**Concept.** `+val` at `l` turns the addition on, `-val` at `r+1` turns it off; prefix-summing replays every switch.

**When to use.** "m operations, each adds v to range [l,r]; print the final array." O(1) per update instead of O(n).

```cpp
vector<ll> diff(n + 2, 0);
diff[l] += val;                        // per update "add val to [l, r]"
diff[r + 1] -= val;

ll run = 0;                            // materialise the final array
for (int i = 1; i <= n; i++) { run += diff[i]; a[i] = run; }
```

### 5.3 2D prefix sum

**Concept.** Inclusion–exclusion: add the two overlapping rectangles, subtract the part you counted twice.

**When to use.** Many "sum of this sub-rectangle" queries on a fixed grid.

```cpp
for (int i = 1; i <= n; i++)
  for (int j = 1; j <= m; j++)
    pre[i][j] = g[i][j] + pre[i-1][j] + pre[i][j-1] - pre[i-1][j-1];

ll s = pre[r2][c2] - pre[r1-1][c2] - pre[r2][c1-1] + pre[r1-1][c1-1];
```

### 5.4 2D difference array

**When to use.** Many "add v to this sub-rectangle" updates, print the grid at the end. Same idea as 1D but 4 corners.

```cpp
d[r1][c1]     += val;
d[r1][c2+1]   -= val;
d[r2+1][c1]   -= val;
d[r2+1][c2+1] += val;
// then 2D prefix-sum d in place to get the final grid
```

| | Query | Update |
|---|---|---|
| 1D | prefix sum (2 corners) | difference array (2 corners) |
| 2D | prefix sum (4 corners) | difference array (4 corners) |

---

## 6. Recursion & backtracking

**Concept.** Solve a problem by solving a smaller copy of itself. **Backtracking** adds one move: try a choice → recurse → **undo it** → try the next. That undo is what lets one array explore an entire decision tree.

**When to use.** The answer is built from a sequence of choices and you must try them all: subsets, permutations, placements, "count the ways", grid paths with constraints. **Only when n is tiny** — 2^n needs n ≤ ~24, n! needs n ≤ ~10.

Every recursion needs: **(1) a base case, (2) a step that shrinks the problem.**

### 6.1 Print before vs after the call

**Concept.** Work placed *before* the call happens on the way down; *after* the call it happens on the way back up (reverse order, for free).

**When to use.** Any "print/process in reverse" — and it's the mental model behind DFS post-order.

```cpp
void down(int n) { if (n == 0) return; cout << n << " "; down(n-1); }  // 5 4 3 2 1
void up(int n)   { if (n == 0) return; up(n-1); cout << n << " "; }    // 1 2 3 4 5
```

### 6.2 Accumulate on return

**When to use.** The answer for `n` is a simple function of the answer for `n-1`.

```cpp
ll sum(int n) { return n == 0 ? 0 : n + sum(n - 1); }
```

### 6.3 Memoized recursion (top-down DP)

**Concept.** The recursion revisits the same state many times; store each result the first time and the exponential tree collapses to one node per state.

**When to use.** Plain recursion is correct but too slow, and the state is small (an index, a remaining capacity). **This is the easiest way to write a DP** — get the recursion right, then add the memo.

```cpp
vector<ll> memo(n + 1, -1);
ll fib(int n) {
    if (n <= 1) return n;
    if (memo[n] != -1) return memo[n];      // already solved
    return memo[n] = fib(n-1) + fib(n-2);   // solve + store
}
```

`-1` as "unsolved" only works when a real answer is never `-1`.

### 6.4 Subsets — the pick / don't-pick tree

**Concept.** At each item there are exactly two branches: take it or skip it → 2^n leaves, every subset exactly once.

**When to use.** "Choose any group of items…" with n ≤ ~24. (For pure enumeration a bitmask loop, §7.5, is shorter.)

```cpp
void rec(int i, vector<int> &cur) {
    if (i == n) { /* cur is one subset */ return; }
    cur.push_back(a[i]);  rec(i + 1, cur);   // take it
    cur.pop_back();       rec(i + 1, cur);   // leave it   <-- the "backtrack"
}
```

The `pop_back()` **is** the backtracking: undo the choice before trying the other branch.

### 6.5 Subsets with a given sum

**When to use.** "Can a group sum to exactly S?" / "how many groups sum to S?" — carry the running sum as a parameter instead of building the list.

```cpp
int cnt = 0;
void rec(int i, ll cur) {
    if (i == n) { if (cur == target) cnt++; return; }
    rec(i + 1, cur + a[i]);
    rec(i + 1, cur);
}
```

### 6.6 Split into two groups, minimise the difference

**Concept.** Every subset defines a split; if one side sums to `s1`, the difference is `|total - 2·s1|`.

**When to use.** "Divide the items into two teams as evenly as possible" (Apple Division).

```cpp
ll total, best = LLONG_MAX;
void rec(int i, ll s1) {
    if (i == n) { best = min(best, llabs(total - 2*s1)); return; }
    rec(i + 1, s1 + a[i]);
    rec(i + 1, s1);
}
```

### 6.7 Permutations

**Concept.** A loop over *all unused* items at each depth → n! orders. `used[]` is what enforces "each item once".

**When to use.** Order matters (arrangements, TSP brute force). n ≤ ~10.

```cpp
void rec(vector<int> &cur, vector<bool> &used) {
    if (cur.size() == n) { /* one permutation */ return; }
    for (int i = 0; i < n; i++) {
        if (used[i]) continue;
        used[i] = true;  cur.push_back(a[i]);
        rec(cur, used);
        cur.pop_back();  used[i] = false;       // undo both
    }
}
```

Shortcut: `sort(all(a)); do { ... } while (next_permutation(all(a)));`

### 6.8 Combinations (choose k of n)

**Concept.** The `start` parameter forbids going backwards, so `{1,3}` is generated but `{3,1}` never is — order stops mattering.

**When to use.** "Choose exactly k of them" where order is irrelevant.

```cpp
void rec(int start, vector<int> &cur) {
    if ((int)cur.size() == k) { /* one combination */ return; }
    for (int i = start; i < n; i++) {
        cur.push_back(a[i]);
        rec(i + 1, cur);          // i+1 : never reuse, never go backwards
        cur.pop_back();
    }
}
```

### 6.9 N-Queens skeleton

**Concept.** Place one row at a time and **prune** immediately — a partial placement that already conflicts is abandoned before exploring below it. Pruning is what makes backtracking beat brute force.

**When to use.** Constraint placement: queens, sudoku, graph coloring, "assign without conflicts".

```cpp
bool safe(int row, int col) {
    for (int i = 0; i < row; i++) {
        if (pos[i] == col) return false;                      // same column
        if (abs(pos[i] - col) == abs(i - row)) return false;  // same diagonal
    }
    return true;
}
void rec(int row) {
    if (row == n) { count++; return; }
    for (int col = 0; col < n; col++)
        if (safe(row, col)) { pos[row] = col; rec(row + 1); }
}
```

**The whole pattern in one line:** choose → recurse → **undo**.

---

## 7. Bit manipulation & bitmask

**Concept.** Every integer is a row of on/off switches. Bitwise operators act on all 64 switches at once, in one CPU instruction. A **bitmask** reinterprets those switches as *"is item i selected?"*, so a single `int` encodes an entire subset.

**When to use.** (1) Micro-operations: parity, powers of 2, XOR tricks. (2) **n ≤ 20–24 and you must try every subset** — counting `0 … 2^n - 1` enumerates all of them for free. (3) Problems where bits are independent, so you solve each bit column separately.

### 7.1 Operators

| Op | Name | Meaning |
|---|---|---|
| `&` | AND | 1 only if **both** are 1 |
| `\|` | OR | 1 if **either** is 1 |
| `^` | XOR | 1 if they **differ** |
| `~` | NOT | flip every bit |
| `<<` | left shift | `x << 1` = ×2 |
| `>>` | right shift | `x >> 1` = ÷2 |

Single `&` `|` for bits — `&&` `||` are the boolean operators.

### 7.2 The spells

| I want to… | Spell |
|---|---|
| Check bit `i` | `(n >> i) & 1` |
| Set bit `i` ON | `n \| (1LL << i)` |
| Clear bit `i` OFF | `n & ~(1LL << i)` |
| Flip bit `i` | `n ^ (1LL << i)` |
| Is odd? | `n & 1` |
| Multiply / divide by 2 | `n << 1` / `n >> 1` |
| Count ON bits | `__builtin_popcountll(n)` |
| Is power of 2? | `n && !(n & (n-1))` |
| Lowest set bit | `n & (-n)` |
| Turn off lowest set bit | `n & (n-1)` |
| All-ones mask of `k` bits | `(1LL << k) - 1` |
| Loop all subsets | `for (int m = 0; m < (1 << n); m++)` |

```cpp
bool checkbit(ll n, ll i)   { return (n >> i) & 1; }
ll   setbit  (ll n, ll b)   { return n | (1LL << b); }
ll   clearbit(ll n, ll b)   { return n & (~(1LL << b)); }
ll   togglebit(ll n, ll b)  { return n ^ (1LL << b); }
```

### 7.3 Two traps

```cpp
1LL << 60          // use 1LL for any shift >= 31, else it overflows int
(1 << k) - 1       // BRACKETS. (1 << k - 1) parses as 1 << (k-1)
```

### 7.4 Identities

```
A & 1 = last bit        A | 0 = A       A ^ 0 = A
A ^ 1 = flip            A ^ A = 0       A ^ 0 ^ B = B
```

**When to use `A ^ A = 0`.** "Everything appears twice except one" — XOR the whole array and the pairs cancel, leaving the odd one out. O(n) time, O(1) memory.

### 7.5 Subset enumeration

**Concept.** `mask` counts 0 → 2^n−1; bit `i` of `mask` says whether item `i` joined this subset. No subset is ever missed or repeated.

**When to use.** n ≤ 20–24 and the problem is "over all possible groups…". Check the constraint first — if n = 30 this is the wrong tool.

```cpp
for (int mask = 0; mask < (1 << n); mask++) {
    ll sum = 0; int cnt = 0, mn = INT_MAX, mx = 0;
    for (int i = 0; i < n; i++) {
        if (mask & (1 << i)) {          // is item i in THIS subset?
            cnt++; sum += a[i];
            mn = min(mn, a[i]); mx = max(mx, a[i]);
        }
    }
    // use cnt / sum / mn / mx
}
```

`__builtin_popcount(mask)` gives the subset size without the inner loop.

### 7.6 Per-bit column trick

**Concept.** AND/OR/XOR never carry between positions, so bit 3 of the answer depends only on bit 3 of the inputs. Solve 30 (or 64) independent easy problems instead of one hard one.

**When to use.** The problem is about AND/OR/XOR over ranges or subsets, or "maximise the XOR/AND of…".

```cpp
for (int bit = 30; bit >= 0; bit--) {
    int on = 0;
    for (int i = 0; i < n; i++)
        if (a[i] & (1 << bit)) on++;      // how many have this bit set
}
```

Prefix over bit columns → range OR / AND in O(64) per query:

```cpp
vector<vector<ll>> pb(64, vector<ll>(n + 1, 0));
for (int b = 0; b < 64; b++)
    for (int i = 1; i <= n; i++)
        pb[b][i] = pb[b][i-1] + ((v[i] >> b) & 1);

ll OR = 0, AND = 0;
for (int b = 0; b < 64; b++) {
    ll c = pb[b][r] - pb[b][l-1];
    if (c > 0)          OR  |= (1LL << b);   // someone has it
    if (c == r - l + 1) AND |= (1LL << b);   // everyone has it
}
```

---

## 8. Strings

**Concept.** A string is an array of small integers (`s[i] - 'a'` ∈ 0..25), which is why frequency arrays and two pointers dominate string problems at this level.

**When to use.** Anagram/frequency questions → count letters. Substring (contiguous) → sliding window. Subsequence (not contiguous) → greedy two pointers or DP.

### 8.1 Frequency / anagram

**Concept.** Two strings are anagrams iff their letter counts match — sorting produces the same canonical signature.

**When to use.** "Same letters, different order", grouping words, "can we rearrange s into t".

```cpp
vector<int> f(26, 0);
for (char c : s) f[c - 'a']++;

string x = s, y = t;                    // anagram check
sort(all(x)); sort(all(y));
bool anagram = (x == y);

unordered_map<string, vector<string>> mp;   // group anagrams
for (string w : words) { string k = w; sort(all(k)); mp[k].push_back(w); }
```

### 8.2 Longest palindromic substring — expand around center

**Concept.** Every palindrome has a center; there are 2n−1 centers (n single + n−1 double), so grow outward from each. O(n²).

**When to use.** Palindromic **substring** questions with n ≤ ~5000.

```cpp
int start = 0, best = 1;
auto expand = [&](int l, int r) {
    while (l >= 0 && r < n && s[l] == s[r]) {
        if (r - l + 1 > best) { best = r - l + 1; start = l; }
        l--; r++;
    }
};
for (int i = 0; i < n; i++) { expand(i, i); expand(i, i + 1); }  // odd, even
return s.substr(start, best);
```

### 8.3 Subsequence check

**Concept.** Greedy: matching each character of `s` as early as possible in `t` is always optimal.

**When to use.** "Is s a subsequence of t?" — characters in order but not adjacent.

```cpp
int i = 0;
for (int j = 0; j < (int)t.size() && i < (int)s.size(); j++)
    if (s[i] == t[j]) i++;
bool isSub = (i == (int)s.size());
```

### 8.4 Tokenizing a line

**When to use.** Input is a whole line with an unknown number of words, or CSV-style separated values.

```cpp
string line; getline(cin, line);
stringstream ss(line);
string word;
while (ss >> word) { /* ... */ }
while (getline(ss, word, ',')) { /* split on a delimiter */ }
```

---

## 9. Math & number theory

**Concept.** Facts about integers that let you skip enumeration. Nearly all of it comes from two ideas: **divisors pair up around √n**, and **modular arithmetic keeps huge numbers small**.

**When to use.** The statement mentions divisors, primes, gcd/lcm, "count the ways mod 10^9+7", or numbers up to 10^18 where looping is impossible.

### 9.1 Divisors of n — O(√n)

**Concept.** Divisors come in pairs `(i, n/i)`, so testing up to √n finds them all.

**When to use.** "How many divisors", "sum of divisors", "is it a perfect square", for one n up to ~10^12.

```cpp
vector<ll> divs;
for (ll i = 1; i * i <= n; i++)
    if (n % i == 0) {
        divs.push_back(i);
        if (i != n / i) divs.push_back(n / i);   // guard the perfect square
    }
```

Divisor **count** of *every* number ≤ N in O(N log N) — use when many queries:

```cpp
vector<int> cnt(N + 1, 0);
for (int i = 1; i <= N; i++)
    for (int j = i; j <= N; j += i) cnt[j]++;
```

### 9.2 Primality — O(√n)

**When to use.** A handful of primality checks on big numbers. For *many* numbers ≤ 10^6, sieve instead (9.4).

```cpp
bool isPrime(ll n) {
    if (n < 2) return false;
    for (ll i = 2; i * i <= n; i++) if (n % i == 0) return false;
    return true;
}
```

### 9.3 Prime factorization — O(√n)

**Concept.** Strip each prime out completely before moving on; anything left above √n must itself be prime.

**When to use.** Counting divisors from exponents, gcd/lcm reasoning, "semi-prime" problems.

```cpp
map<ll,int> f;
for (ll p = 2; p * p <= n; p++)
    while (n % p == 0) { f[p]++; n /= p; }     // strip p fully
if (n > 1) f[n]++;                              // leftover prime > sqrt
```

### 9.4 Sieve of Eratosthenes — O(N log log N)

**Concept.** Cross out multiples of each prime; whatever survives is prime. Start at `i*i` — smaller multiples are already crossed.

**When to use.** You need primality/primes **many times** for values up to 10^6–10^7. Preprocess once, answer O(1).

```cpp
vector<bool> isP(N + 1, true);
isP[0] = isP[1] = false;
for (int i = 2; (ll)i * i <= N; i++)
    if (isP[i])
        for (int j = i * i; j <= N; j += i) isP[j] = false;
```

Smallest-prime-factor sieve → factorize any `n ≤ N` in O(log n). Use when factorizing many numbers:

```cpp
vector<int> spf(N + 1);
for (int i = 2; i <= N; i++) if (!spf[i])
    for (int j = i; j <= N; j += i) if (!spf[j]) spf[j] = i;

while (n > 1) { int p = spf[n]; while (n % p == 0) n /= p; /* p is a factor */ }
```

### 9.5 GCD / LCM

**Concept.** Euclid: `gcd(a,b) = gcd(b, a mod b)` — O(log n).

**When to use.** Fraction reduction, "meet at the same time again" (lcm), cycle lengths, "make all elements equal by dividing".

```cpp
ll gcd(ll a, ll b) { return b == 0 ? a : gcd(b, a % b); }   // or __gcd(a,b)
ll lcm(ll a, ll b) { return a / gcd(a, b) * b; }            // DIVIDE FIRST — overflow
```

`gcd(a,0)=a` · `gcd(a,b)·lcm(a,b)=a·b`. GCD of an array: fold `g = __gcd(g, a[i])` from `g = 0`.

### 9.6 Modular arithmetic

**Concept.** A clock: after `m` you wrap to 0. `%` distributes over `+`, `−`, `×` — so you can reduce at every step and never overflow.

**When to use.** The answer is huge and the statement says "modulo 10^9+7". Take `% MOD` after **every** multiplication.

```
(a + b) % m = ((a % m) + (b % m)) % m
(a - b) % m = ((a % m) - (b % m) + m) % m      <-- the +m, always
(a * b) % m = ((a % m) * (b % m)) % m
```

Division does **not** distribute — use the modular inverse (9.8).

### 9.7 Binary exponentiation — O(log n)

**Concept.** `a^n` by repeated squaring: `a^10 = (a^5)^2`. 60 multiplications instead of 10^18.

**When to use.** Any big power, especially `pow(a, b) % MOD`. Never use `pow()` from `<cmath>` for integers — it returns a double and loses precision.

```cpp
ll power(ll b, ll e, ll m) {
    ll res = 1; b %= m;
    while (e > 0) {
        if (e & 1) res = res * b % m;    // odd exponent -> take one b out
        b = b * b % m;                    // square the base
        e >>= 1;                          // halve the exponent
    }
    return res;
}
```

### 9.8 Modular inverse (m prime — Fermat)

**Concept.** Dividing mod a prime = multiplying by `a^(m-2)`.

**When to use.** Any division inside a mod computation — probabilities, nCr, averages.

```cpp
ll inv(ll a, ll m) { return power(a, m - 2, m); }
// a / b mod m  ==  a * inv(b, m) % m
```

### 9.9 Combinatorics with factorials

**Concept.** Precompute factorials and their inverses once → every `nCr` is O(1).

**When to use.** "Count the number of ways … mod 10^9+7" with many queries.

```cpp
vector<ll> fact(N), ifact(N);
fact[0] = 1;
for (int i = 1; i < N; i++) fact[i] = fact[i-1] * i % MOD;
ifact[N-1] = power(fact[N-1], MOD - 2, MOD);
for (int i = N-1; i > 0; i--) ifact[i-1] = ifact[i] * i % MOD;

ll C(int n, int r) {
    if (r < 0 || r > n) return 0;
    return fact[n] * ifact[r] % MOD * ifact[n-r] % MOD;
}
```

### 9.10 Handy

```cpp
ll ceilDiv(ll a, ll b) { return (a + b - 1) / b; }   // avoids ceil() precision bugs
// sum 1..n = n*(n+1)/2      (use ll)
// number of digits of n = floor(log10(n)) + 1
```

---

## 10. Dynamic programming

**Concept.** The problem has **overlapping subproblems** (the same situation is reached by many paths) and **optimal substructure** (the best whole is built from best parts). Solve each distinct situation once, store it, reuse it.

**When to use.** "Count the number of ways", "minimum/maximum cost to…", "is it possible to reach…", where a greedy choice is provably wrong and brute force is exponential. **Test:** can you describe your situation with 1–2 small numbers (index, remaining capacity)? Then that's your state.

**How to design one:** name the state in words → write the transition → set the base case → choose the loop order so every dependency is already computed. Complexity = number of states × cost per transition.

Top-down = recursion + memo (easier to derive). Bottom-up = loops (faster, no stack limit).

### 10.1 Fibonacci — both forms

```cpp
ll f(int n) { if (n <= 1) return n;                 // top-down
              if (memo[n] != -1) return memo[n];
              return memo[n] = f(n-1) + f(n-2); }

dp[0] = 0; dp[1] = 1;                               // bottom-up
for (int i = 2; i <= n; i++) dp[i] = dp[i-1] + dp[i-2];
```

### 10.2 0/1 Knapsack

**Concept.** State = (items considered, capacity used). Each item is a binary choice: skip, or take it and pay its weight.

**When to use.** Pick a subset under a **capacity/budget** limit to maximise value, each item usable **once**. `n × W` must be affordable (~10^7).

```cpp
// dp[i][w] = best value using items 0..i-1 with capacity w
for (int i = 1; i <= n; i++)
  for (int w = 0; w <= W; w++) {
      dp[i][w] = dp[i-1][w];                                  // skip item i
      if (wt[i-1] <= w)
          dp[i][w] = max(dp[i][w], dp[i-1][w - wt[i-1]] + val[i-1]);
  }
// answer dp[n][W]
```

1D version — **iterate w downward** so each item is used once:

```cpp
for (int i = 0; i < n; i++)
  for (int w = W; w >= wt[i]; w--)
      dp[w] = max(dp[w], dp[w - wt[i]] + val[i]);
```

Loop **upward** instead → unlimited copies (unbounded knapsack / coin change).

### 10.3 Coin change

**Concept.** To make `i`, try every coin as the *last* one used.

**When to use.** "Fewest coins to make X" / "number of ways to make X". Coins in the **outer** loop counts combinations; in the inner loop it counts ordered sequences — pick deliberately.

```cpp
vector<ll> dp(x + 1, INF); dp[0] = 0;               // minimum coins
for (int i = 1; i <= x; i++)
  for (int c : coins)
      if (c <= i) dp[i] = min(dp[i], dp[i - c] + 1);

vector<ll> ways(x + 1, 0); ways[0] = 1;             // number of combinations
for (int c : coins)
  for (int i = c; i <= x; i++) ways[i] = (ways[i] + ways[i - c]) % MOD;
```

### 10.4 LCS + reconstruction

**Concept.** State = (prefix of a, prefix of b). Characters match → extend the diagonal; otherwise drop one character and take the better side.

**When to use.** Comparing two sequences: longest common subsequence, edit distance, diff. Walk the table backwards to rebuild the actual answer.

```cpp
for (int i = 1; i <= n; i++)
  for (int j = 1; j <= m; j++)
      dp[i][j] = (a[i-1] == b[j-1]) ? dp[i-1][j-1] + 1
                                    : max(dp[i-1][j], dp[i][j-1]);

string res; int i = n, j = m;
while (i > 0 && j > 0) {
    if (a[i-1] == b[j-1])            { res += a[i-1]; i--; j--; }
    else if (dp[i-1][j] >= dp[i][j-1]) i--;
    else                               j--;
}
reverse(all(res));
```

### 10.5 LIS in O(n log n)

**Concept.** `tails[k]` = the smallest possible tail of an increasing subsequence of length k+1. Binary-search where each new value belongs and overwrite.

**When to use.** "Longest increasing/decreasing subsequence" with n up to 10^5. (The O(n²) DP is fine up to ~5000.)

```cpp
vector<int> tails;
for (int x : a) {
    auto it = lower_bound(all(tails), x);       // upper_bound => non-decreasing
    if (it == tails.end()) tails.push_back(x);
    else *it = x;
}
int lis = tails.size();                          // tails is NOT the actual LIS
```

### 10.6 Grid paths / minimum path sum

**Concept.** Each cell's best value comes from the cells you could have arrived from — so fill top-left to bottom-right.

**When to use.** Movement restricted to right/down (or similar), counting paths, minimum cost path, paths with blocked cells.

```cpp
dp[0][0] = g[0][0];
for (int i = 0; i < n; i++)
  for (int j = 0; j < m; j++) {
      if (i == 0 && j == 0) continue;
      ll best = INF;
      if (i > 0) best = min(best, dp[i-1][j]);
      if (j > 0) best = min(best, dp[i][j-1]);
      dp[i][j] = best + g[i][j];
  }
```

---

## 11. Graphs

**Concept.** Nodes + connections. The moment a problem has *"is X reachable from Y"*, *"fewest steps"*, *"groups of connected things"*, or *"A must come before B"*, it is a graph problem — even if the word "graph" never appears (grids, word ladders, states of a puzzle are all graphs).

**When to use.** Explicit edges, or an **implicit** graph where nodes are positions/states and edges are legal moves. Everything below is O(V + E) except Dijkstra.

### 11.1 Building an adjacency list

**Concept.** For each node, store the list of its neighbours. Memory O(V + E) — the only sane choice for sparse graphs.

**When to use.** Default representation. Adjacency **matrix** only when V ≤ ~1000 and you need O(1) "is there an edge u-v".

```cpp
int n, m; cin >> n >> m;
vector<vector<int>> g(n + 1);
for (int i = 0; i < m; i++) {
    int u, v; cin >> u >> v;
    g[u].push_back(v);
    g[v].push_back(u);      // omit this line for a DIRECTED graph
}
vector<bool> vis(n + 1, false);
```

Weighted: `vector<vector<pair<int,int>>> g;` with `g[u].push_back({v, w});`

### 11.2 DFS

**Concept.** Go as deep as possible, then back up. `vis[]` guarantees each node is processed once.

**When to use.** Reachability, connected components, cycle detection, trees, topological order, flood fill. **Not** for shortest paths.

```cpp
void dfs(int u) {
    vis[u] = true;
    for (int v : g[u])
        if (!vis[v]) dfs(v);
}
```

Iterative version — use when n ≥ ~10^5 and recursion may blow the stack:

```cpp
stack<int> st; st.push(s); vis[s] = true;
while (!st.empty()) {
    int u = st.top(); st.pop();
    for (int v : g[u]) if (!vis[v]) { vis[v] = true; st.push(v); }
}
```

### 11.3 BFS — shortest path in an UNWEIGHTED graph

**Concept.** Explore in rings: all nodes at distance 1, then 2, then 3. The first time you reach a node is necessarily via a shortest path.

**When to use.** "Minimum number of moves/steps" where **every move costs the same**. If costs differ → Dijkstra.

```cpp
vector<int> dist(n + 1, -1);
queue<int> q;
q.push(s); dist[s] = 0;
while (!q.empty()) {
    int u = q.front(); q.pop();
    for (int v : g[u])
        if (dist[v] == -1) {           // dist == -1 doubles as "not visited"
            dist[v] = dist[u] + 1;
            par[v] = u;
            q.push(v);
        }
}
```

**Mark visited when you PUSH, not when you pop** — otherwise nodes enter the queue many times.

Reconstruct the path (store `par[v] = u` when you first reach `v`):

```cpp
vector<int> path;
for (int cur = t; cur != -1; cur = par[cur]) path.push_back(cur);
reverse(all(path));
```

### 11.4 Connected components

**Concept.** Start a fresh DFS from every unvisited node; each start = one new component.

**When to use.** "How many groups/islands/friend circles", "is everyone connected".

```cpp
int comps = 0;
for (int i = 1; i <= n; i++)
    if (!vis[i]) { comps++; dfs(i); }
```

### 11.5 Grid as a graph (implicit)

**Concept.** No edge list needed — the neighbours of `(r,c)` are computed from the direction arrays.

**When to use.** Mazes, islands, flood fill, "shortest path in a grid with walls". Check bounds **before** touching the cell.

```cpp
int dx[] = {0, 0, 1, -1};
int dy[] = {1, -1, 0, 0};              // add diagonals for 8-direction

queue<pair<int,int>> q;
q.push({sr, sc}); d[sr][sc] = 0;
while (!q.empty()) {
    auto [r, c] = q.front(); q.pop();
    for (int k = 0; k < 4; k++) {
        int nr = r + dx[k], nc = c + dy[k];
        if (nr < 0 || nr >= n || nc < 0 || nc >= m) continue;   // bounds FIRST
        if (grid[nr][nc] == '#' || d[nr][nc] != -1) continue;
        d[nr][nc] = d[r][c] + 1;
        q.push({nr, nc});
    }
}
```

**Multi-source BFS** — push *all* sources with distance 0 before the loop. Use for "distance from each cell to the **nearest** fire/exit/shop" in one pass instead of one BFS per source.

### 11.6 Cycle detection

**Concept (undirected).** Reaching an already-visited node that isn't the one you came from means there was a second route → a cycle.

**When to use.** "Is it a tree/forest?", "does the system contain a loop?" A connected undirected graph is a **tree** iff it's connected and `edges == n - 1`.

```cpp
bool dfs(int u, int p) {
    vis[u] = true;
    for (int v : g[u]) {
        if (!vis[v]) { if (dfs(v, u)) return true; }
        else if (v != p) return true;       // back edge -> cycle
    }
    return false;
}
```

**Concept (directed).** The parent trick fails; you need to know whether the node is *currently on the recursion stack*. 0 = unseen, 1 = in progress, 2 = finished.

**When to use.** Dependency loops, "can these tasks be ordered?", deadlock detection.

```cpp
bool dfs(int u) {
    color[u] = 1;
    for (int v : g[u]) {
        if (color[v] == 1) return true;              // back edge -> cycle
        if (color[v] == 0 && dfs(v)) return true;
    }
    color[u] = 2;
    return false;
}
```

### 11.7 Topological sort (Kahn / BFS)

**Concept.** Repeatedly output any node with no remaining prerequisites, and remove it. Works only on a DAG.

**When to use.** "A must happen before B" — course prerequisites, build order, task scheduling. If fewer than n nodes come out, there's a cycle → no valid order.

```cpp
vector<int> indeg(n + 1, 0);
for (int u = 1; u <= n; u++) for (int v : g[u]) indeg[v]++;

queue<int> q;
for (int i = 1; i <= n; i++) if (indeg[i] == 0) q.push(i);

vector<int> order;
while (!q.empty()) {
    int u = q.front(); q.pop();
    order.push_back(u);
    for (int v : g[u]) if (--indeg[v] == 0) q.push(v);
}
if ((int)order.size() != n) /* cycle exists — no valid order */;
```

### 11.8 Bipartite check (2-coloring)

**Concept.** Paint each node the opposite colour of its neighbour. A conflict means an odd-length cycle → not bipartite.

**When to use.** "Split into two teams with no internal conflicts", "is the graph 2-colorable", odd-cycle detection.

```cpp
vector<int> col(n + 1, -1);
queue<int> q; q.push(s); col[s] = 0;
while (!q.empty()) {
    int u = q.front(); q.pop();
    for (int v : g[u]) {
        if (col[v] == -1) { col[v] = 1 - col[u]; q.push(v); }
        else if (col[v] == col[u]) /* NOT bipartite */;
    }
}
```

### 11.9 Dijkstra (non-negative weights)

**Concept.** BFS with a priority queue: always expand the closest unfinished node, so the first time you finalise a node its distance is optimal.

**When to use.** Shortest path when **edges have different costs** and none are negative. O((V+E) log V).

```cpp
vector<ll> d(n + 1, INF); d[s] = 0;
priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<>> pq;
pq.push({0, s});
while (!pq.empty()) {
    auto [du, u] = pq.top(); pq.pop();
    if (du > d[u]) continue;                     // stale entry
    for (auto [v, w] : g[u])
        if (d[u] + w < d[v]) { d[v] = d[u] + w; pq.push({d[v], v}); }
}
```

### 11.10 DSU / Union-Find

**Concept.** Keep one representative per group; `find` follows parents to the root (compressing the path), `unite` hangs the smaller tree under the bigger. Effectively O(1).

**When to use.** Groups **merge over time** and you keep asking "same group?" — connectivity with incremental edges, Kruskal's MST, "are these two people already friends".

```cpp
vector<int> par(n + 1), sz(n + 1, 1);
iota(all(par), 0);

int find(int x) { return par[x] == x ? x : par[x] = find(par[x]); }
void unite(int a, int b) {
    a = find(a); b = find(b);
    if (a == b) return;
    if (sz[a] < sz[b]) swap(a, b);
    par[b] = a; sz[a] += sz[b];
}
```

### 11.11 Which tool?

| Question in the statement | Tool |
|---|---|
| Reachable? / how many groups | DFS or BFS |
| Fewest moves, all moves equal | BFS |
| Cheapest path, costs differ | Dijkstra |
| Nearest source from every cell | multi-source BFS |
| A before B / valid order | topological sort |
| Loop in an undirected graph | DFS with parent |
| Loop in a directed graph | DFS with 3 colors |
| Split into two conflict-free sides | BFS bipartite |
| Groups merging as edges arrive | DSU |

---

## 12. Contest checklist

**Before you code**
- Read the constraints FIRST — they name the intended complexity.
- Check the sample by hand. If your understanding disagrees with the sample, your understanding is wrong.
- Multiple test cases? Then **reset every global array/counter inside the loop.**

**While you code**
- `long long` on: any sum of ≥ 10^5 elements, any product of two values ≥ 10^5, any prefix sum.
- `accumulate(all(v), 0LL)` — not `0`.
- Overflow-safe mid: `l + (r - l) / 2`.
- 1-indexed or 0-indexed? Pick one per problem and stay with it.
- `\n` not `endl` inside loops.
- Every two-pointer branch must move a pointer (no infinite loop).
- Comparators use `<`, never `<=`.

**Getting WA**
- n = 1, empty input, all elements equal, all negative.
- Duplicates — should they be skipped or counted?
- Did sorting destroy the indices the answer needs?
- Integer division truncating where you wanted `ceilDiv`.
- Negative `%`: fix with `((x % m) + m) % m`.
- Output format — trailing spaces, blank line between cases, "Case #i:".

**Getting TLE**
- `endl` in a hot loop, or missing `sync_with_stdio(false)`.
- `map` where `unordered_map`, a `vector` frequency array, or a plain array would do.
- Passing big vectors **by value** into a function — take `&`.
- `lower_bound(s.begin(), s.end(), x)` on a `set` — use the member function.
- Recomputing a range sum instead of prefix-summing it.

**Getting RE**
- Out-of-bounds by one (`i <= n` on a 0-indexed array of size n).
- Recursion depth too deep → rewrite iteratively.
- Division by zero, `s[i]` on an empty string, `.top()` / `.front()` on an empty container.

---

## 13. "Which technique?" — read the statement

| The statement says… | Reach for |
|---|---|
| "sorted array", "find a value" | binary search (§3) |
| "minimum X such that", "maximum X such that" | binary search on the answer (§3.4) |
| "contiguous subarray/substring", all positive | sliding window (§4.8) |
| "contiguous" but with negatives, or exact sum | prefix sum + hash map (§4.9) |
| "pair/triple with sum …" | sort + two pointers (§4.2–4.4) |
| many range-sum queries | prefix sum (§5.1) |
| many range-add updates, print at end | difference array (§5.2) |
| "count the ways", "min/max cost", greedy fails | DP (§10) |
| n ≤ 24, "every possible group" | bitmask subsets (§7.5) |
| n ≤ 10, "every possible order" | permutations / backtracking (§6.7) |
| "fewest moves", equal cost | BFS (§11.3) |
| "cheapest path", costs differ | Dijkstra (§11.9) |
| "how many groups/islands" | DFS components (§11.4) or DSU (§11.10) |
| "A before B" | topological sort (§11.7) |
| divisors / primes / gcd / "mod 10^9+7" | number theory (§9) |
| XOR / AND / OR of things | per-bit columns (§7.6) |

---

Related: [[Problem Solving/PS Level 1/Binary Search]] · [[Two Pointers]] · [[Bitmasks]] · [[Recursion Notes]] · [[Sliding window Tips]] · [[Graphs, DFS]] · [[BFS, Graph Applications]] · [[DP]] · [[Number theory.1]] · [[Number Theory.2]] · [[1D Partial Sum]] · [[2D Partial Sum]] · [[Backtracking]] · [[MUST HAVE]]
