---
tags: [problem-solving, reference, ecpc, contest]
topic: ECPC Reference Sheet
description: Printable one-file reference for the contest — templates, STL, and every Level-1 technique
---

# ECPC Reference Sheet

Print settings: A4, portrait, margins 10mm, **scale 80%**. Code blocks are kept short on purpose so no line wraps in print.
Built from `PS Level 1` + `C++ Notes` + `Bookmarks`.

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

**Complexity budget — ~10^8 simple ops/second.**

| n up to | What fits |
|---|---|
| 10 – 12 | `O(n!)` permutations |
| 20 – 24 | `O(2^n)` or `O(2^n · n)` bitmask |
| 500 | `O(n^3)` |
| 5·10^3 | `O(n^2)` |
| 10^5 – 10^6 | `O(n log n)` — sort, binary search, set/map |
| 10^7 – 10^8 | `O(n)` only, and keep the constant small |

**Value limits**

| Type | Max |
|---|---|
| `int` | ~2.1·10^9 |
| `long long` | ~9.2·10^18 |
| `unsigned long long` | ~1.8·10^19 |

Constants: `const ll INF = 1e18;` `const int inf = 1e9;` `const ll MOD = 1e9 + 7;`

**Output formatting**

```cpp
cout << fixed << setprecision(2) << x;   // needs <iomanip>
cout << "\n";                            // never endl in loops (flushes)
```

---

## 1. STL

### 1.1 Containers — pick by what you need

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

### 1.2 vector

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

```cpp
map<char,int> freq;
for (char c : s) freq[c]++;            // missing key auto-creates 0
for (auto &p : freq) cout << p.first << " " << p.second << "\n";

if (freq.count(c)) ...                 // exists?
if (mp.find(x) != mp.end()) ...        // same thing
mp.erase(key);

set<int> s;
s.insert(x);
s.erase(x);
*s.begin();                            // smallest
*s.rbegin();                           // largest
auto it = s.lower_bound(x);            // MEMBER version — O(log n)
```

> On a `set` / `map` always use the **member** `s.lower_bound(x)`, never `lower_bound(s.begin(), s.end(), x)` — the free function is O(n) on a tree.

`multiset` erase gotcha:

```cpp
ms.erase(x);                  // erases ALL copies of x
ms.erase(ms.find(x));         // erases exactly ONE copy   <-- usually what you want
```

### 1.4 priority_queue

```cpp
priority_queue<int> pq;                                     // MAX-heap
priority_queue<int, vector<int>, greater<int>> mn;           // MIN-heap
priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<>> d;  // Dijkstra

pq.push(x); pq.top(); pq.pop(); pq.empty(); pq.size();
```

Pairs sort by `.first`, then `.second`. To make a max-heap into a min-heap cheaply, push `-x`.

### 1.5 pair / tuple

```cpp
pair<int,int> p = {a, b};
p.first; p.second;
vector<pair<int,int>> v;
v.push_back({val, idx});

tuple<int,int,int> t = {a, b, c};
auto [x, y, z] = t;            // C++17 structured binding
```

### 1.6 Algorithms you will actually use

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
__gcd(a, b);
swap(a, b);
min({a,b,c});  max({a,b,c});
fill(all(v), 0);
memset(arr, 0, sizeof arr);               // only for 0 and -1
```

### 1.7 String

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

### 2.1 Comparators

```cpp
bool cmp(const pair<int,int> &a, const pair<int,int> &b) {
    if (a.first != b.first) return a.first < b.first;   // asc by first
    return a.second > b.second;                          // tie: desc by second
}
sort(all(v), cmp);

// lambda, inline
sort(all(v), [](auto &a, auto &b) { return a.second < b.second; });
```

Rule: the comparator returns **true when `a` must come before `b`**. It must be a strict weak order — never `<=`, that crashes.

### 2.2 Sorting structs

```cpp
struct Dragon {
    int strength;
    int bonus;
};

bool compare(const Dragon &a, const Dragon &b) {
    return a.strength < b.strength;
}

vector<Dragon> d(n);
for (int i = 0; i < n; i++) cin >> d[i].strength >> d[i].bonus;
sort(all(d), compare);
```

Or define it inside the struct:

```cpp
struct P {
    int x, y;
    bool operator<(const P &o) const { return x < o.x; }
};
```

### 2.3 Keeping the original index

Sorting destroys positions. If the answer needs indices, sort `(value, index)` pairs:

```cpp
vector<pair<int,int>> v;
for (int i = 0; i < n; i++) v.push_back({a[i], i});
sort(all(v));                          // v[k].second is the original index
```

### 2.4 Counting sort / frequency array

When values are small (`≤ 10^6`), skip the sort:

```cpp
vector<int> freq(MAXV + 1, 0);
for (int x : a) freq[x]++;
for (int x = 0; x <= MAXV; x++)
    while (freq[x]--) cout << x << " ";
```

---

## 3. Binary search

**Rule: the array must be sorted.** Every step halves the window → O(log n).

### 3.1 Does `x` exist?

```cpp
int l = 0, r = n - 1, ans = -1;
while (l <= r) {
    int mid = l + (r - l) / 2;        // overflow-safe
    if (a[mid] == x)      { ans = mid; break; }
    else if (a[mid] < x)  l = mid + 1;
    else                  r = mid - 1;
}
```

`l <= r` (not `<`) — when `l == r` the window still holds one element.

### 3.2 Lower / upper bound by hand

```cpp
// first index with a[i] >= x
int l = 0, r = n - 1, ans = n;        // ans = n means "no such element"
while (l <= r) {
    int mid = l + (r - l) / 2;
    if (a[mid] >= x) { ans = mid; r = mid - 1; }   // valid — but look left for earlier
    else               l = mid + 1;
}
```

Upper bound = the same code with `a[mid] > x`.
Initialise `ans = n`, **not 0** — with `ans = 0` a "not found" answer is indistinguishable from "found at index 0".

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
| Does `x` exist? | plain binary search / `binary_search(all(v),x)` |
| First index `>= x` | `lower_bound` |
| First index `> x` | `upper_bound` |
| How many `x` | `upper_bound - lower_bound` |
| How many in `[L,R]` | `upper_bound(R) - lower_bound(L)` |

### 3.4 Binary search on the ANSWER

Use when the question is "minimum X such that it works" and `check(X)` is **monotonic** (false…false, true…true).

```cpp
bool check(ll mid) { /* is mid feasible? */ }

ll l = 1, r = 1e18, ans = -1;
while (l <= r) {
    ll mid = l + (r - l) / 2;
    if (check(mid)) { ans = mid; r = mid - 1; }   // MINIMISE: shrink right
    else              l = mid + 1;
}
```

To **maximise**, flip: on success `ans = mid; l = mid + 1;`.

Classic shapes: minimum machine time to produce k items, minimum capacity, max minimum distance, "magic powder", split-array-into-k-parts.

**Real form (Machines: t seconds to make ≥ k items):**

```cpp
bool check(ll t) {
    ll made = 0;
    for (int i = 0; i < n; i++) {
        made += t / a[i];
        if (made >= k) return true;    // early exit avoids overflow
    }
    return made >= k;
}
```

Floating point version: run a fixed 100 iterations instead of `l <= r`.

```cpp
double l = 0, r = 1e9;
for (int i = 0; i < 100; i++) {
    double mid = (l + r) / 2;
    if (check(mid)) r = mid; else l = mid;
}
```

---

## 4. Two pointers & sliding window

Both are O(n) because **each pointer only ever moves forward** — total moves ≤ 2n.

### 4.1 The three families

| Family | Movement | Needs | Typical use |
|---|---|---|---|
| Opposite | `l→ ... ←r` | sorted / symmetric | pair with sum X, palindrome, container-with-most-water |
| Same direction (window) | both → | window validity monotonic | longest/shortest subarray, ≤k distinct |
| Two arrays | one pointer each | both sorted | merge, intersection, union |

### 4.2 Pair with a given sum

```cpp
sort(all(a));
int l = 0, r = n - 1;
while (l < r) {                       // '<' : an element can't pair with itself
    ll sum = a[l] + a[r];             // ll — two 1e9 values overflow int
    if (sum == target) break;
    else if (sum < target) l++;       // only way to grow the sum
    else                   r--;       // only way to shrink it
}
```

### 4.3 Count pairs with sum ≤ X

```cpp
sort(all(v));
int l = 0, r = n - 1; ll cnt = 0;
while (l < r) {
    if (v[l] + v[r] <= target) { cnt += (r - l); l++; }
    else r--;
}
```

`cnt += (r - l)` because if `v[l]+v[r] ≤ target`, then `v[l]` paired with **every** index in `l+1..r` is also ≤ target — count them all at once.

### 4.4 3Sum — fix one, two-point the rest (O(n²))

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

```cpp
int l = 0, r = s.size() - 1;
bool ok = true;
while (l < r) {
    if (s[l] != s[r]) { ok = false; break; }
    l++; r--;
}
```

### 4.6 Merge two sorted arrays

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

```cpp
ll sum = 0, best = LLONG_MIN;
for (int i = 0; i < n; i++) {
    sum += a[i];
    if (i >= k) sum -= a[i - k];       // slide: drop the element leaving
    if (i >= k - 1) best = max(best, sum);
}
```

### 4.8 Variable window — the universal skeleton

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

Sliding window needs adding an element to only ever make the window "more invalid". **Negative numbers break this** — a longer window is not necessarily a bigger sum. Use prefix sum + hash map instead:

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

Subarray sum divisible by k → same idea keyed on `((pre % k) + k) % k`.

---

## 5. Prefix sums & difference arrays

### 5.1 1D prefix sum — many range-sum QUERIES

```cpp
vector<ll> pre(n + 1, 0);
for (int i = 1; i <= n; i++) pre[i] = pre[i-1] + a[i];   // a is 1-indexed
// sum of a[l..r] :
ll s = pre[r] - pre[l-1];
```

### 5.2 1D difference array — many range UPDATES

Mirror of prefix sum: add at `l`, cancel at `r+1`, then prefix-sum once at the end.

```cpp
vector<ll> diff(n + 2, 0);
// for each update "add val to [l, r]":
diff[l] += val;
diff[r + 1] -= val;

// materialise the final array:
ll run = 0;
for (int i = 1; i <= n; i++) { run += diff[i]; a[i] = run; }
```

O(1) per update, O(n) once at the end — instead of O(n) per update.

### 5.3 2D prefix sum

```cpp
// build
for (int i = 1; i <= n; i++)
  for (int j = 1; j <= m; j++)
    pre[i][j] = g[i][j] + pre[i-1][j] + pre[i][j-1] - pre[i-1][j-1];

// sum of rectangle (r1,c1)..(r2,c2)
ll s = pre[r2][c2] - pre[r1-1][c2] - pre[r2][c1-1] + pre[r1-1][c1-1];
```

### 5.4 2D difference array — 4 corners

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

Recognise it: **"add v to every element in [l,r], many times, print the array at the end"** → difference array. **"answer many range-sum questions on a fixed array"** → prefix sum.

---

## 6. Recursion & backtracking

Every recursion needs: **(1) a base case, (2) a step that shrinks the problem.**

### 6.1 Print before vs after the call

```cpp
void down(int n) { if (n == 0) return; cout << n << " "; down(n-1); }  // 5 4 3 2 1
void up(int n)   { if (n == 0) return; up(n-1); cout << n << " "; }    // 1 2 3 4 5
```

Before the call = on the way **down**. After the call = on the way **back up**.

### 6.2 Accumulate on return

```cpp
ll sum(int n) { return n == 0 ? 0 : n + sum(n - 1); }
```

### 6.3 Memoized recursion (top-down DP)

```cpp
vector<ll> memo(n + 1, -1);
ll fib(int n) {
    if (n <= 1) return n;
    if (memo[n] != -1) return memo[n];      // already solved
    return memo[n] = fib(n-1) + fib(n-2);   // solve + store
}
```

`-1` as "unsolved" only works when a real answer is never `-1`.

### 6.4 Subsets — the pick / don't-pick tree (2^n)

```cpp
void rec(int i, vector<int> &cur) {
    if (i == n) { /* cur is one subset */ return; }
    cur.push_back(a[i]);  rec(i + 1, cur);   // take it
    cur.pop_back();       rec(i + 1, cur);   // leave it   <-- the "backtrack"
}
```

The `pop_back()` **is** the backtracking: undo the choice before trying the other branch.

### 6.5 Subsets with a given sum

```cpp
int cnt = 0;
void rec(int i, ll cur) {
    if (i == n) { if (cur == target) cnt++; return; }
    rec(i + 1, cur + a[i]);
    rec(i + 1, cur);
}
```

### 6.6 Split array into two groups, minimise the difference

```cpp
ll total, best = LLONG_MAX;
void rec(int i, ll s1) {
    if (i == n) { best = min(best, llabs(total - 2*s1)); return; }
    rec(i + 1, s1 + a[i]);
    rec(i + 1, s1);
}
```

### 6.7 Permutations

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

Or just: `sort(all(a)); do { ... } while (next_permutation(all(a)));`

### 6.8 Combinations (choose k of n)

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

The `start` parameter is what kills duplicate orderings — one recursive call inside a loop, not two.

### 6.9 N-Queens skeleton

```cpp
bool safe(int row, int col) {
    for (int i = 0; i < row; i++) {
        if (pos[i] == col) return false;                 // same column
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

**The pattern, in one line:** choose → recurse → **undo**.

---

## 7. Bit manipulation & bitmask

### 7.1 Operators

| Op | Name | Meaning |
|---|---|---|
| `&` | AND | 1 only if **both** are 1 |
| `\|` | OR | 1 if **either** is 1 |
| `^` | XOR | 1 if they **differ** |
| `~` | NOT | flip every bit |
| `<<` | left shift | `x << 1` = ×2 |
| `>>` | right shift | `x >> 1` = ÷2 |

Use single `&` `|` for bits — `&&` `||` are the boolean operators.

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
| Loop all subsets of `n` items | `for (int m = 0; m < (1 << n); m++)` |

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

`A ^ A = 0` is how you find "the one number that appears an odd number of times": XOR everything together.

### 7.5 Subset enumeration (n ≤ 20-24)

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

Many problems become easy when you handle **each bit position independently**:

```cpp
for (int bit = 30; bit >= 0; bit--) {
    int on = 0;
    for (int i = 0; i < n; i++)
        if (a[i] & (1 << bit)) on++;
    // on = how many numbers have this bit set
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

### 8.1 Frequency / anagram

```cpp
vector<int> f(26, 0);
for (char c : s) f[c - 'a']++;

// anagram check
string x = s, y = t;
sort(all(x)); sort(all(y));
bool anagram = (x == y);

// group anagrams
unordered_map<string, vector<string>> mp;
for (string w : words) { string k = w; sort(all(k)); mp[k].push_back(w); }
```

### 8.2 Longest palindromic substring — expand around center O(n²)

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

### 8.3 Subsequence check (greedy two pointers)

```cpp
int i = 0;
for (int j = 0; j < (int)t.size() && i < (int)s.size(); j++)
    if (s[i] == t[j]) i++;
bool isSub = (i == (int)s.size());
```

### 8.4 Tokenizing a line

```cpp
string line; getline(cin, line);
stringstream ss(line);
string word;
while (ss >> word) { /* ... */ }

// split on a delimiter
while (getline(ss, word, ',')) { /* ... */ }
```

---

## 9. Math & number theory

### 9.1 Divisors of n — O(√n)

```cpp
vector<ll> divs;
for (ll i = 1; i * i <= n; i++)
    if (n % i == 0) {
        divs.push_back(i);
        if (i != n / i) divs.push_back(n / i);   // guard the perfect square
    }
```

Divisor **count** of every number ≤ N in O(N log N):

```cpp
vector<int> cnt(N + 1, 0);
for (int i = 1; i <= N; i++)
    for (int j = i; j <= N; j += i) cnt[j]++;
```

### 9.2 Primality — O(√n)

```cpp
bool isPrime(ll n) {
    if (n < 2) return false;
    for (ll i = 2; i * i <= n; i++) if (n % i == 0) return false;
    return true;
}
```

### 9.3 Prime factorization — O(√n)

```cpp
map<ll,int> f;
for (ll p = 2; p * p <= n; p++)
    while (n % p == 0) { f[p]++; n /= p; }     // strip p fully
if (n > 1) f[n]++;                              // leftover prime > sqrt
```

### 9.4 Sieve of Eratosthenes — O(N log log N)

```cpp
vector<bool> isP(N + 1, true);
isP[0] = isP[1] = false;
for (int i = 2; (ll)i * i <= N; i++)
    if (isP[i])
        for (int j = i * i; j <= N; j += i) isP[j] = false;
```

Smallest-prime-factor sieve → factorize any `n ≤ N` in O(log n):

```cpp
vector<int> spf(N + 1);
for (int i = 2; i <= N; i++) if (!spf[i])
    for (int j = i; j <= N; j += i) if (!spf[j]) spf[j] = i;

while (n > 1) { int p = spf[n]; while (n % p == 0) n /= p; /* p is a factor */ }
```

### 9.5 GCD / LCM

```cpp
ll gcd(ll a, ll b) { return b == 0 ? a : gcd(b, a % b); }   // or __gcd(a,b)
ll lcm(ll a, ll b) { return a / gcd(a, b) * b; }            // DIVIDE FIRST — overflow
```

Properties: `gcd(a,0)=a`, `gcd(a,b)=gcd(b, a%b)`, `gcd(a,b)·lcm(a,b)=a·b`.
GCD of an array: fold with `g = __gcd(g, a[i])` starting from `g = 0`.

### 9.6 Modular arithmetic

```
(a + b) % m = ((a % m) + (b % m)) % m
(a - b) % m = ((a % m) - (b % m) + m) % m      <-- the +m, always
(a * b) % m = ((a % m) * (b % m)) % m
```

Division does **not** distribute — you need the modular inverse.

### 9.7 Binary exponentiation — O(log n)

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

```cpp
ll inv(ll a, ll m) { return power(a, m - 2, m); }
// a / b mod m  ==  a * inv(b, m) % m
```

### 9.9 Combinatorics with factorials

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

Two ways to write the same thing. **Top-down** = recursion + memo (easier to derive). **Bottom-up** = loops (faster, no stack limit).

### 10.1 Fibonacci — both forms

```cpp
// top-down
ll f(int n) { if (n <= 1) return n;
              if (memo[n] != -1) return memo[n];
              return memo[n] = f(n-1) + f(n-2); }

// bottom-up
dp[0] = 0; dp[1] = 1;
for (int i = 2; i <= n; i++) dp[i] = dp[i-1] + dp[i-2];
```

### 10.2 0/1 Knapsack

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

1D space optimisation (**iterate w downward** or you reuse the same item):

```cpp
for (int i = 0; i < n; i++)
  for (int w = W; w >= wt[i]; w--)
      dp[w] = max(dp[w], dp[w - wt[i]] + val[i]);
```

Unbounded knapsack / coin change = the same loop **upward**.

### 10.3 Coin change

```cpp
// minimum coins to make x
vector<ll> dp(x + 1, INF); dp[0] = 0;
for (int i = 1; i <= x; i++)
  for (int c : coins)
      if (c <= i) dp[i] = min(dp[i], dp[i - c] + 1);

// number of ways (combinations — coins outer loop kills permutation duplicates)
vector<ll> ways(x + 1, 0); ways[0] = 1;
for (int c : coins)
  for (int i = c; i <= x; i++) ways[i] = (ways[i] + ways[i - c]) % MOD;
```

### 10.4 LCS + reconstruction

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

**How to design a DP:** name the state (what does `dp[i][j]` MEAN in words?) → write the transition → set the base case → decide the iteration order so every dependency is already computed.

---

## 11. Graphs

### 11.1 Building an adjacency list

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

```cpp
void dfs(int u) {
    vis[u] = true;
    for (int v : g[u])
        if (!vis[v]) dfs(v);
}
```

Iterative (when n is large and recursion may stack-overflow):

```cpp
stack<int> st; st.push(s); vis[s] = true;
while (!st.empty()) {
    int u = st.top(); st.pop();
    for (int v : g[u]) if (!vis[v]) { vis[v] = true; st.push(v); }
}
```

### 11.3 BFS — shortest path in an UNWEIGHTED graph

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

Reconstruct the path:

```cpp
vector<int> path;
for (int cur = t; cur != -1; cur = par[cur]) path.push_back(cur);
reverse(all(path));
```

### 11.4 Connected components

```cpp
int comps = 0;
for (int i = 1; i <= n; i++)
    if (!vis[i]) { comps++; dfs(i); }
```

To collect each component's nodes, push `u` into a vector inside `dfs` and clear it between roots.

### 11.5 Grid as a graph (implicit)

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

**Multi-source BFS**: push *all* sources with distance 0 before the loop starts. Answers "nearest X from every cell" in one pass.

### 11.6 Cycle detection

Undirected — a visited neighbour that isn't the parent:

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

A connected undirected graph is a **tree** iff `edges == n - 1` and it's connected (no cycle).

Directed — 3 colors (0 = unseen, 1 = in progress, 2 = done):

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

| Question | Tool |
|---|---|
| Reachable? / components | DFS or BFS |
| Shortest path, unweighted | BFS |
| Shortest path, weighted ≥ 0 | Dijkstra |
| Nearest source from every cell | multi-source BFS |
| Valid ordering of dependencies | topological sort |
| Cycle in undirected | DFS with parent |
| Cycle in directed | DFS with 3 colors |
| 2-colorable? | BFS bipartite |
| Merge groups online | DSU |

All of DFS/BFS is **O(V + E)**.

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
