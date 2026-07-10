[#Sheet 3 : Dynamic Programming (Recursive) - Virtual Judge](https://vjudge.net/contest/694272#problem/O)
```C++
#include <iostream>
#include <vector>
#include <cstring>
#include <climits>
#include <algorithm>
using namespace std;

const int N = 2e5 + 5;
int n;
long long dp[N];

struct Project {
    int start, end;
    long long reward;
};

vector<Project> projects;

bool cmp(const Project &a, const Project &b) 
{
    return a.end < b.end; 
}


int overlap(int i) 
{
    int l = 0, r = i - 1, ans = -1;
    
    while (l <= r) 
    {
        int mid = (l + r) / 2;

        if (projects[mid].end < projects[i].start) 
        {
            ans = mid;  
            l = mid + 1;
        } else {
            r = mid - 1;
        }
    }

    return ans;
}

long long go(int i) 
{
    if (i == -1) return 0;  
    if (dp[i] != -1) return dp[i];

    long long ch1 = projects[i].reward;
    int lastNonOverlap = overlap(i);
    if (lastNonOverlap != -1) ch1 += go(lastNonOverlap);

    
    long long ch2 = go(i - 1);

    return dp[i] = max(ch1, ch2);
}

int main() {
    cin >> n;
    projects.resize(n);

    for (int i = 0; i < n; i++) 
    {
        cin >> projects[i].start >> projects[i].end >> projects[i].reward;
    }

    sort(projects.begin(), projects.end(), cmp);

    memset(dp, -1, sizeof(dp));

    cout << go(n - 1) << endl;

    return 0;
}

```