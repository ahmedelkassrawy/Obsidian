## Subarray sum

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
    prefix_sum_count[0] = 1;

    for (int i = 0; i < n; i++) 
    {
        prefix_sum += arr[i];

        // Check if there's a prefix sum that would result in a subarray sum of x.
        if (prefix_sum_count.find(prefix_sum - x) != prefix_sum_count.end()) 
        {
            subarray_count += prefix_sum_count[prefix_sum - x];
        }

        // Update the prefix sum count map.
        prefix_sum_count[prefix_sum]++;
    }

    cout << subarray_count << endl;

    return 0;
}
```

## Subarray of distinct values
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

## Basic Sliding window sum
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

## Subarray Divisibility 
same as the sum of subarray but now dividing 
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

## We want pairs of same sum
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

we want all the values from 2 --> 2*n and then another for loop in to loop on the freq array. the other is looping - value of j 
if the value of other is 0 or negative don't loop to the if condition.
total and min(j.second,mp[other]) --> is choosing the min freq there
total is double no. of teams

## Longest substring with no duplicates
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

### Min substring window
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