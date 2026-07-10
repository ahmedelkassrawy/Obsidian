### Edge List
```C++
vector<pair<int,int>> edge_list(m);

for(int i = 0; i < m; i++)
{
	cin>>edge_list[i].first>>edge_list[i].second;
}

for(int i = 0; i < m;i++)
{
	cout<<edge_list[i].first<<" "<<edge_list[i].second<<endl;
}

set<pair<int,int>> edge_list;
for(int i = 0; i < m; i++)
{
	int u , v;
	cin>>u>>v;

	edge_list.insert({u,v});
	edge_list.insert({v,u});
}

int q;
cin>>q;

while(q--)
{
	int u,v;
	cin>>u>>v;

	if(edge_list.find({u,v}) != edge_list.end())
	{
		cout<<"YES"<<endl;
	}
	else
	{
		cout<<"NO"<<endl;
	}
}
```

using Matrix
```C++
vector<vector<int>> mat(n+1,vector<int>(n+1,0));

for(int i = 0;i < m;i++)
{
	int u,v;
	cin>>u>>v;

	mat[u][v] = 1;
	mat[v][u] = 1;
}

for(int i = 1; i <= n;i++)
{
	for(int j = 1; j <= n;j++)
	{
		cout<<mat[i][j]<<" ";
	}
	cout<<endl;
}
```

Using Adj List
```C++
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <set>
using namespace std;

int n,m;
vector<vector<int>> adj_list;
vector<bool>vis;

int main()
{
    cin>>n>>m;

    adj_list.resize(n + 1);
    vis.resize(n + 1, 0);

    for(int i = 0; i <m;i++)
    {
        int u ,v;
        cin>>u>>v;

        adj_list[u].push_back(v);
        adj_list[v].push_back(u);
    }
}
```

### DFS
```C++
void DFS(int u)
{
    vis[u] = 1;
    //cout<<u<<' ';
    for(auto v:adj_list[u])
    {
        if(!vis[v])
        {
            DFS(v);
        }
    }
}
```

### Finding connected components
```C++
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <set>
using namespace std;

int n,m;
vector<vector<int>> adj_list;
vector<bool>vis;

void DFS(int u)
{
    vis[u] = 1;
    
    //cout<<u<<' '; to print the connected components
    
    for(auto v:adj_list[u])
    {
        if(!vis[v])
        {
            DFS(v);
        }
    }
}

int main()
{
    cin>>n>>m;

    adj_list.resize(n + 1);
    vis.resize(n + 1, 0);

    for(int i = 0; i <m;i++)
    {
        int u ,v;
        cin>>u>>v;

        adj_list[u].push_back(v);
        adj_list[v].push_back(u);
    }

    int ans = 0;
    for(int i = 1; i <= n ;i++)
    {
        if(!vis[i])
        {
            ans++;
            DFS(i);
            //cout<<endl; //to print the connected components
        }
    }

    cout<<ans<<endl;
}
```

```C++
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <set>
using namespace std;

int n,m;

vector<vector<int>> adj_list,comps;
vector<bool>vis;
vector<int> tmp;

void DFS(int u)
{
    vis[u] = 1;
    
    tmp.push_back(u);

    for(auto v:adj_list[u])
    {
        if(!vis[v])
        {
            DFS(v);
        }
    }
}

int main()
{
    cin>>n>>m;

    adj_list.resize(n + 1);
    vis.resize(n + 1, 0);

    for(int i = 0; i <m;i++)
    {
        int u ,v;
        cin>>u>>v;

        adj_list[u].push_back(v);
        adj_list[v].push_back(u);
    }

    int ans = 0;
    for(int i = 1; i <= n ;i++)
    {
        if(!vis[i])
        {
            ans++;
            DFS(i);

            comps.push_back(tmp);
            tmp.clear();
        }
    }

    for(auto v : comps)
    {
        for(auto u : v)
        {
            cout<<u<<' ';
        }
        cout<<endl;
    }

    cout<<ans<<endl;
}
```

### Checking for trees
```C++
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <set>
using namespace std;

int n,m; // n is the number of nodes and m is the number of edges

vector<vector<int>> adj_list,comps;
vector<bool>vis;
vector<int> tmp;

void DFS(int u) 
{
    vis[u] = 1;

    for(auto v:adj_list[u])
    {


        if(!vis[v])
        {
            DFS(v,u);
        }
    }
}

int main()
{
    cin>>n>>m;

    adj_list.resize(n + 1);
    vis.resize(n + 1, 0);

    for(int i = 0; i <m;i++)
    {
        int u ,v;
        cin>>u>>v;

        adj_list[u].push_back(v);
        adj_list[v].push_back(u);
    }


    int ans = 0;
    for(int i = 1; i <= n ;i++)
    {
        if(!vis[i])
        {
            ans++;
            DFS(i);
        }
    }

    cout<<(ans == 1 && m == n - 1 ? "YES" : "NO")<<endl; 
    //to check if this graph was a tree or not
    cout<<(m == n - ans ? "YES" : "NO")<<endl;
    //to check if this graph was a forest or not
}
```

### Not cyclic
```C++
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <set>
using namespace std;

int n,m; // n is the number of nodes and m is the number of edges

vector<vector<int>> adj_list,comps;
vector<bool>vis;
vector<int> tmp;
bool not_cyclic = 1;

void DFS(int u,int p) //p is the last node i last visted
{
    vis[u] = 1;

    for(auto v:adj_list[u])
    {
        if(v == p) continue;

        if(!vis[v])
        {
            DFS(v,u);
        }
        else
        {
            not_cyclic = 0;
        }
    }
}

int main()
{
    cin>>n>>m;

    adj_list.resize(n + 1);
    vis.resize(n + 1, 0);

    for(int i = 0; i <m;i++)
    {
        int u ,v;
        cin>>u>>v;

        adj_list[u].push_back(v);
        adj_list[v].push_back(u);
    }
    DFS(1,1); //just an invalid value to make the not_cyclic be 1 not zero

    cout<<(not_cyclic?"YES":"NO")<<endl;
}
```

### Cyclic Detetection in Directed Graph
```C++
#include <iostream>
#include <vector>
using namespace std;

int n, m; // n is the number of nodes, m is the number of edges
vector<vector<int>> adj_list;
vector<int> vis; // 0 = unvisited, 1 = visited, 2 = in current DFS path
bool not_cyclic = true;

void DFS(int u)
{
    vis[u] = 2; // Mark as being visited in the current DFS path

    for (auto v : adj_list[u])
    {
        if (!vis[v])
        {
            DFS(v); // Recursively visit unvisited neighbors
        }
        else if (vis[v] == 2)
        {
            not_cyclic = false; // Found a back edge (cycle)
        }
    }

    vis[u] = 1; // Mark as fully visited
}

int main()
{
    cin >> n >> m;

    // Resize adj_list and vis to accommodate n+1 vertices
    adj_list.resize(n + 1);
    vis.resize(n + 1, 0);

    // Read edges and build adjacency list
    for (int i = 0; i < m; i++)
    {
        int u, v;
        cin >> u >> v;

        adj_list[u].push_back(v); // Directed edge from u to v
    }

    // Perform DFS for all unvisited vertices
    for (int i = 1; i <= n; i++)
    {
        if (!vis[i])
        {
            DFS(i);
        }
    }

    // Output result
    cout << (not_cyclic ? "YES" : "NO") << endl;
}
```

### Topological Sorting
```C++
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int n, m; // n is the number of nodes, m is the number of edges
vector<vector<int>> adj_list;
vector<int> vis; // 0 = unvisited, 1 = visited, 2 = in current DFS path
bool not_cyclic = true;
vector<int> topo;

void DFS(int u)
{
    vis[u] = 2; // Mark as being visited in the current DFS path

    for (auto v : adj_list[u])
    {
        if (!vis[v])
        {
            DFS(v); // Recursively visit unvisited neighbors
        }
        else if (vis[v] == 2)
        {
            not_cyclic = false; // Found a back edge (cycle)
        }
    }

    vis[u] = 1; // Mark as fully visited
    topo.push_back(u); // Add to topological order (post-order)
}

int main()
{
    cin >> n >> m;

    // Resize adj_list and vis to accommodate n+1 vertices
    adj_list.resize(n + 1);
    vis.resize(n + 1, 0);

    // Read edges and build adjacency list
    for (int i = 0; i < m; i++)
    {
        int u, v;
        cin >> u >> v;

        adj_list[u].push_back(v); // Directed edge from u to v
    }

    // Perform DFS for all unvisited vertices
    for (int i = 1; i <= n; i++)
    {
        if (!vis[i])
        {
            DFS(i);
        }
    }

    if (not_cyclic)
    {
        // Reverse the topo vector to get the correct topological order
        reverse(topo.begin(), topo.end());

        // Output the topological order
        for (auto i : topo)
        {
            cout << i << " ";
        }
    }
    else
    {
        cout << -1; // Output -1 if the graph contains a cycle
    }

    cout << endl;
}
```

### To check if the graph is connected
```C++
//check if graph is connected
    dfs(1); //to start from any place
		
    for(int i = 1; i<= n ; i++)
    {
        if(!vis[i]) //if not visited then not connected
        {
            cout<<"NO"<<endl;
            return 0;
        }
    }
```