[#Sheet2 : BFS & Graph Applications - Virtual Judge](https://vjudge.net/contest/692604#problem/U)
```C++
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

int n,m,k,s;
vector<int> a;
vector<vector<int>> adj;

vector<int> bfs(int good)
{
    queue<int> q;
    vector<int> dist(n+1,-1);

    for(int i = 1; i <= n; i++)
    {
        if(a[i] == good)
        {
            q.push(i);
            dist[i] = 0;
        }
    }

    while(!q.empty())
    {
        int u = q.front();
        q.pop();

        for(int v : adj[u])
        {
            if(dist[v] == -1)
            {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }

    return dist;
}


int main()
{
    cin >> n >> m >> k >> s;

    a.resize(n+1);
    adj.resize(n+1);

    for(int i = 1; i <= n; i++)
    {
        cin >> a[i];
    }

    for(int i = 0; i < m; i++)
    {
        int u,v;
        cin >> u >> v;

        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    //dist[k][i] = distance from k to i
    vector<vector<int>> dist(k + 1,vector<int> (n + 1, -1));

    for(int i = 1; i <= k; i++)
    {
        dist[i] = bfs(i);
    }

    for(int i = 1; i <= n; i++)
    {
        vector<int> tot;
        for(int j = 1; j <= k; j++)
        {
            tot.push_back(dist[j][i]);
        }
        sort(tot.begin(),tot.end());

        int ans = 0;
        for(int j = 0; j < s; j++)
        {
            ans += tot[j];
        }
        cout << ans << " ";
    }
}
```

### **Problem Overview**

- **Input**:
    
    - `n`: Number of nodes (5)
    - `m`: Number of edges (5)
    - `k`: Number of special nodes (4)
    - `s`: Number of minimum distances to consider for each node (3)
- **Goal**:
    
    - For each node, compute the sum of the **smallest `s` distances** from the node to the `k` special nodes. These nodes are given by the array `a`.

### **Key Components**

1. **Adjacency List (`adj`)**:
    
    - Represents the graph, with each node's neighbors.
2. **Array (`a`)**:
    
    - Specifies which nodes are **special nodes** (`good` nodes). Nodes marked as `good` will be used to compute distances to all other nodes.
3. **Breadth-First Search (BFS)**:
    
    - Used to compute the shortest distance from **any special node** to all other nodes.
4. **Processing Each Node**:
    
    - For each node `i`, it computes the sum of the **smallest `s` distances** to the special nodes.

---

### **Step-by-Step Explanation with Example**

#### **Input**

CopyEdit

`5 5 4 3 1 2 4 3 2 1 2 2 3 3 4 4 1 4 5 2 2 2 2 3`

1. **Graph Construction**:
    
    - Number of nodes = `5` and edges = `5`.
    - The adjacency list is built based on the following edges:
        
        CopyEdit
        
        `1-2 2-3 3-4 4-1 4-5`
        
    - So the adjacency list (`adj`) looks like:
        
        CopyEdit
        
        `adj[1] = {2, 4} adj[2] = {1, 3} adj[3] = {2, 4} adj[4] = {3, 1, 5} adj[5] = {4}`
        
2. **Special Nodes (`a`)**:
    
    - `a = {0, 1, 2, 4, 3, 2}` (1-based indexing).
    - The special nodes are: `1, 2, 4, 3`.
3. **BFS from each special node**:
    
    - Perform a BFS starting from each special node to calculate the shortest distance to all other nodes.
    
    For each special node:
    
    - **BFS from node 1** (good node):
        - Distances: `dist[1] = {0, 0, 1, 1, 1}`
        - Distances from node 1: 0 to itself, 1 to node 2, 1 to node 4, 1 to node 3.
    - **BFS from node 2** (good node):
        - Distances: `dist[2] = {0, 1, 0, 2, 2}`
        - Distances from node 2: 1 to node 1, 0 to itself, 2 to node 4, 2 to node 3.
    - **BFS from node 4** (good node):
        - Distances: `dist[4] = {1, 2, 2, 0, 1}`
        - Distances from node 4: 1 to node 1, 2 to node 2, 0 to itself, 2 to node 3, 1 to node 5.
    - **BFS from node 3** (good node):
        - Distances: `dist[3] = {1, 2, 0, 0, 1}`
        - Distances from node 3: 1 to node 1, 2 to node 2, 0 to itself, 0 to node 4, 1 to node 5.

#### **Distance Matrix**:

The matrix `dist` after BFS will look like this:

CopyEdit

`dist[1] = {0, 1, 1, 1, 1} dist[2] = {1, 0, 2, 2, 2} dist[3] = {1, 2, 0, 0, 1} dist[4] = {1, 2, 2, 0, 1}`

4. **Processing each node (`i`)**: For each node `i` (from 1 to `n`), calculate the sum of the smallest `s = 3` distances from `i` to all `k = 4` special nodes.
    
    For each node `i`:
    
    - **Node 1**:
        - Distances to the special nodes: `[0, 1, 1, 1]`
        - Sort the distances: `[0, 1, 1, 1]`
        - Sum of the smallest 3: `0 + 1 + 1 = 2`
    - **Node 2**:
        - Distances to the special nodes: `[1, 0, 2, 2]`
        - Sort the distances: `[0, 1, 2, 2]`
        - Sum of the smallest 3: `0 + 1 + 2 = 3`
    - **Node 3**:
        - Distances to the special nodes: `[1, 2, 0, 0]`
        - Sort the distances: `[0, 0, 1, 2]`
        - Sum of the smallest 3: `0 + 0 + 1 = 1`
    - **Node 4**:
        - Distances to the special nodes: `[1, 2, 2, 0]`
        - Sort the distances: `[0, 1, 2, 2]`
        - Sum of the smallest 3: `0 + 1 + 2 = 3`
    - **Node 5**:
        - Distances to the special nodes: `[1, 2, 1, 1]`
        - Sort the distances: `[1, 1, 1, 2]`
        - Sum of the smallest 3: `1 + 1 + 1 = 3`

#### **Final Output**:

CopyEdit

`2 3 1 3 3`

### **Explanation of Output**:

For each node, the output represents the sum of the smallest `3` distances to the `4` special nodes. These sums are computed and printed for each node in the graph.

---

### **Time Complexity**:

- **BFS from each special node**: O(n + m) for each BFS, and there are `k` special nodes. Therefore, O(k * (n + m)).
- Sorting the distances for each node: O(k log k), and this is done for each node, so O(n * k log k).

Overall, the time complexity is approximately **O(k * (n + m) + n * k log k)**.