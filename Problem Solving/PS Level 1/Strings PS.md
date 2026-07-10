```C++
class Solution 
{
public:
    string longestPalindrome(string s) 
    {
        int n = s.size();
        if (n == 0) return "";

        int start = 0, maxLength = 1;

        // Helper function to expand around the center
        auto expandAroundCenter = [&](int left, int right) {
            while (left >= 0 && right < n && s[left] == s[right]) {
                if (right - left + 1 > maxLength) {
                    start = left;
                    maxLength = right - left + 1;
                }
                left--;
                right++;
            }
        };

        for (int i = 0; i < n; i++) {
            // Odd-length palindromes (single center)
            expandAroundCenter(i, i);

            // Even-length palindromes (two centers)
            expandAroundCenter(i, i + 1);
        }

        return s.substr(start, maxLength);
    }
};

//[Longest Palindromic Substring - LeetCode](https://leetcode.com/problems/longest-palindromic-substring/solutions/4212564/beats-96-49-5-different-approaches-brute-force-eac-dp-ma-recursion/)
```

```C++
class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs)
    {
        unordered_map<string,vector<string>> mp;

        for(auto s : strs)
        {
            string word = s;
            sort(word.begin(),word.end())
            mp[word].push_back(s);
        }


        vector<vector<string>> ans;
        for(auto x: mp)
        {
            ans.push_back(x.second);
        }
        return ans;
    }
};
```

```C++
class Solution {
public:
    bool isAnagram(string s, string t) {
        if (s.size() != t.size()) return false; // Strings of different lengths can't be anagrams

        map<char, int> mp;

        // Count character frequencies in `s`
        for (char c : s) {
            mp[c]++;
        }

        // Decrement character frequencies based on `t`
        for (char c : t) {
            if (mp.find(c) == mp.end() || mp[c] == 0) {
                return false; // Character not found or count mismatch
            }
            mp[c]--;
        }

        // Check if all counts are zero
        for (auto x : mp) {
            if (x.second != 0) {
                return false;
            }
        }

        return true;
    }
};
//[Valid Anagram - LeetCode](https://leetcode.com/problems/valid-anagram/)
```