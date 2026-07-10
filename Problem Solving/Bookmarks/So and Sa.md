[Problem - J - Codeforces](https://codeforces.com/group/5pUldkahAU/contest/520378/problem/J)
[[Sets]][[Vectors]]

```C++
#include <iostream>
#include <string>
#include <vector>
#include <set>
using namespace std;

int main() {
    int t;
    cin >> t;

    while (t--) {
        int n;
        cin >> n;
        string s;
        cin >> s;

        // Track unique character counts for prefix and suffix
        vector<int> prefix_counts(n, 0);
        vector<int> suffix_counts(n, 0);
        set<char> unique_chars;

        // Calculate unique characters for prefix up to each position
        for (int i = 0; i < n; i++) {
            unique_chars.insert(s[i]);
            prefix_counts[i] = unique_chars.size();
        }

        // Clear the set to reuse for suffix calculation
        unique_chars.clear();

        // Calculate unique characters for suffix from each position
        for (int i = n - 1; i >= 0; i--) {
            unique_chars.insert(s[i]);
            suffix_counts[i] = unique_chars.size();
        }

        // Find the maximum possible value of prefix_counts[i] + suffix_counts[i+1]
        int max_unique_sum = 0;
        for (int i = 0; i < n - 1; i++) {
            max_unique_sum = max(max_unique_sum, prefix_counts[i] + suffix_counts[i + 1]);
        }

        // Output the result for this test case
        cout << max_unique_sum << endl;
    }

    return 0;
}

```