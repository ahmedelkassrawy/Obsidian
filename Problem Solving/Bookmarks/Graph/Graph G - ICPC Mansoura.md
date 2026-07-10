[#Sheet1 : Intro To Graph & DFS - Virtual Judge](https://vjudge.net/contest/690295#problem/G)
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
using namespace std;

int main()
{
    int n, m;
    cin >> n >> m;
    vector<bool> vis(n + 1, false);

    for(int i = 0; i < m; i++)
    {
        int u, v;
        cin >> u >> v;

        vis[u] = vis[v] = true;
    }

    cout << n - 1 << endl;
    
    for(int i = 1; i <= n; i++)
    {
        if(!vis[i])
        {
            for(int j = 1; j <= n; j++)
            {
                if(i != j)
                {
                    cout << i << " " << j << endl;
                }
            }
            break;
        }
    }

    return 0;
}
```