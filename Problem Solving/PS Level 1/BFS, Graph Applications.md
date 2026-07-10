### BFS Code
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
using namespace std;

int n, m;
vector<vector<int>> adj;
vector<bool> vis;
vector<int> levels;

void bfs(int start)
{
    queue<int> q;

    // Step 1: Initialize the queue and mark the starting node as visited
    q.push(start);
    vis[start] = true;
    levels[start] = 0;

    // Step 2: Continue until the queue is empty
    while (!q.empty())
    {
        // Step 3: Pop the front element from the queue
        int curr = q.front();
        q.pop();


        // Step 4: Loop through all the neighbors of the current node
        for (auto v : adj[curr])
        {
            if (!vis[v])
            {
                // Step 5: Mark the neighbor as visited and set its level
                q.push(v);
                vis[v] = true;
                levels[v] = levels[curr] + 1;
            }
        }
    }
}

int main()
{
    cin >> n >> m;

    adj.resize(n + 1);
    vis.resize(n + 1, false);
    levels.resize(n + 1, 0);

    for (int i = 0; i < m; i++)
    {
        int u, v;
        cin >> u >> v;

        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    bfs(1);

    cout<<levels[n] + 1<<endl; //shortest number of nodes
    cout<<levels[n]<<endl; //shortest number of edges

    return 0;
}
```

### Used for an example
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
#include <stack>
using namespace std;

int n, m;
vector<vector<int>> adj;
vector<bool> vis;
vector<int> levels,parent;

void bfs(int start)
{
    queue<int> q;

    // Step 1: Initialize the queue and mark the starting node as visited
    q.push(start);
    vis[start] = true;
    levels[start] = 0;
    parent[start] = -1;

    // Step 2: Continue until the queue is empty
    while (!q.empty())
    {
        // Step 3: Pop the front element from the queue
        int curr = q.front();
        q.pop();


        // Step 4: Loop through all the neighbors of the current node
        for (auto v : adj[curr])
        {
            if (!vis[v])
            {
                // Step 5: Mark the neighbor as visited and set its level
                q.push(v);
                vis[v] = true;
                levels[v] = levels[curr] + 1;
                parent[v] = curr; //the parent of the node is the node that pushed it into the queue
            } 
        }
    }
}

int main()
{
    cin >> n >> m;

    adj.resize(n + 1);
    vis.resize(n + 1, false);
    levels.resize(n + 1, 0);
    parent.resize(n + 1, 0);

    for (int i = 0; i < m; i++)
    {
        int u, v;
        cin >> u >> v;

        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    bfs(1);

    int cur = n;

    stack<int> st;
    while(cur != -1) // -1 is the parent of the starting node
    {
        st.push(cur);
        cur = parent[cur]; // go to the parent of the current node
    }

    while(!st.empty())
    {
        cur = st.top();
        st.pop();
        cout << cur << " ";
    }

    return 0;
}
```

### Before Optimization
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
#include <stack>
#include <map>
using namespace std;

//i am given two nums of n and m , i want to reach from n to m using 
//two methods or operations either n - 1 or 2 * n
//here we dont have any graph given or edges so we will use bfs to solve this problemq

int n,m;
map<int,int> vis,levels; //cause the size of the vis is not available

void bfs(int start)
{
    queue<int> q;

    q.push(start);
    vis[start] = 1;
    levels[start] = 0;

    while(!q.empty())
    {
        int curr = q.front();
        q.pop();

        if(curr > 1 && !vis[curr - 1]) //the curr > 1 is to avoid the negative values and avoid the infinity loop it might get into
        {
            q.push(curr - 1);
            vis[curr - 1] = 1;
            levels[curr - 1] = levels[curr] + 1;
        }

        if(curr < m && !vis[2 * curr]) //1e4 is the maximum value of n to end the infinity loop it might get itself into
        //but its still not fully optimized i will make it curr < m
        //since why do we need to go beyond the value of m
        //we are multiplying the curr by 2 so it will always be greater than m
        {
            q.push(2 * curr);
            vis[2 * curr] = 1;
            levels[2 * curr] = levels[curr] + 1;
        }
    }
}

int main()
{
    cin>>n>>m;

    bfs(n);

    cout<<levels[m]<<endl;
}
```

### After Optimization
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
#include <stack>
#include <map>
using namespace std;

//i am given two nums of n and m , iwant to reach from n to m using 
//two methods or operations either n - 1 or 2 * n
//here we dont have any graph given or edges so we will use bfs to solve this problemq

int n,m;
map<int,int> vis; //cause the size of the vis is not available

int bfs(int start)
{
    queue<pair<int,int>> q;

    q.push({start,0});
    vis[start] = 1;

    while(!q.empty())
    {
        int curr = q.front().first;
        int curr_level = q.front().second;
        q.pop();

        if(curr == m) return curr_level;

        if(curr > m && !vis[curr - 1]) //the curr > 1 is to avoid the negative values and avoid the infinity loop it might get into
        {
            q.push({curr - 1,curr_level + 1});
            vis[curr - 1] = 1;
        }

        if(curr < m && !vis[2 * curr]) //1e4 is the maximum value of n to end the infinity loop it might get itself into
        //but its still not fully optimized i will make it curr < m
        //since why do we need to go beyond the value of m
        //we are multiplying the curr by 2 so it will always be greater than m
        {
            q.push({2 * curr,curr_level + 1});
            vis[2 * curr] = 1;
        }
    }

    return -1;
}

int main()
{
    cin>>n>>m;

    cout<<bfs(n)<<endl;
}

///removed the map of levels
//made the queue of pair<int,int> to store the level of the node on the fly
```

### Bipartite 
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
#include <stack>
#include <map>
using namespace std;

int n,m;
vector<int> vis,levels,teams;
vector<vector<int>> adj;

void bfs(int start)
{
    queue<int> q;

    q.push(start);
    vis[start] = 1;
    levels[start] = 0;
    teams[start] = 1; // 1 for red, 2 for blue
    //ebda2 be2ay loon te7ebo

    while(!q.empty())
    {
        int curr = q.front();
        q.pop();

        for(auto v : adj[curr])
        {
            if(!vis[v])
            {
                vis[v] = 1;
                levels[v] = levels[curr] + 1;
                q.push(v);

                // if(teams[curr] == 1) teams[v] = 2;
                // else teams[v] = 1;

                teams[v] = 3 - teams[curr];
            }
            else
            {
                if(teams[v] == teams[curr]) //that means we are on the ssame team
                {
                    cout<<"IMPOSSIBLE"<<endl;
                    return;
                }
            }
        }
    }

    cout<<"POSSIBLE"<<endl;
}

int main()
{
    cin>>n>>m;

    adj.reserve(n + 1);
    vis.resize(n + 1,0);
    levels.resize(n + 1,0);
    teams.resize(n + 1,0);

    for(int i = 0; i < m; i++)
    {
        int u,v;
        cin>>u>>v;

        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    for(int i = 1; i <= n; i++)
    {
        if(!vis[i])
        {
            bfs(i);
        }
    }

    for(int i = 1; i <= n; i++)
    {
        cout<<teams[i]<<" ";
    }
}
```

##### Second example
https://codeforces.com/problemset/problem/862/B
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
#include <stack>
#include <map>
using namespace std;

int n,m;
vector<int> vis,levels,teams;
vector<vector<int>> adj;
vector<int> cnt;

void bfs(int start)
{
    queue<int> q;

    q.push(start);
    vis[start] = 1;
    levels[start] = 0;
    teams[start] = 1; // 1 for red, 2 for blue
    //ebda2 be2ay loon te7ebo
    cnt[teams[start]]++;

    while(!q.empty())
    {
        int curr = q.front();
        q.pop();

        for(auto v : adj[curr])
        {
            if(!vis[v])
            {
                vis[v] = 1;
                levels[v] = levels[curr] + 1;
                q.push(v);

                // if(teams[curr] == 1) teams[v] = 2;
                // else teams[v] = 1;

                teams[v] = 3 - teams[curr];
                cnt[teams[v]]++;
            }
            else
            {
                if(teams[v] == teams[curr]) //that means we are on the ssame team
                {
                    cout<<"IMPOSSIBLE"<<endl;
                    return;
                }
            }
        }
    }

    cout<<"POSSIBLE"<<endl;
}

int main()
{
    cin>>n;

    adj.reserve(n + 1);
    vis.resize(n + 1,0);
    levels.resize(n + 1,0);
    teams.resize(n + 1,0);
    cnt.resize(3);

    for(int i = 0; i < n-1; i++)
    {
        int u,v;
        cin>>u>>v;

        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    for(int i = 1; i <= n; i++)
    {
        if(!vis[i])
        {
            bfs(i);
        }
    }

    cout<<(cnt[1] * cnt[2]) - (n - 1)<<endl; //the number of edges that we need to add to make the graph connected

}

//We are given a tree (which is a connected, acyclic graph) with n nodes, and we need to add as many edges as possible while ensuring the graph remains bipartite (i.e., we can divide the nodes 
//into two sets where no two nodes within the same set are connected).

//A bipartite graph is a graph where we can color the nodes using two colors 
//such that no two adjacent nodes have the same color.

//We can only add edges between nodes that are in different partitions.

//we use bfs to color the tree into 2 sets
//count how many nodes are in each set (team)
//the number of edges of bipartite graph = (number of nodes in team 1) * (number of nodes in team 2) - (number of edges in the tree)
//because we can add edges between nodes in different teams only
//the num of max tree edges are n-1
//so max additional edges we an add is = (cnt[1] * cnt[2]) - (n - 1)
```

### Topo Sort
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
#include <stack>
#include <map>
using namespace std;

int n,m;
vector<int> vis,levels,indegree,topo;
vector<vector<int>> adj;

void bfs()
{
    queue<int> q;

    for(int i = 1; i <= n; i++)
    //queue contains all valid nodes 
    {
        if(indegree[i] == 0) //starting node if you dont have any in arrows
        {
            q.push(i);
            vis[i] = 1;
            levels[i] = 1;
        }
    }

    //queue {1,6}

    while(!q.empty())
    {
        int curr = q.front();
        q.pop();

        topo.push_back(curr);

        for(auto v : adj[curr])
        {
            if(!vis[v])
            {
                indegree[v]--;

                if(indegree[v] == 0)
                {
                    q.push(v);
                    vis[v] = 1;
                    levels[v] = levels[curr] + 1;
                }
            }
        }
    }
}

//when does topo sort not exist or fail?
//when there is a cycle in the graph

int main()
{
    cin>>n;

    adj.reserve(n + 1);
    vis.resize(n + 1,0);
    levels.resize(n + 1,0);
    indegree.resize(n + 1,0);

    for(int i = 0; i < n-1; i++)
    {
        int u,v;
        cin>>u>>v;

        adj[u].push_back(v); //directed graph
        indegree[v]++;
    }

    bfs();
    if(topo.size() < n) cout<<"IMPOSSIBLE"<<endl;
    //because topo takes the free nodes and then goes on to the next level
    //if there are no free nodes, then the graph has a cycle

    for(auto i : topo) cout<<i<<" ";
}
```

### BFS with Multi Sources
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
#include <stack>
#include <map>
using namespace std;

// Global variables
int n, m, t;                      // n = number of nodes, m = number of edges, t = number of special nodes
vector<int> vis, levels;           // vis = visited array, levels = stores the shortest distance from special nodes
vector<vector<int>> adj;           // adjacency list representation of the graph
map<int, int> is_special;          // map to store special nodes

// Multi-source BFS function to compute the shortest distance from special nodes
void bfs()
{
    queue<int> q;

    // Push all special nodes into the queue as starting points
    for (int i = 1; i <= n; i++)
    {
        if (is_special[i])  // If the node is special
        {
            q.push(i);
            vis[i] = 1;      // Mark as visited
            levels[i] = 0;   // Distance from itself is 0
        }
    }

    // Standard BFS traversal
    while (!q.empty())
    {
        int curr = q.front();
        q.pop();

        // Visit all adjacent nodes
        for (auto v : adj[curr])
        {
            if (!vis[v])  // If not visited yet
            {
                q.push(v);
                vis[v] = 1;                  // Mark as visited
                levels[v] = levels[curr] + 1; // Distance is parent's distance +1
            }
        }
    }
}

int main()
{
    cin >> n >> m; // Read number of nodes and edges

    adj.resize(n + 1);  // Initialize adjacency list
    vis.resize(n + 1, 0); // Initialize visited array
    levels.resize(n + 1, 0); // Initialize levels array

    // Read edges and build the adjacency list
    for (int i = 0; i < n - 1; i++)
    {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    // Read number of special nodes
    cin >> t;
    int sp;
    for (int i = 0; i < t; i++)
    {
        cin >> sp;
        is_special[sp] = 1; // Mark special nodes
    }

    // Perform BFS from all special nodes
    bfs();

    // Process queries
    int q, x;
    cin >> q;
    while (q--)
    {
        cin >> x;
        cout << levels[x] << endl; // Print shortest distance from any special node
    }
}
```

