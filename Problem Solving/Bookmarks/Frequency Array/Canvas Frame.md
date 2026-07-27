[Problem - C - Codeforces](https://codeforces.com/group/isP4JMZTix/contest/380288/problem/C)

[[Frequency Array]]
```C++
1. #include <iostream>
2. #include <vector>
3. #include <algorithm>
4. using namespace std;

6. int main() {
7. int n;
8. cin >> n;

10. vector<int> sticks(n);
11. for (int i = 0; i < n; ++i) {
12. cin >> sticks[i];
13. }

15. // Frequency array to count the occurrences of each stick length
16. vector<int> freq(101, 0);
17. for (int length : sticks) {
18. freq[length]++;
19. }

21. // Count pairs
22. vector<int> pairs;
23. for (int i = 1; i <= 100; ++i) {
24. pairs.push_back(freq[i] / 2); // Each pair needs 2 sticks
25. }

27. // Calculate maximum number of frames
28. int total_pairs = 0;
29. for (int p : pairs) {
30. total_pairs += p;
31. }

33. // Each frame needs 2 pairs of sticks
34. int max_frames = total_pairs / 2;

36. cout << max_frames << endl;

38. return 0;
39. }
```