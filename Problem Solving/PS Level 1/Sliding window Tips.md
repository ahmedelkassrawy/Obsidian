# Sliding Window Technique — Concepts & Patterns

## What is the Sliding Window?

The sliding window technique maintains a **contiguous subarray/substring** (the "window") and moves it across the sequence to avoid recomputing from scratch. Instead of checking every possible subarray (O(n²) or worse), you slide the window's boundaries and **incrementally update** the answer.

### Two types of sliding windows

| Type | Behavior | Use Case |
|---|---|---|
| **Variable window** | Both `l` and `r` move forward; window shrinks or grows | "Longest subarray with sum ≤ k", "distinct elements ≤ k" |
| **Fixed window** | `r - l + 1` is constant; both advance together | Max sum of any k-length subarray |

### Visual: how a sliding window moves

```
Array:        [ 2   1   3   5   1   4   3 ]

Window moves (variable, target sum ≤ 6):

  [ 2 ]              sum = 2   len=1
  [ 2   1 ]          sum = 3   len=2
  [ 2   1   3 ]      sum = 6   len=3  ← max so far
      [ 1   3   5 ]  sum = 9   >6 → shrink
      [ 3   5 ]      sum = 8   >6 → shrink
      [ 5 ]          sum = 5   len=1
      [ 5   1 ]      sum = 6   len=2
      [ 5   1   4 ]  sum = 10  >6 → shrink
          [ 1   4 ]  sum = 5   len=2
          [ 1   4   3 ] sum=8  >6 → shrink
          [ 4   3 ]  sum = 7   >6 → shrink
          [ 3 ]      sum = 3   len=1
```

Each step: add one element on the right (r++), remove as many from the left (l++) as needed to stay valid. The answer updates from `r - l + 1` in O(1).

### Not all "subarray problems" are sliding window

Some subarray problems use **prefix sums + a hashmap** instead. They still solve "find subarrays with property X" but the math works through prefix differences, not window movement. I label them below so you can tell them apart.

---

## Subarray sum (Prefix Sum + Hashmap — NOT sliding window)

**Problem:** Count how many subarrays have sum exactly `x`.

**Why not sliding window?** Because `arr[i]` can be negative. Sliding window only works when the window property is monotonic (adding elements always increases sum). With negatives, a larger window might have a *smaller* sum, so the two-pointer shrink logic breaks.

**How prefix sum works instead:**

```
arr    =  [ 2   -1    3    5   -2    1 ]
prefix =  [ 0    2    1    4    9    7    8 ]
            ↑
          start=0

Subarray [1..3] = arr[1] + arr[2] + arr[3]
                = prefix[4] - prefix[1]
                = 9 - 1 = 8 ✓
```

The key insight: `prefix[j] - prefix[i] = sum of subarray [i..j-1]`.  
So if we want sum `x`, we look for pairs `(i, j)` where `prefix[j] - prefix[i] = x`, i.e. `prefix[i] = prefix[j] - x`.  
A hashmap counts how many times each prefix sum has appeared before.

**Counting subarrays summing to x = 3:**

```
prefix: [0, 2, 1, 4, 9, 7, 8]

We iterate j, check how many earlier i give prefix[i] = prefix[j] - 3:

j=0 (prefix=2):  need earlier prefix = -1 → count 0
j=1 (prefix=1):  need earlier prefix = -2 → count 0
j=2 (prefix=4):  need earlier prefix = 1  → count 1 (j=1)   → subarray [2] (arr[2]=3)
j=3 (prefix=9):  need earlier prefix = 6  → count 0
j=4 (prefix=7):  need earlier prefix = 4  → count 1 (j=2)   → subarray [3..4] = [5,-2]
j=5 (prefix=8):  need earlier prefix = 5  → count 0

Total = 2
```

```C++
#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

int main() {
    int n;
    long long x;
    cin >> n >> x;

    vector<long long> arr(n);
    for (int i = 0; i < n; i++) 
    {
        cin >> arr[i];
    }

    unordered_map<long long, int> prefix_sum_count;
    long long prefix_sum = 0;
    int subarray_count = 0;

    // Initialize the map with a prefix sum of 0 to account for subarrays that start from index 0.
    // A subarray from 0 to j has sum = prefix[j] - 0, so we seed prefix=0 with count 1.
    prefix_sum_count[0] = 1;

    for (int i = 0; i < n; i++) 
    {
        prefix_sum += arr[i];

        // Check if there's a prefix sum that would result in a subarray sum of x.
        // We want: prefix_sum - earlier_prefix = x  →  earlier_prefix = prefix_sum - x
        if (prefix_sum_count.find(prefix_sum - x) != prefix_sum_count.end()) 
        {
            subarray_count += prefix_sum_count[prefix_sum - x];
        }

        // Record this prefix sum for future iterations
        prefix_sum_count[prefix_sum]++;
    }

    cout << subarray_count << endl;

    return 0;
}
```

---

## Subarray of distinct values (Variable Window — true sliding window)

**Problem:** Count subarrays with **at most k distinct elements**.

**Visual walkthrough:**

```
arr = [1, 2, 1, 3, 2], k = 2

r=0  [1]               distinct=1 ≤ k
     count += 1 → new: [1]

r=1  [1, 2]            distinct=2 ≤ k
     count += 2 → new: [2], [1,2]

r=2  [1, 2, 1]         distinct=2 ≤ k
     count += 3 → new: [1], [2,1], [1,2,1]

r=3  [1, 2, 1, 3]      distinct=3 > k → shrink
     → [2, 1, 3]       distinct=3 > k → shrink
     → [1, 3]          distinct=2 ≤ k ✓
     count += 2 → new: [3], [1,3]

r=4  [1, 3, 2]         distinct=3 > k → shrink
     → [3, 2]          distinct=2 ≤ k ✓
     count += 2 → new: [2], [3,2]

Total = 1 + 2 + 3 + 2 + 2 = 10
```

**Why `count += (r - l + 1)`?** Every valid subarray ending at `r` starts at some position between `l` and `r`. There are exactly `r - l + 1` possible start positions. Counting by right endpoint ensures we count each subarray exactly once.

```C++
#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

int main() {
    int n, k;
    cin >> n >> k;

    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    unordered_map<int, int> mp;
    int l = 0;
    long long cnt = 0;

    for (int r = 0; r < n; r++) {
        mp[arr[r]]++;  // Add the element at `r` to the current window

        // If we have more than `k` distinct elements, shrink the window from the left
        while (mp.size() > k) 
        {
            mp[arr[l]]--;// Decrease the mp of the element at `l`
            
            if (mp[arr[l]] == 0) 
            {
                mp.erase(arr[l]);  // Remove element if its mp reaches zero
            }
            l++;  // Move the left pointer to shrink the window
        }

        // At this point, we have a valid window with at most `k` distinct elements
        cnt += (r - l + 1);  // Count subarrays ending at `r`
    }

    cout << cnt << endl;

    return 0;
}
```

---

## Basic Sliding window sum (Variable Window — true sliding window)

**Problem:** Maximum number of consecutive books you can read within `t` minutes (each book[i] has a time cost a[i]).

**Visual walkthrough:**

```
books = [3, 1, 2, 5, 4], t = 6

r=0 add 3 → sum=3 ≤ t,  l=0  len=1  max=1
r=1 add 1 → sum=4 ≤ t,  l=0  len=2  max=2
r=2 add 2 → sum=6 ≤ t,  l=0  len=3  max=3
r=3 add 5 → sum=11 > t → shrink!
   remove book[0]=3 → sum=8 > t → shrink
   remove book[1]=1 → sum=7 > t → shrink
   remove book[2]=2 → sum=5 ≤ t ✓  l=3  len=1  max=3
r=4 add 4 → sum=9 > t → shrink!
   remove book[3]=5 → sum=4 ≤ t ✓  l=4  len=1  max=3

Result: max_length = 3
```

**Why sliding window works here:** Each book adds a positive time cost. Adding books always increases `current_time`, removing always decreases it (monotonic). If `current_time > t`, we *must* drop books from the left — no other arrangement fixes the overflow. This monotonic property makes sliding window the right tool.

```C++
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, t;
    cin >> n >> t;
    
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    
    int l = 0, r = 0, current_time = 0, max_length = 0;
    
    while (r < n) {
        current_time += a[r];
        
        // If the total time exceeds the available time, move the left pointer to shrink the window
        while (current_time > t) {
            current_time -= a[l];
            l++;
        }
        
        // Calculate the number of books in the current window
        max_length = max(max_length, r - l + 1);
        
        // Move the right pointer to include the next book
        r++;
    }
    
    cout << max_length << endl;
    
    return 0;
}
```

---

## Subarray Divisibility (Prefix Sum + Modulo — NOT sliding window)

**Problem:** Count subarrays whose sum is **divisible by n**.

Same prefix-sum family as the first problem, but now the condition is modular:  
`(prefix[j] - prefix[i]) % n == 0` → `prefix[j] % n == prefix[i] % n`.  
So instead of looking for a specific difference, we count matching **remainders**.

**Why not sliding window?** Same reason as subarray sum: negative numbers break monotonicity. Also, the modulo operation wraps around.

**Visual walkthrough:**

```
arr = [3, 1, 2, -4, 6], n = 5

   i    arr[i]    prefix    mod=prefix%5    modCount map          result
   -     -         0          0             {0:1}                 0
   0     3         3          3             {0:1, 3:1}            0
   1     1         4          4             {0:1, 3:1, 4:1}       0
   2     2         6          1             {0:1, 3:1, 4:1, 1:1}  0
   3    -4         2          2             {0:1, 3:1, 4:1, 1:1, 2:1}  0
   4     6         8          3             {0:1, 3:2, ...}       1
                   
At i=4: prefix=8, mod=3. Mod 3 was seen at i=0 (prefix=3).
That means subarray [1..4] = [1,2,-4,6] has sum = 5, and 5 % 5 = 0 ✓
```

Note: `(prefixSum % n + n) % n` handles C++'s negative modulo behavior. In C++, `-4 % 5 = -4`, but mathematically we want `1`. The `+ n) % n` adjustment shifts negative remainders into the [0, n-1] range.

```C++
#include <iostream>
#include <unordered_map>
using namespace std;

int main() {
    int n;
    cin >> n;
    
    int arr[n];
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    unordered_map<int, int> modCount;
    modCount[0] = 1;  // Initialize with the remainder 0 having count 1 (for subarrays that start from index 0)
    
    long long prefixSum = 0;
    long long result = 0;
    
    for (int i = 0; i < n; i++) {
        prefixSum += arr[i];
        
        // Compute the modulo and ensure it is non-negative
        int mod = (prefixSum % n + n) % n; 
        // If this modulo has been seen before, it means there are subarrays
        // whose sum is divisible by n
        result += modCount[mod];
        // Increment the count of this mod value
        modCount[mod]++;
    }
    
    cout << result << endl;
    
    return 0;
}
```

---

## We want pairs of same sum (Frequency Map — NOT sliding window)

**Problem:** Given participant weights, form the maximum number of **pairs** (teams of 2) such that each pair has the *same* total weight (each participant belongs to at most one team).

**Core idea:** For each possible total `s` (from 2 to 2n), count how many pairs can make that sum. The answer is the maximum across all `s`.

**How to count pairs for a given sum `s`:**

```
weights = [1, 2, 2, 3, 3, 4]
freq map: {1:1, 2:2, 3:2, 4:1}

For s = 5:
  w=1, other=4 → min(1,1) = 1  → 1 pair (1,4)
  w=2, other=3 → min(2,2) = 2  → 2 pairs (2,3)×2
  w=3, other=2 → already counted (same as w=2,other=3) → adds 2 again
  w=4, other=1 → already counted (same as w=1,other=4) → adds 1 again

total = 1+2+2+1 = 6  → total/2 = 3 teams ✓
```

**Why `total /= 2`?** The inner loop iterates over all weights in the map, so each pair is counted twice: once as `(w, other)` and once as `(other, w)`. We divide by 2 to correct.

**Edge case `other == w` (same weight):**  
If `s = 4` and `freq[2] = 5`: `min(5, 5) = 5`, total after ÷2 = 2 (integer division).  
Correct: floor(5/2) = 2 teams of (2,2). The integer division naturally rounds down, which is what we want (can't have half a team).

```C++
#include <iostream>
#include <map>
#include <algorithm>

using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
    
    int t;
    cin >> t; // Read the number of test cases
    
    while (t--) {
        int n;
        cin >> n; // Read the number of participants
        map<int, int> mp; // Map to store frequency of each weight
        
        // Read the weights and store frequencies in the map
        for (int i = 0; i < n; i++) {
            int x;
            cin >> x;
            mp[x]++;
        }

        int maxi = 0; // To store the maximum number of teams we can form
        // Try all possible total weights from 2 to 2 * n
        for (int i = 1; i <= (2 * n); i++) {
            int total = 0;
            // For each weight, check if we can form a team with another weight such that their sum equals 'i'
            for (auto j : mp) {
                int other = i - j.first;
                // If the other weight exists in the map, form a pair
                if (other >= 1 && mp.count(other)) {
                    total += min(j.second, mp[other]);
                }
            }
            total /= 2; // Each team is counted twice (once for each direction)
            maxi = max(maxi, total); // Keep track of the maximum number of teams
        }
        
        cout << maxi << "\n"; // Output the result for this test case
    }

    return 0;
}
```

**Key points about this approach:**
- We try **every possible sum** from 2 to 2n — individual weights range from 1 to n, so max pair sum is 2n.
- `other = i - j.first` — what weight pairs with `j.first` to reach sum `i`?
- If `other ≤ 0`, skip — no such weight exists.
- `total += min(j.second, mp[other])` — the **bottleneck** is whichever weight has fewer participants. You can't make more teams than the less abundant weight allows.
- Time complexity: O(n × unique_weights), which is fine for small constraints (n ≤ 50 typical for this problem).

---

## Longest substring with no duplicates (Variable Window — true sliding window)

**Problem:** Find the longest substring where every character is unique.

**Visual walkthrough:**

```
s = "abcabcbb"

r=0  [a]               set={a}, max=1
r=1  [a b]             set={a,b}, max=2
r=2  [a b c]           set={a,b,c}, max=3
r=3  [a b c a]         'a' duplicate → shrink
     shrink: [b c a]   set={b,c,a}, max=3
r=4  [b c a b]         'b' duplicate → shrink
     shrink: [c a b]   set={c,a,b}, max=3
r=5  [c a b c]         'c' duplicate → shrink
     shrink: [a b c]   set={a,b,c}, max=3
r=6  [a b c b]         'b' duplicate → shrink
     shrink: [b c b]   still duplicate → shrink again
     shrink: [c b]     set={c,b}, max=3
r=7  [c b b]           'b' duplicate → shrink
     shrink: [b]       set={b}, max=3

Result: maxlength = 3 ("abc")
```

The critical loop: as long as `s[r]` is already in the set, keep erasing from the left and moving `l` forward until the duplicate is gone.

```C++
#include <iostream>
#include <unordered_set>
#include <string>
using namespace std;

int main()
{
    string s;
    cin >> s;

    int l = 0;
    int maxlength = 0;
    
    unordered_set<char> st;

    for (int r = 0; r < s.size(); r++)
    {
        // If character is already in the set, shrink the window from the left
        while (st.find(s[r]) != st.end())
        {
            st.erase(s[l]);
            l++;
        }
        // Add the current character to the set
        st.insert(s[r]);

        // Update the maximum length of the substring
        maxlength = max(maxlength, r - l + 1);
    }

    cout << maxlength << endl;
    return 0;
}
```

---

## Min substring window (Variable Window — true sliding window)

**Problem (LeetCode 76):** Given strings `s` and `t`, find the **minimum window** in `s` that contains **all characters of `t`** (with their frequencies).

**Key data structure:** Two frequency maps — `t_count` (the requirement) and `window_count` (what we currently have). A `formed` counter tracks how many distinct characters have met their quota — this avoids scanning the window for requirements at every step.

**Visual walkthrough:**

```
s = "ADOBECODEBANC", t = "ABC"
t_count = {A:1, B:1, C:1}, required = 3

r=0  [A]                                formed=1 (A done)
r=1  [A D]                              formed=1
r=2  [A D O]                            formed=1
r=3  [A D O B]                          formed=2 (B done)
r=4  [A D O B E]                        formed=2
r=5  [A D O B E C]                      formed=3 ✓  min="ADOBEC" (len=6)
     shrink: [D O B E C]                formed=3, no improvement
     shrink: [O B E C]                  formed=2 → stop (lost A)

...

r=10 [B E C O D E B A]                  formed=3 ✓
     shrink: [E C O D E B A]            formed=3, len=6
     shrink: [C O D E B A]              formed=3, len=5 ← new min "CODEBA"
     shrink: [O D E B A]                formed=2 → stop (lost C)

...

r=12 [O D E B A N C]                    formed=3 ✓
     shrink: [D E B A N C]              formed=3, len=6
     shrink: [E B A N C]                formed=3, len=5
     shrink: [B A N C]                  formed=3, len=4 ← new min "BANC"
     shrink: [A N C]                    formed=2 → stop (lost B)

Result: "BANC"
```

**How `formed` works:**  
`formed` only changes when a character's count *crosses its threshold exactly*:
- `window_count[c] == t_count[c]` after increment → `formed++` (this character just met its quota)
- `window_count[c] == t_count[c] - 1` after decrement → `formed--` (it just fell below)

This keeps the validity check O(1) instead of O(k) per step.

```C++
#include <iostream>
#include <unordered_map>
#include <string>
#include <climits>
using namespace std;

int main()
{
    string s, t;
    cin >> s >> t;

    if (t.length() > s.length())
    {
        cout << "" << endl;
        return 0;
    }

    unordered_map<char, int> t_count, window_count;
    for (char c : t)
        t_count[c]++;

    int l = 0, min_length = INT_MAX, min_start = 0, required = t_count.size(), formed = 0;

    for (int r = 0; r < s.size(); r++)
    {
        char c = s[r];
        window_count[c]++;
        if (t_count[c] > 0 && window_count[c] == t_count[c])
            formed++;

        while (formed == required)
        {
            if (r - l + 1 < min_length)
            {
                min_length = r - l + 1;
                min_start = l;
            }

            char left_char = s[l++];
            if (t_count[left_char] > 0 && --window_count[left_char] < t_count[left_char])
                formed--;
        }
    }

    cout << (min_length == INT_MAX ? "" : s.substr(min_start, min_length)) << endl;
    return 0;
}
```

---

## Summary: How to choose the right technique

| Pattern | Data structure | Works with negatives? | Typical problem |
|---|---|---|---|
| **Variable sliding window** | Two pointers + counter/`unordered_set` | No (needs monotonic) | Longest/shortest subarray with ≤ k distinct, sum ≤ k |
| **Fixed sliding window** | Two pointers | No | Max sum of any k-length subarray |
| **Prefix sum + hashmap** | `unordered_map<long long, int>` | **Yes** | Subarray sum = target, subarray divisibility |
| **Frequency map + iteration** | `map<int, int>` | N/A | Pair/team formation problems |

**The key question: Is the property monotonic?**  
If adding elements always increases the measured value and removing always decreases it → **sliding window**.  
If not (negatives, modulo, non-monotonic frequency matching) → **prefix sum + hashmap**.