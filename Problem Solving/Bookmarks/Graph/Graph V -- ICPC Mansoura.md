[#Sheet1 : Intro To Graph & DFS - Virtual Judge](https://vjudge.net/contest/690295#status//V/0/)
```C++
#include <vector>
#include <iostream>
using namespace std;

int n;
vector<vector<pair<int, int>>> adj;
vector<bool> vis;
vector<int> ans;

void dfs(int u, int p, int last) {
    for (auto [v, id] : adj[u]) 
    {
        if (v == p) continue;

        if (last == 2) 
        {
            ans[id] = 3;
            dfs(v, u, 3);
        } else {
            ans[id] = 2;
            dfs(v, u, 2);
        }
    }
}

int main() {
    int t;
    cin >> t;

    while (t--) 
    {
        cin >> n;

        adj.assign(n + 1, vector<pair<int, int>>());
        vis.assign(n + 1, false);
        ans.assign(n - 1, 0);

        for (int i = 1; i <= n - 1; i++) {
            int u, v;
            cin >> u >> v;

            adj[u].push_back({v, i});
            adj[v].push_back({u, i});
        }

        int root = -1;
        bool invalid = false;

        for (int i = 1; i <= n; i++) {
            if (adj[i].size() > 2) {
                cout << -1 << '\n';
                invalid = true;
                break; // Stop checking further, move to the next test case
            }
            if (adj[i].size() == 1) root = i;
        }

        if (invalid) continue; // Skip the rest of the loop and move to the next test case

        dfs(root, -1, 2);

        for (int i = 1; i <= n - 1; i++) cout << ans[i] << ' ';
        cout << '\n';
    }

    return 0;
}
```

3andy tree of kaza leaf bs ana 3ayzha linear aw m4 aktr mn 2 34an lw h7ot arkam prime tb2a sum bta3ha mzboot lw node fy elawl aw la5r hyb2a el size bta3ha b 1 bs 