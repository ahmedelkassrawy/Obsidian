These 8 problems are **core** LeetCode medium problems that almost every FAANG/company interview will test you on in some form.  
Mastering the patterns below will let you solve ~80% of all array/hashing questions confidently.

## Priority Topics You Must Know Cold

| Rank | Topic / Pattern                          | Why It Matters (Problems That Use It)                                                                                 | Key Things to Memorize / Practice                                                                 |
|------|------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| 1    | **Hash Map (unordered_map)**              | Appears in **every single problem** you solved. The #1 most important tool.                                           | • `mp[num]++` for counting<br>• `mp.count(x)` or `mp.find(x) != mp.end()` for lookup<br>• `target - nums[i]` complement pattern<br>• Using sorted string as key (Group Anagrams) |
| 1    | **Hash Set (unordered_set)**              | Fast O(1) duplicate detection & existence check. Optimal for Longest Consecutive & Sudoku.                             | • Insert all → iterate and only start counting when `num-1` not present (Longest Consecutive optimal solution)<br>• One set per row/col/box (Valid Sudoku) |
| 2    | **Sorting**                               | Quick way to check anagrams or find consecutive sequences.                                                                   | • `sort(str.begin(), str.end())` → use as map key (Group Anagrams)<br>• Sort array → linear pass to remove duplicates & count streaks (Longest Consecutive – your solution) |
| 3    | **Prefix / Suffix Products**              | Product Except Self classic pattern. Avoids division and handles zeros cleanly.                                             | Left-to-right prefix → Right-to-left suffix → multiply together.<br>Write this 10 times until it's muscle memory. |
| 4    | **Frequency Bucket Sort**                 | Top K Frequent Elements – O(n) solution instead of priority queue O(n log n).                                               | `vector<vector<int>> bucket(n + 1);`<br>Put numbers into bucket[frequency]<br>Iterate from back → collect k elements |
| 5    | **Multiple Validation Containers**       | Valid Sudoku – need to check 3 constraints simultaneously.                                                                   | 9 row sets + 9 col sets + 9 box sets  OR  bitmasking / array of sets (your solution is perfect) |
| 6    | **Complement Technique**                  | Two Sum (the most famous hashing problem of all time)                                                                         | Store `value → index` while iterating. Check if `target - current` already exists. |

## Exact Problem → Pattern Mapping

| Problem                          | Your Approach                          | Optimal/Better Pattern (if different)                 | Must-Know Takeaway                                                                 |
|----------------------------------|----------------------------------------|--------------------------------------------------------|-------------------------------------------------------------------------------------|
| Longest Consecutive Sequence     | Sort + linear pass (O(n log n))        | **unordered_set + start only when num-1 missing** → true O(n) | Sorting works but is slower. Always think “can I do it in one pass with a set?” |
| Contains Duplicate               | Hash map count                         | unordered_set → try insert, return false if already present | Set is cleaner and slightly faster for pure existence checks                     |
| Valid Anagram                    | Two hash maps                          | One map: count t, then decrement with s (or sort both) | Sorting strings is also completely fine and often shorter to write                |
| Two Sum                          | Hash map value → index (perfect)       | Same                                                   | This is the canonical hash map problem. Know it by heart.                          |
| Valid Sudoku                     | 9 row + 9 col + 9 box sets (perfect)   | Same or bitmasking                                     | Very clean solution. This is the standard way.                                     |
| Product Except Self              | Prefix × suffix (perfect, no division)     | Same                                                   | One of the most beautiful O(n) time O(1) extra space tricks. Memorize it.         |
| Top K Frequent Elements          | Hash map count → bucket sort (perfect) | Priority queue (min-heap of size k) also works         | Bucket sort version is faster and very elegant. Use this when freq ≤ n            |
| Group Anagrams                   | Sort each string → use as key (perfect) | Counting 26 letters → string key of counts also works  | Sorting string is simplest and runs plenty fast                                    |

## Recommended Study Order (Bang-for-Buck)

1. Two Sum → master the complement hash map pattern  
2. Contains Duplicate & Valid Anagram → frequency counting  
3. Group Anagrams → sorting/counting as key  
4. Valid Sudoku → multiple sets/arrays  
5. Product Except Self → prefix/suffix trick  
6. Top K Frequent → bucket sort version  
7. Longest Consecutive → practice both sort version and true O(n) set version  

Do all of them **twice**: once with your current style, once trying to write the absolute cleanest/optimal version.

## Quick Reference Code Templates

```cpp
// 1. Two Sum template
unordered_map<int, int> mp;
for (int i = 0; i < nums.size(); i++) {
    if (mp.count(target - nums[i])) return {mp[target - nums[i]], i};
    mp[nums[i]] = i;
}

// 2. Frequency count template
unordered_map<int, int> cnt;
for (int x : nums) cnt[x]++;

// 3. Group Anagrams template
unordered_map<string, vector<string>> mp;
for (auto s : strs) {
    string key = s;
    sort(key.begin(), key.end());
    mp[key].push_back(s);
}

// 4. Longest Consecutive O(n) 
unordered_set<int> s(nums.begin(), nums.end());
int best = 0;
for (int x : s) {
    if (s.count(x - 1)) continue;  // only start from beginning of sequence
    int cur = 1;
    while (s.count(x + cur)) cur++;
    best = max(best, cur);
}
return best;
```

### Sliding window
Master the [sliding window technique](https://leetcode.com/problems/minimum-window-substring/solutions/26808/here-is-a-10-line-template-that-can-solve-most-substring-problems/) that applies to many subarray/substring problems. In a sliding window, the two pointers usually move in the same direction will never overtake each other. This ensures that each value is only visited at most twice and the time complexity is still O(n).
- Longest / shortest subarray
- Subarray with sum ≤ K or ≥ K
- Subarray with unique elements
- Max average of subarray of size K
- Count subarrays meeting a condition

The key idea:
> **Use two pointers (`l` and `r`) to maintain a window that moves across the array without restarting.**  
> This avoids O(n²) brute force.

Instead of checking all subarrays, you **expand the window** with `r` and **shrink it** with `l`.

Types:
1. Fixed-size window
   - r expands, l moves when window size == k

2. Variable-size window
   - r expands
   - shrink using l while invalid
   - update best answer when valid

```python
int l = 0;
unordered_map<int,int> cnt;

for (int r = 0; r < n; r++) 
{
    // 1. Expand window
    cnt[nums[r]]++;

    // 2. Shrink window until valid
    while (window is invalid) 
    {
        cnt[nums[l]]--;
        l++;
    }

    // 3. Update answer
    ans = max(ans, r - l + 1);
}
```